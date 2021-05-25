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

from collections import defaultdict, namedtuple
from flask_dropzone import Dropzone

from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.datastructures import FileStorage
from flask import Flask, request, send_file, render_template, abort, jsonify, redirect, url_for, make_response
from flask_cors import CORS
from flask_basicauth import BasicAuth
from flasgger import Swagger

import utils
import worker
import database
import GEOBIM_Tool as geobim
# from geobim_analysis import analyser

application = Flask(__name__)
dropzone = Dropzone(application)

# application.config['DROPZONE_UPLOAD_MULTIPLE'] = True
# application.config['DROPZONE_PARALLEL_UPLOADS'] = 3

DEVELOPMENT = os.environ.get('environment', 'production').lower() == 'development'

DEVELOPMENT = True

if not DEVELOPMENT and os.path.exists("/version"):
    PIPELINE_POSTFIX = "." + open("/version").read().strip()
else:
    PIPELINE_POSTFIX = ""

if not DEVELOPMENT:
    # In some setups this proved to be necessary for url_for() to pick up HTTPS
    application.wsgi_app = ProxyFix(application.wsgi_app, x_proto=1)
    
MODELS_PATH = "../models-preloaded/"
IDS_PATH = MODELS_PATH + "ids.json"

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

# geobim.init()
# app = geobim.application()
# app.start()
analysers = {}

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
    
    path = MODELS_PATH
    fns = [fn for fn in os.listdir(path) if os.path.isfile(os.path.join(path, fn)) and fn[-4:] == ".ifc"]
    
    return jsonify(fns)

@application.route('/load_preloaded_file/<fn>', methods=['GET'])
def load_preloaded_file(fn):
    path = MODELS_PATH + fn
    ids_f = open(IDS_PATH)
    ids = json.load(ids_f)
    id = ids[fn]["id"]
    
    if id not in analysers.keys():
        analyser = geobim.analyser()
        analyser.load(path)
        analysers[id] = analyser
        
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
                f.close()
                settings[fn] = {}
                settings[fn]["id"] = id
                settings[fn]["path"] = path + fn
                
    os.remove(settings_path)
    with open(settings_path, 'w') as f:
        json.dump(settings, f)
    

def init_analyser(id):
    settings_path = IDS_PATH
    with open(settings_path, "r") as settings_file:
        settings = json.load(settings_file)
        for model in settings:
            if settings[model]["id"] == id:
                analyser = geobim.analyser()
                analyser.load(settings[model]["path"])
                analysers[id] = analyser
                
def init_analysers():
    settings_path = IDS_PATH
    with open(settings_path, "r") as settings_file:
        settings = json.load(settings_file)
        for model in settings:
            if id not in analysers:
                analyser = geobim.analyser()
                analyser.load(settings[model]["path"])
                analysers[id] = analyser
                
@application.route('/init_all_analysers', methods=['GET'])
def init_all_analysers():
    if DEVELOPMENT:
        t = threading.Thread(target=init_analysers)
        t.start()
    else:
        q.enqueue(preload_files)
        
    return jsonify("success")

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
    if id not in analysers:
        init_analyser(id)
    result = analysers[id].footprintWKT(floornumber)
    return jsonify({"wkt": result})

@application.route('/analysis/<id>/overhangsingle/<floornumber>', methods=['GET'])
def overhangsingle(id, floornumber):
    if id not in analysers:
        init_analyser(id)
    result = analysers[id].OverhangOneFloor(floornumber)
    return jsonify(result)

@application.route('/analysis/<id>/overhangall', methods=['GET'])
def overhangall(id):
    if id not in analysers:
        init_analyser(id)
    result = analysers[id].OverhangAll_new()
    return jsonify(result)

@application.route('/analysis/<id>/height', methods=['GET'])
def height(id):
    if id not in analysers:
        init_analyser(id)
    result = analysers[id].GetHeight()
    return result

@application.route('/analysis/<id>/baseheight/<floornumber>', methods=['GET'])
def baseheight(id, floornumber):
    if id not in analysers:
        init_analyser(id)
    result = analysers[id].GetBaseHeight(floornumber)
    return result

@application.route('/analysis/<id>/overlapsingle/<floornumber>', methods=['GET'])
def overlapsingle(id, floornumber):
    if id not in analysers:
        init_analyser(id)
    result = analysers[id].OverlapOneFloor(floornumber)
    return result

@application.route('/analysis/<id>/overlapall', methods=['GET'])
def overlapall(id):
    if id not in analysers:
        init_analyser(id)
    result = analysers[id].OverlapAll()
    return result

@application.route('/analysis/<id>/overlapsinglebbox/<floornumber>', methods=['GET'])
def overlapsinglebbox(id, floornumber):
    if id not in analysers:
        init_analyser(id)
    result = analysers[id].OverlapOneFloorOBB(floornumber)
    return result

@application.route('/analysis/<id>/overlapallbbox', methods=['GET'])
def overlapallbbox(id):
    if id not in analysers:
        init_analyser(id)
    result = analysers[id].OverlapAllOBB()
    return result
    
@application.route('/analysis/<id>/setbasefloornum/<floornumber>', methods=['GET'])
def setbasefloornum(id, floornumber):
    if id not in analysers:
        init_analyser(id)
    analysers[id].setBaseFloornum()
    return "success"

@application.route('/analysis/<id>/addgeoreferencepoint/<xyz>', methods=['GET'])
def addgeoreferencepoint(id, x, y, z):
    if id not in analysers:
        init_analyser(id)
    analysers[id].setBaseFloornum()
    return "success"

@application.route('/analysis/<id>/setoverhangdir/<direction>', methods=['GET'])
def setoverhangdir(id, direction):
    if id not in analysers:
        init_analyser(id)
    analysers[id].setOverhangdir(direction)
    return "success"

@application.route('/analysis/<id>/setoverlapparameters', methods=['GET'])
def setoverlapparameters(id, x, y, z):
    if id not in analysers:
        init_analyser(id)
    analysers[id].setOverlapParameters(x, y, z)
    return "success"


"""
# Create a file called routes.py with the following
# example content to add application-specific routes

from main import application

@application.route('/test', methods=['GET'])
def test_hello_world():
    return 'Hello world'
"""
try:
    import routes
except ImportError as e:
    pass
