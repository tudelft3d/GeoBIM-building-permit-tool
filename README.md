ifc-pipeline
------------

Based on [ifc-pipeline](https://github.com/AECgeeks/ifc-pipeline):

> A processing queue that uses [IfcOpenShell](https://github.com/IfcOpenShell/IfcOpenShell/) to convert IFC input files into a graphic display using glTF 2.0 and [BIMSurfer2](https://github.com/AECgeeks/BIMsurfer2/) for visualization.

## Installation

1. Install Docker Compose and npm
2.  `git submodule update --init --recursive` in the cloned repository
3.  `npm i` in `application/geobim_viewer`
4.  `sudo docker-compose up -d` in the root directory
5.  `npm run serve` in `application/geobim_viewer`

You probably want to change the amount of gunicorn and database workers in  `docker-compose.yml` for production (`-w` and `NUM_WORKERS` respectively).

### Development

1. Install missing Python libraries with `application/requirements.txt`
2. Install other dependencies that are seen in `application/Dockerfile`  (need to see if there's an easy way to do this, otherwise explain here)
3. `export FLASK_ENV=development`
4. `flask run` in `application/`

### Possible issues

For developing the GEOBIM_Tool, geos Python library should be of version 3.8.1. Newer can cause issues.