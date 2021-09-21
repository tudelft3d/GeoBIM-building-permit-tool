FROM debian:buster-slim

WORKDIR /

RUN apt-get -y update && apt-get -y --no-install-recommends --no-install-suggests install python3 python3-pip

RUN apt-get -y update && apt-get -y --no-install-recommends --no-install-suggests install python3 python3-pip unzip wget libpq-dev build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev npm python3-setuptools python3-dev python3-wheel supervisor libpq-dev gdal-bin python-gdal python3-gdal libgdal-dev git swig
RUN apt-get install ffmpeg libsm6 libxext6  -y
# Conda
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
RUN apt-get update

RUN apt-get install -y wget && rm -rf /var/lib/apt/lists/*

RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh 
    
# GDAL & PROJ
RUN conda install -c conda-forge proj
RUN conda install -c conda-forge gdal=3.2.0
ENV CPLUS_INCLUDE_PATH="/usr/include/gdal"
ENV C_INCLUDE_PATH="/usr/include/gdal"

# Flask/GEOBIM_Tool
RUN python3 -m pip install flask==1.1.2 flask-cors==3.0.10 numpy==1.19.4 Pillow==8.3.0 gunicorn==20.1.0 rq==1.9.0 redis==3.5.3 sqlalchemy==1.4.20 psycopg2==2.9.1 sqlalchemy-utils==0.37.8 flasgger==0.9.5 requests==2.25 attrs==20.3.0 auto-sklearn==0.12.1 backcall==0.2.0 certifi==2020.12.5 chardet==4.0.0 click==7.1.2 click-plugins==1.1.1 cligj==0.7.1 cloudpickle==1.6.0 ConfigSpace==0.4.17 cycler==0.10.0 Cython==0.29.21 dask==2021.1.1 decorator==4.4.2 descartes==1.1.0 distributed==2021.1.1 emcee==3.0.2 Fiona==1.8.18 GDAL==3.2.0 geopandas==0.9.0 HeapDict==1.0.1 idna==2.10 itsdangerous==1.1.0 jedi==0.17.0 Jinja2==2.11.2 joblib==1.0.0 jsonschema==3.2.0 kiwisolver==1.3.1 lazy-import==0.2.2 liac-arff==2.5.0 MarkupSafe==1.1.1 matplotlib==3.3.3 mistune==0.8.4 msgpack==1.0.2 munch==2.5.0 networkx==2.5 osmnx==1.0.1 pandas==1.2.1 pyaml==20.4.0 pyDOE==0.3.8 pynisher==0.6.3 pyparsing==2.4.7 pyproj==3.0.1 pyqt5==5.14.0 PyQt5-sip==12.8.1 pyrfr==0.8.0 pyrsistent==0.17.3 python-dateutil==2.8.1 pytz==2021.1 pyvista==0.32.1 PyYAML==5.3.1 Rtree==0.9.7 scikit-learn==0.24.1 scikit-optimize==0.8.1 scipy==1.5.4 Shapely==1.7.1 sklearn==0.0 smac==0.13.1 sortedcontainers==2.3.0 tblib==1.7.0 threadpoolctl==2.1.0 toolz==0.11.1 tornado==6.1 urllib3==1.21.1 Werkzeug==1.0.1 zict==2.0.0

# WORKDIR /
RUN apt-get -y update && apt-get -y install libxcb-xinerama0

RUN npm install -g jsdoc gltf-pipeline requirejs npx uglify-js
RUN python3 -m pip install --upgrade pip

# PythonOCC
RUN conda install -c conda-forge pythonocc-core=7.5.1
RUN git clone https://github.com/tpaviot/pythonocc-utils.git /tmp/pythonocc
RUN python3 -m pip install /tmp/pythonocc

# IfcConvert v0.6.0
RUN wget https://s3.amazonaws.com/ifcopenshell-builds/IfcConvert-v0.6.0-c15fdc7-linux64.zip -O /tmp/IfcConvert.zip
RUN unzip /tmp/IfcConvert.zip -d /usr/bin

RUN wget -O /tmp/ifcopenshell_python.zip https://s3.amazonaws.com/ifcopenshell-builds/ifcopenshell-python-`python3 -c 'import sys;print("".join(map(str, sys.version_info[0:2])))'`-v0.6.0-c15fdc7-linux64.zip
RUN mkdir -p `python3 -c 'import site; print(site.getusersitepackages())'`
RUN unzip -d `python3 -c 'import site; print(site.getusersitepackages())'` /tmp/ifcopenshell_python.zip

# Temporary 'hotfix'
RUN wget  -O `python3 -c 'import site; print(site.getusersitepackages())'`/ifcopenshell/validate.py https://raw.githubusercontent.com/IfcOpenShell/IfcOpenShell/v0.6.0/src/ifcopenshell-python/ifcopenshell/validate.py

RUN conda install -c conda-forge cgal

# Server
WORKDIR /www/static
COPY application/queue.conf /etc/supervisord.conf

WORKDIR /www
COPY models-preloaded /www/models-preloaded
COPY application/*.py /www/
COPY application/templates /www/templates
COPY application/GEOBIM_Tool /www/GEOBIM_Tool
