##################################################################################
#                                                                                #
# Copyright (c) 2020 AECgeeks                                                    #
#                                                                                #
# Permission is hereby granted, free of charge, to any person obtaining a copy   #
# of this software and associated documentation files (the "Software"), to deal  #
# in the Software without restriction, including without limitation the rights   #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell      #
# copies of the Software, and to permit persons to whom the Software is          #
# furnished to do so, subject to the following conditions:                       #
#                                                                                #
# The above copyright notice and this permission notice shall be included in all #
# copies or substantial portions of the Software.                                #
#                                                                                #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR     #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,       #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE    #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER         #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE  #
# SOFTWARE.                                                                      #
#                                                                                #
##################################################################################

from __future__ import print_function

import os
import json
import threading
import logging
import shutil

from collections import namedtuple

from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.datastructures import FileStorage
from flask import Flask, request, send_file, render_template, abort, jsonify, redirect, url_for, make_response
from flask_cors import CORS
from flasgger import Swagger

import utils
import worker
import database
import GEOBIM_Tool as geobim

application = Flask(__name__)

DEVELOPMENT = os.environ.get('environment', 'production').lower() == 'development'

if not DEVELOPMENT and os.path.exists("/version"):
    PIPELINE_POSTFIX = "." + open("/version").read().strip()
else:
    PIPELINE_POSTFIX = ""

if not DEVELOPMENT:
    # In some setups this proved to be necessary for url_for() to pick up HTTPS
    application.wsgi_app = ProxyFix(application.wsgi_app, x_proto=1)
    
if os.environ.get("FLASK_ENV") == "development":
    MODELS_PATH = "../models-preloaded/"
    IDS_PATH = MODELS_PATH + "ids_development.json"
else:
    MODELS_PATH = "./models-preloaded/"
    IDS_PATH = MODELS_PATH + "ids_production.json"

CORS(application)
application.config['SWAGGER'] = {
    'title': os.environ.get('APP_NAME', 'ifc-pipeline request API'),
    'openapi': '3.0.2',
    "specs": [
        {
            "version": "0.1",
            "title": os.environ.get('APP_NAME', 'ifc-pipeline request API'),
            "description": os.environ.get('APP_NAME', 'ifc-pipeline request API'),
            "endpoint": "spec",
            "route": "/apispec",
        },
    ]
}
swagger = Swagger(application)

if not DEVELOPMENT:
    from redis import Redis
    from rq import Queue

    q = Queue(connection=Redis(host=os.environ.get("REDIS_HOST", "localhost")), default_timeout=3600)

@application.route('/', methods=['GET'])
def get_main():
    return render_template('index.html')


def process_upload(filewriter, callback_url=None):
    id = utils.generate_id()
    d = utils.storage_dir_for_id(id)
    os.makedirs(d)

    filewriter(os.path.join(d, id + ".ifc"))

    session = database.Session()
    session.add(database.model(id, ''))
    session.commit()
    session.close()

    if DEVELOPMENT:
        t = threading.Thread(target=lambda: worker.process(id, callback_url))
        t.start()

    else:
        q.enqueue(worker.process, id, callback_url)

    return id


def process_upload_multiple(files, callback_url=None):
    id = utils.generate_id()
    d = utils.storage_dir_for_id(id)
    os.makedirs(d)

    file_id = 0
    paths = []
    session = database.Session()
    m = database.model(id, '')
    session.add(m)

    for file in files:
        fn = file.filename
        filewriter = lambda fn: file.save(fn)
        path = os.path.join(d, id + "_" + str(file_id) + ".ifc")
        filewriter(path)
        paths.append(path)
        file_id += 1
        m.files.append(database.file(id, ''))
        analyser = geobim.analyser()
        analyser.load(path)
        analysers[id] = analyser

    session.commit()
    session.close()

    if DEVELOPMENT:
        t = threading.Thread(target=lambda: worker.process(id, callback_url))
        t.start()
    else:
        q.enqueue(worker.process, id, callback_url)
        
    settings_path = IDS_PATH
    with open(settings_path, "r") as settings_file:
        settings = json.load(settings_file)
        settings[file.filename] = {}
        settings[file.filename]["id"] = id
        settings[file.filename]["path"] = paths[0]
                
    os.remove(settings_path)
    with open(settings_path, 'w') as f:
        json.dump(settings, f)
        
    return id

@application.route('/preloaded_models_info', methods=['GET'])
def preloaded_models_info():
    with open(IDS_PATH, 'r') as f:
        settings = json.load(f)
        fns = list(settings.keys())
    
    return jsonify(fns)

@application.route('/load_preloaded_file/<fn>', methods=['GET'])
def load_preloaded_file(fn):
    ids_f = open(IDS_PATH)
    ids = json.load(ids_f)
    id = ids[fn]["id"]
        
    return id

@application.route('/init_preloaded_files', methods=['GET'])
def init_preloaded_files():
    
    if DEVELOPMENT:
        t = threading.Thread(target=preload_files)
        t.start()
    else:
        q.enqueue(preload_files)
        
    return jsonify("success")

def preload_files():
    path = MODELS_PATH
    fns = [fn for fn in os.listdir(path) if os.path.isfile(os.path.join(path, fn))]
    
    settings_path = path + "ids.json"
    with open(settings_path, "r") as settings_file:
        settings = json.load(settings_file)
    
        for fn in fns:
            if fn[-4:] == ".ifc" and fn not in settings.keys():
                f = open(path + fn, 'rb')
                file = FileStorage(f)
                
                id = process_upload_multiple([file])
                d = utils.storage_dir_for_id(id)
                f.close()
                settings[fn] = {}
                settings[fn]["id"] = id
                settings[fn]["path"] = path + fn
                
    os.remove(settings_path)
    with open(settings_path, 'w') as f:
        json.dump(settings, f)
    

def init_analyser(id):
    global analysers
    
    print("Init analyser, checking if exists...")
    settings_path = IDS_PATH
    with open(settings_path, "r") as settings_file:
        settings = json.load(settings_file)
        for model in settings:
            if settings[model]["id"] == id:
                print("Creating analyser for " + model)
                analyser = geobim.analyser()
                analyser.load(settings[model]["path"])
                analysers[id] = analyser
                print("Finished creating analyser for " + model)
                
def init_analysers():
    global analysers

    settings_path = IDS_PATH
    
    f = open(settings_path, "r")
    settings = json.load(f)
    print(settings)
    f.close()
        
    for model in settings:
        if settings[model]["id"] not in analysers:
            print("Create analyser for " + model)
            analyser = geobim.analyser()
            analyser.load(settings[model]["path"])
            analysers[settings[model]["id"]] = analyser
            print("Finished creating analyser for " + model)
        else:
            print("Analyser for " + model + " already exists")
                
# @application.route('/init_all_analysers', methods=['GET'])
def init_all_analysers():
    
    t = threading.Thread(target=init_analysers)
    t.start()
    
    """
    if DEVELOPMENT:
        t = threading.Thread(target=init_analysers)
        t.start()
    else:
        q.enqueue(init_analysers)
    """
        
    # return jsonify("success")

@application.route('/upload_ifc', methods=['POST'])
def put_main():
    """
    Upload model
    ---
    requestBody:
      content:
        multipart/form-data:
          schema:
            type: object
            properties:
              ifc:
                type: string
                format: binary
    responses:
      '200':
        description: redirect
    """
    ids = []

    files = []
    for key, f in request.files.items():
        if key.startswith('file'):
            if f.filename[-4:] != ".ifc":
                return "Invalid file", 400
            files.append(f)

    id = process_upload_multiple(files)
    d = utils.storage_dir_for_id(id)
    url = url_for('get_progress', id=id)

    if request.accept_mimetypes.accept_json:
        return jsonify({"url": url})
    else:
        return redirect(url)


@application.route('/p/<id>', methods=['GET'])
def check_viewer(id):
    if not utils.validate_id(id):
        abort(404)
    return render_template('progress.html', id=id)


@application.route('/pp/<id>', methods=['GET'])
def get_progress(id):
    if not utils.validate_id(id):
        abort(404)
    session = database.Session()
    model = session.query(database.model).filter(database.model.code == id).all()[0]
    session.close()
    return jsonify({"progress": model.progress})


@application.route('/log/<id>.<ext>', methods=['GET'])
def get_log(id, ext):
    log_entry_type = namedtuple('log_entry_type', ("level", "message", "instance", "product"))

    if ext not in {'html', 'json'}:
        abort(404)

    if not utils.validate_id(id):
        abort(404)
    logfn = os.path.join(utils.storage_dir_for_id(id), "log.json")
    if not os.path.exists(logfn):
        abort(404)

    if ext == 'html':
        log = []
        for ln in open(logfn):
            l = ln.strip()
            if l:
                log.append(json.loads(l, object_hook=lambda d: log_entry_type(
                    *(d.get(k, '') for k in log_entry_type._fields))))
        return render_template('log.html', id=id, log=log)
    else:
        return send_file(logfn, mimetype='text/plain')


@application.route('/v/<id>', methods=['GET'])
def get_viewer(id):
    if not utils.validate_id(id):
        abort(404)
    d = utils.storage_dir_for_id(id)

    ifc_files = [os.path.join(d, name) for name in os.listdir(d) if
                 os.path.isfile(os.path.join(d, name)) and name.endswith('.ifc')]

    if len(ifc_files) == 0:
        abort(404)

    failedfn = os.path.join(utils.storage_dir_for_id(id), "failed")
    if os.path.exists(failedfn):
        return render_template('error.html', id=id)

    for ifc_fn in ifc_files:
        glbfn = ifc_fn.replace(".ifc", ".glb")
        if not os.path.exists(glbfn):
            abort(404)

    n_files = len(ifc_files) if "_" in ifc_files[0] else None

    return render_template(
        'viewer.html',
        id=id,
        n_files=n_files,
        postfix=PIPELINE_POSTFIX
    )


@application.route('/m/<fn>', methods=['GET'])
def get_model(fn):
    """
    Get model component
    ---
    parameters:
        - in: path
          name: fn
          required: true
          schema:
              type: string
          description: Model id and part extension
          example: BSESzzACOXGTedPLzNiNklHZjdJAxTGT.glb
    """

    id, ext = fn.split('.', 1)

    if not utils.validate_id(id):
        abort(404)

    if ext not in {"xml", "svg", "glb", "unoptimized.glb"}:
        abort(404)

    path = utils.storage_file_for_id(id, ext)

    if not os.path.exists(path):
        abort(404)

    if os.path.exists(path + ".gz"):
        import mimetypes
        response = make_response(
            send_file(path + ".gz",
                      mimetype=mimetypes.guess_type(fn, strict=False)[0])
        )
        response.headers['Content-Encoding'] = 'gzip'
        return response
    else:
        return send_file(path)


@application.route('/analysis/<id>/wkt/<floornumber>', methods=['GET'])
def floor_wkt(id, floornumber):
    result = analysers[id].footprintWKT(floornumber)
    return jsonify({"wkt": result})

@application.route('/analysis/<id>/overhangsingle/<floornumber>', methods=['GET'])
def overhangsingle(id, floornumber):
    result = analysers[id].OverhangOneFloor(floornumber)
    return jsonify(result)

@application.route('/analysis/<id>/overhangall', methods=['GET'])
def overhangall(id):
    result = analysers[id].OverhangAll_new()
    return jsonify(result)

@application.route('/analysis/<id>/height', methods=['GET'])
def height(id):
    result = analysers[id].GetHeight()
    return result

@application.route('/analysis/<id>/baseheight/<floornumber>', methods=['GET'])
def baseheight(id, floornumber):
    result = analysers[id].GetBaseHeight(floornumber)
    return result

@application.route('/analysis/<id>/overlapsingle/<floornumber>', methods=['GET'])
def overlapsingle(id, floornumber):
    result = analysers[id].OverlapOneFloor(floornumber)
    return result

@application.route('/analysis/<id>/overlapall', methods=['GET'])
def overlapall(id):
    result = analysers[id].OverlapAll()
    return result

@application.route('/analysis/<id>/overlapsinglebbox/<floornumber>', methods=['GET'])
def overlapsinglebbox(id, floornumber):
    result = analysers[id].OverlapOneFloorOBB(floornumber)
    return result

@application.route('/analysis/<id>/overlapallbbox', methods=['GET'])
def overlapallbbox(id):
    result = analysers[id].OverlapAllOBB()
    return result
    
@application.route('/analysis/<id>/setbasefloornum/<floornumber>', methods=['GET'])
def setbasefloornum(id, floornumber):
    analysers[id].setBaseFloornum(floornumber)
    return "success"

@application.route('/analysis/<id>/addgeoreferencepoint/<xyz>', methods=['GET'])
def addgeoreferencepoint(id, x, y, z):
    analysers[id].setBaseFloornum()
    return "success"

@application.route('/analysis/<id>/setoverhangdir/<direction>', methods=['GET'])
def setoverhangdir(id, direction):
    analysers[id].setOverhangdir(direction)
    return "success"

@application.route('/analysis/<id>/setoverlapparameters/<s>/<dbscan>/<k>', methods=['GET'])
def setoverlapparameters(id, s, dbscan, k):
    analysers[id].setOverlapParameters(s, dbscan, k)
    return "success"

@application.route('/analysis/<id>/overhangroads/<floornum>/<guidelines>', methods=['GET'])
def overhangroads(id, floornum, guidelines):

    guidelinesParsed = {}
    for guideline in guidelines.split('|'):
        entry = guideline.split(": ")
        guidelinesParsed[entry[0]] = float(entry[1])
    
    ifc_path = None
    ids = open(IDS_PATH, 'r')
    settings = json.load(ids)
    ids.close()
    for k, v in settings.items():
        if v["id"] == id:
            ifc_path = v["path"]
            break
    
    if floornum != "none":
        result = analysers[id].overhangRoads(guidelinesParsed, int(floornum))
    else:
        result = analysers[id].overhangRoads(guidelinesParsed)
    
    return jsonify(result)

@application.route('/analysis/<id>/overhangroadsalphashape/<floornum>/<guidelines>', methods=['GET'])
def overhangroadsalphashape(id, floornum, guidelines):

    guidelinesParsed = {}
    for guideline in guidelines.split('|'):
        entry = guideline.split(": ")
        guidelinesParsed[entry[0]] = float(entry[1])
    
    ifc_path = None
    ids = open(IDS_PATH, 'r')
    settings = json.load(ids)
    ids.close()
    for k, v in settings.items():
        if v["id"] == id:
            ifc_path = v["path"]
            break
    
    if floornum != "none":
        result = analysers[id].overhangRoadsAlphaShape(guidelinesParsed, int(floornum))
    else:
        result = analysers[id].overhangRoadsAlphaShape(guidelinesParsed)
    
    return jsonify(result)

@application.route('/analysis/<id>/heightcheck/<max>', methods=['GET'])
def heightcheck(id, max):
    result = analysers[id].heightCheck(float(max))
    return jsonify(result)

@application.route('/analysis/<id>/boundarycheck', methods=['GET'])
def boundarycheck(id):
    result = analysers[id].boundaryCheck()
    return jsonify(result)

@application.route('/analysis/<id>/getgeoref', methods=['GET'])
def getgeoref(id):
    result = analysers[id].getGeoref()
    if result != None:
        return jsonify(result)
    else:
        return "No georeferencing information in IFC file", 400
    
@application.route('/analysis/<id>/parking/<zone>', methods=['POST', 'GET'])
def parking(id, zone):
    
    ifc_path = None
    ids = open(IDS_PATH, 'r')
    settings = json.load(ids)
    ids.close()
    for k, v in settings.items():
        if v["id"] == id:
            ifc_path = v["path"]
            break

    if request.method == 'GET':
        result = analysers[id].parkingCalculate(ifc_path, zone)
    
    elif request.method == 'POST':
        result = None
        
        for key,f in request.files.items():
            if key.startswith('file') and key.endswith('xlsx'):
                print(f.filename)
                fn = f.filename
                p = os.path.join("/data/", fn)
                f.save(p)
                
                result = analysers[id].parkingCalculate(ifc_path, zone)
    
    if result:
        return result
    else:
        return "Error", 400

    
if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    application.logger.handlers = gunicorn_logger.handlers
    application.logger.setLevel(gunicorn_logger.level)
    
# Move preloaded data to correct folder because it doesn't work doing it directly in the Dockerfile for some reason
if os.environ.get("FLASK_ENV") != "development":
    shutil.copytree("/www/models-preloaded/G", "/data/G", dirs_exist_ok=True)
analysers = {}
init_all_analysers()
print("Initialising analysers done")


try:
    import routes
except ImportError as e:
    pass
