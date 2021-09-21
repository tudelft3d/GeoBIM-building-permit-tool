<template>

  <div id="analysis">
    
      <nav
      class="navbar is-light is-size-7"
      role="navigation"
      aria-label="flask navigation"
      id="navbar"
    >
      
          <div
            class="navbar-item has-dropdown is-hoverable"
          >
            <a class="navbar-link">
              File
            </a>
            <div class="navbar-dropdown">
              <a class="navbar-item">

                <input class="file-input" type="file" ref="ifcFiles" @change="selectedIfcFile">
                Upload IFC
              </a>

              <a class="navbar-item" @click="pickFile()">
                Pick IFC
              </a>

              <a class="navbar-item">

                <input class="file-input" type="file" ref="requirementsFile" @change="selectedPermitFile">
                Upload permit requirements

              </a>

              <a class="navbar-item">

                <input type="checkbox" id="checkbox" checked @change="performanceTest = !performanceTest">
                <label for="checkbox">Performance improvement</label>
                
              </a>

              
            </div>

          </div>

          <div
            class="navbar-item has-dropdown is-hoverable"
          >
            <a class="navbar-link">
              Clear
            </a>
            <div class="navbar-dropdown">

              <a class="navbar-item" @click="clearViewer()">
                Clear viewer
              </a>

              <a class="navbar-item" @click="clearAnalysisVisualisation()">
                Clear analysis visualisation
              </a>
              
            </div>

          </div>

          <div
            class="navbar-item has-dropdown is-hoverable"
          >
            <a class="navbar-link">
              Preprocess
            </a>
            <div class="navbar-dropdown">

                <a class="navbar-item" @click="setBaseFloorNumSettings()">
                Set base floor number
                </a>

                <!-- <a class="navbar-item" @click="addGeoreferencePointSettings()">
                Add georeference point
                </a> -->

                <!-- <a class="navbar-item" @click="hoi()">
                Set overhang direction
                </a> -->

                <a class="navbar-item" @click="setOverlapParamsSettings()">
                Set overlap parameters
                </a>
              
            </div>

          </div>

            <div
            class="navbar-item has-dropdown is-hoverable"
          >
            <a class="navbar-link">
              Overlap
            </a>
            <div class="navbar-dropdown">

                <a class="navbar-item" @click="overlapSingleSettings()">
                Single floor overlap
                </a>

                <a class="navbar-item" @click="overlapSingleBboxSettings()">
                Single floor overlap bounding box
                </a>

                <a class="navbar-item" @click="overlapAllSettings()">
                All floors overlap
                </a>

                <a class="navbar-item" @click="overlapAllBboxSettings()">
                All floors overlap bounding box
                </a>
              
            </div>

          </div>

            <div
            class="navbar-item has-dropdown is-hoverable"
          >
            <a class="navbar-link">
              Overhang
            </a>
            <div class="navbar-dropdown">

                <a class="navbar-item" @click="overhangSingleSettings()">
                Single floor overhang
                </a>

                <a class="navbar-item" @click="overhangAllSettings()">
                All floors overhang
                </a>

                <a class="navbar-item is-dark" @click="overhangRoadsSettings()" id="overhang">
                Floors overhang (roads)
                </a>

            </div>

          </div>

            <div
            class="navbar-item has-dropdown is-hoverable"
          >
            <a class="navbar-link">
              Height
            </a>
            <div class="navbar-dropdown">

                <a class="navbar-item" @click="heightSettings()">
                Height
                </a>

                <a class="navbar-item" @click="heightNewSettings()" id="height">
                Height (roads)
                </a>

                <a class="navbar-item" @click="baseHeightSettings()">
                Get floor height
                </a>
              
            </div>

          </div>

          <div
            class="navbar-item has-dropdown is-hoverable"
          >
            <a class="navbar-link">
              Other analysis
            </a>
            <div class="navbar-dropdown">

                <a class="navbar-item" @click="wktFootprintSettings">
                  Write floor footprint to WKT
                </a>

                <a class="navbar-item" @click="parkingUnitsSettings()">
                  Parking units calculation
                </a>

                <a class="navbar-item" @click="parcelLimitSettings()">
                  Parcel limit check
                </a>
              
            </div>

          </div>

    <b-modal
      v-model="showModal"
      has-modal-card
    >
      <div class="modal-card" modal-background-background-color>
        <header class="modal-card-head">
          <p class="modal-card-title">
            {{ modalParams.title }}
            
          </p>
          <button
            class="delete"
            aria-label="close"
            @click="showModal = false; resetModalParams()"
          />
        </header>
        <section class="modal-card-body">
          <div class="content" style="white-space: pre-line">

            {{ modalParams.info }}

            <b-field v-for="(input, label) in modalParams.fields" v-bind:key="(input, label)" v-bind:label="label">

              <b-input v-model="modalParams.input[ input ]"></b-input>
            </b-field>

            <b-field v-for="(input, label) in modalParams.fieldsBig" v-bind:key="(input, label)" v-bind:label="label">

              <b-input type="textarea" v-model="modalParams.input[ input ]"></b-input>
            </b-field>

            <b-field v-if="modalParams.file" label="Upload file">

              <div class="file has-name">
                <label class="file-label">
                  <input class="file-input" type="file" ref="modalFile" @change="selectedModalFile">
                  <span class="file-cta">
                    <span class="file-icon">
                      <i class="fas fa-upload"></i>
                    </span>
                    <span class="file-label">
                      Choose a file…
                    </span>
                  </span>
                </label>
              </div>
              
            </b-field>

            <b-field label="Result">
              <textarea class="textarea" :value="modalParams.result"></textarea>
            </b-field>

            <div class="buttons">
              <b-button type="is-light" @click="analysisCall(modalParams.function)">OK</b-button>
              <b-button type="is-light" v-if="modalParams.result.length != 0" @click="downloadFile(modalParams.result, 'text')">Save result</b-button>
            </div>

          </div>
        </section>
      </div>
    </b-modal>

    <b-modal
      v-model="showFilePicker"
      has-modal-card
    >
      <div class="modal-card" modal-background-background-color>
        <header class="modal-card-head">
          <p class="modal-card-title">
            Available IFC files
          </p>
          <button
            class="delete"
            aria-label="close"
            @click="showFilePicker = false"
          />
        </header>
        <section class="modal-card-body">
          <div class="content">

            <div class="control">

              <div v-for="fn in availableFiles" :key="fn">
                <label class="radio">
                <input type="radio" name="pickedId">
                {{ fn }}
                </label>
                <br>
              </div>

            </div>

            <br>

            <div class="buttons">
              <b-button type="is-light" @click="loadPreloadedFile">Load</b-button>
            </div>

          </div>
        </section>
      </div>
    </b-modal>

    </nav>

  </div>
</template>

<script>

import axios from 'axios';
import shp from 'shpjs';
import earcut from 'earcut';
import * as THREE from 'three';
import { BufferGeometryUtils } from 'three/examples/jsm/utils/BufferGeometryUtils.js';

function initialData() {

  return {

      showModal: false,
      showFilePicker: false,
      loadedId: "",
      v: undefined,
      performanceTest: true,
      availableFiles: [],
      modalParams: { "fields": {}, "fieldsBig": {}, "title": "", "info": "", "result": "", "function": "", "input": {}, "file": false },
      permitParams: {},
      georef: {
          "direction": [ 0, 0, 0 ], 
          "location": [ 0, 0, 0 ]
          },

  }

}

export default {
  name: 'Viewer',

  props: {

    baseURL: {
      type: String,
      default: process.env.VUE_APP_FLASK_PATH
    },

    filename: {
      type: String,
      default: "result"
    },

    cameraParams: {

      type: Object,
      default() {

        return { "pan": 100, "rotate": 8, "zoom": 5 }

      }

    },

  },

  data() {

    return initialData();

  },

  mounted: function() {

  },

  watch: {

    showModal: function (val) {

      if ( val == false ) {

        this.resetModalParams();

      }

    }

  },

  methods: {

    clearViewer() {

      this.$data.v.bimSurfer3D.destroy();
      this.$data.v.destroy();
      Object.assign( this.$data, initialData() );

    },

    clearAnalysisVisualisation() {

      this.$data.v.clearAnalysisVisualisation();

    },

    resetModalParams() {

      Object.assign( this.$data.modalParams, initialData().modalParams );

    },

    poll( url ) {

      fetch( url )

      .then(function(r) { return r.json(); })

      .then(function(r) {

        if ( r.progress === 100 ) {

          const split = url.split( "/" );
          const id = split[ split.length - 1 ];

          this.loadedId = id;
          
          this.loadModel( id );

          return;

        }

        setTimeout( () => {

          console.log( r.progress );

          this.poll( url );

        }, 1000);

      }.bind( this ));

    },

  async selectedIfcFile() {

    const files = this.$refs.ifcFiles; 
    const file = files.files[0];

    if ( !file || file.name.slice(-4) != ".ifc" ) {

      alert( "Please choose an IFC file!" );
      return;

    }

    const form = new FormData();
    form.append("file", file);

    axios.post( this.baseURL + 'upload_ifc', form, {

        headers: {

          'Content-Type': 'multipart/form-data'

        }

    })

    .then( function ( res ) {

      const url = res.data[ 'url' ];

      console.log(url);

      this.poll( this.baseURL + url );

    }
    
    .bind( this ))
    .catch(console.error);

  },

  async selectedModalFile() {

    const files = this.$refs.modalFile; 
    const file = files.files[0];

    if ( !file || file.name.slice(-5) != ".xlsx" ) {

      alert( "Please choose an XLSX file!" );
      return;

    }

    this.modalParams.file = file;

  },

  async selectedPermitFile() {

    const files = this.$refs.requirementsFile; 
    const file = files.files[0];

    if ( !file || file.name.slice(-5) != ".json" ) {

      alert( "Please choose a JSON file!" );
      return;

    }

    this.permitParams = JSON.parse(await file.text());
    this.permitAnalysis();

  },

  async permitAnalysis() {

    const params = this.permitParams;

    if ( params.height != undefined ) {

      const maxHeight = params.height.maxMetres;
      await this.height();
      this.permitParams.height["result"] = {};
      this.permitParams.height["result"]["height"] = parseFloat(this.modalParams.result);
      this.permitParams.height["result"]["complies"] = parseFloat(this.modalParams.result) < parseFloat(maxHeight);

    }

    if ( params.overlap != undefined ) {

      for ( var k in params.overlap ) {

        const maxPercentage = params.overlap[k].maxPercentage;
        const floor = params.overlap[k].floor;

        if ( floor != undefined ) {

          this.modalParams.input[ "floorNumber" ] = floor;
          await this.overlapSingle();
          var result = JSON.parse(this.modalParams.result);
          this.permitParams.overlap[k].result = result;
          this.permitParams.overlap[k].result["complies"] = parseFloat(this.modalParams.result["overlap_percentage"]) < parseFloat(maxPercentage);

        } else {

          await this.overlapAll();
          var result = JSON.parse(this.modalParams.result);
          this.permitParams.overlap[k].result = result;
          this.permitParams.overlap[k].result["complies"] = parseFloat(result["overlap_percentage"]) < parseFloat(maxPercentage);

        }

      }

    }

    if ( params.overhang != undefined ) {

      for ( var k in params.overhang ) {

        const maxMetres = params.overhang[k].maxMetres;
        const floor = params.overhang[k].floor;

        if ( floor != undefined ) {

          this.modalParams.input[ "floorNumber" ] = floor;
          await this.overhangSingle();
          var result = JSON.parse(this.modalParams.result);
          this.permitParams.overhang[k].result = result;
          this.permitParams.overhang[k].result["complies"] = ( parseFloat(result.up_overhang) < parseFloat(maxMetres) ) && ( parseFloat(result.low_overhang) < parseFloat(maxMetres) );

        } else {

          await this.overhangAll();
          var result = JSON.parse(this.modalParams.result);
          this.permitParams.overhang[k].result = result;
          this.permitParams.overhang[k].result["complies"] = ( parseFloat(result.north.distance) < parseFloat(maxMetres) ) && ( parseFloat(result.south.distance) < parseFloat(maxMetres) );


        }
        
      }

    }

    console.log(this.permitParams);
    this.downloadFile(this.permitParams, 'json');
    
  },

  async loadModel( id ) {

    fetch( this.baseURL + "/analysis/" + this.loadedId + "/getgeoref" )
      .then(function(r) { 
      
        if (r.status === 200) {

          return r.json(); 
          
        } else {

          return undefined;

        } })
      .then(function(res) {

        var loadBasemap = false;

        if (res != undefined) {
          this.georef = res;
          loadBasemap = true;
        }

        var v = new ifcViewer({
          domNode: 'right',
          svgDomNode: 'bottom',
          modelId: id,
          withTreeVisibilityToggle: true,
          n_files: window.NUM_FILES,
          flaskPath: process.env.VUE_APP_FLASK_PATH
        });
        if (window.SPINNER_CLASS) {
            v.setSpinner({className: window.SPINNER_CLASS});
        } else if (window.SPINNER_URL) {
            v.setSpinner({url: window.SPINNER_URL});
        }
        v.load2d();
        v.load3d(this.performanceTest, this.georef, undefined, undefined, id);
        v.loadMetadata('middle');
        v.loadTreeView('top');

        this.v = v;
        this.$data.v = v;
        this.v.bimSurfer3D.setCameraControls( this.cameraParams );

        // this.v.loadShp( "../../../../shp.js/BRK_SelectieCentrum.shp", this.georef );


        return loadBasemap;

    }.bind( this ))
    .then( async function( load ) {

      // if ( load || true ) {

        const threeGroup = await this.parseGeojson();
        this.v.loadGroup( threeGroup );

      // }

    }.bind( this ));

  },
  
  adjacentGeom(geom, point, threshold) {

    var centroid = [ 0,0 ];
    var total = 0;
  
    for ( var i = 0; i < geom.length; i++ ) {

      for ( var j = 0; j < geom[i].length; j++ ) {

        total += 1;
        centroid[0] += geom[i][j][0];
        centroid[1] += geom[i][j][1];

      }

    }

    if ( total != 0 ) {

      centroid[0] /= total;
      centroid[1] /= total;

    }

    const distance = Math.sqrt( Math.pow( centroid[0] - point[0], 2 ) + Math.pow( centroid[1] - point[1], 2 ) );

    return distance <= threshold;

  },

  fontLoader() {

    return new Promise( ( resolve, reject ) => {

      const loader = new THREE.FontLoader();
      loader.load( 'helvetiker_regular.typeface.json', data => resolve( data ), null, reject );

    } )

  },

  async parseGeojson() {

    var shpFile = await fetch('shp/Wegvakonderdelen_subset.shp');
    var shpBuf = await shpFile.arrayBuffer();
    var dbfFile = await fetch('shp/Wegvakonderdelen_subset.dbf');
    var dbfBuf = await dbfFile.arrayBuffer();
    var geojson = await shp.combine([shp.parseShp(shpBuf), shp.parseDbf(dbfBuf)]);

    var group = new THREE.Group();
    const font = await this.fontLoader();
    const meshColor = 0xdbdad7;
    const lineColor = 0x111111;

    var meshGeometries = [];
    var lineGeometries = [];
    var lineIndices = [];

    for (var i = 0; i < geojson.features.length; i ++) {

        var feature = geojson.features[i];
        var geom = feature.geometry.coordinates;
        
        // TODO: use IFC model bounding box instead of georef point, and polygon-point distance formula instead of centroid
        if ( !this.adjacentGeom(geom, this.georef.location, 140) ) {

          continue;

        }

        var geom2 = earcut.flatten(geom);
        var triangles = earcut(geom2.vertices, geom2.holes, geom2.dimensions);

        var vertices3d = [];
        for ( var t = 0; t < triangles.length; t++ ) {

          const v = triangles[t];
          vertices3d.push(geom2.vertices[v*2], 0, - geom2.vertices[v*2+1]);

        }

        var threeGeom = new THREE.BufferGeometry();
        threeGeom.addAttribute( 'position', new THREE.Float32BufferAttribute( vertices3d, 3 ) );
        meshGeometries.push( threeGeom );

        var color = 0xdbdad7;
        const material = new THREE.MeshBasicMaterial( { color: color, depthWrite: false } );
        const mesh = new THREE.Mesh( threeGeom, material );
        
        const id = feature.properties.ID;
        mesh.name = id;

        if ( id == '358205' || id == '35152' || id == '35238'  ) {

          const bbox = new THREE.Box3().setFromObject( mesh );

          console.log( feature.properties.STRAAT );

          const textGeom = new THREE.TextGeometry( feature.properties.STRAAT, {
            font: font,
            size: 5,
            height: 0,
            curveSegments: 3
          } );

          // const lineMaterial = new THREE.LineBasicMaterial( { color: 0xffffff, transparent: true, opacity: 0.5 } );
          const meshMaterial = new THREE.MeshPhongMaterial( { color: 0x156289, emissive: 0x072534, side: THREE.DoubleSide, flatShading: true } );

          const line = new THREE.LineSegments( textGeom, lineMaterial );
          const textMesh = new THREE.Mesh( textGeom, meshMaterial );
          textMesh.renderOrder = 2;
          const center = bbox.getCenter();
          textMesh.position.set( center.x, center.y, center.z );
          textMesh.rotateX( - Math.PI / 2 );
          // const maxZ = Math.abs( bbox.max.z );
          // const angle = Math.atan2( maxZ, 1 );

          textMesh.rotateZ( 0.8 );
          group.add( textMesh );

        }
        
        for ( var g = 0; g < geom.length; g++ ) {

          var line = [];
          for ( var v = 0; v < geom[ g ].length; v++ ) {

            lineGeometries.push( geom[ g ][ v ][ 0 ], 0, - geom[ g ][ v ][ 1 ] );

            if ( v != 0 ) {

              line.push( lineGeometries.length / 3 - 2, lineGeometries.length / 3 - 1 );

            }

          }

          lineIndices.push( ...line );

        }
      
    }

    const mergeGeom = BufferGeometryUtils.mergeBufferGeometries( meshGeometries );
    const mergeMaterial = new THREE.MeshBasicMaterial( { color: meshColor, depthWrite: false } );
    const mergeMesh = new THREE.Mesh( mergeGeom, mergeMaterial );
    group.add( mergeMesh );

    var mergeLineGeom = new THREE.BufferGeometry();
    mergeLineGeom.addAttribute( 'position', new THREE.BufferAttribute( new Float32Array( lineGeometries ), 3 ) );
    mergeLineGeom.setIndex( new THREE.BufferAttribute( new Uint16Array( lineIndices ), 1 ) );
    const lineMaterial = new THREE.LineBasicMaterial({

      color: lineColor,
      linewidth: 1,
      depthWrite: false

    });
    const mergeLines = new THREE.LineSegments( mergeLineGeom, lineMaterial);
    mergeLines.renderOrder = 1;
    group.add( mergeLines );

    const location = this.georef.location;
    group.translateX(- location[0]);
    group.translateY(- location[2]);
    group.translateZ( location[1] );

    return group;

  },

  pickFile() {

    fetch( this.baseURL + "/preloaded_models_info" )
      .then(function(r) { return r.json(); })
      .then(function(res) {

        this.availableFiles = res;

    }.bind( this ));

    this.showFilePicker = true;

  },

  loadPreloadedFile() {

    var fn;

    var radios = document.getElementsByName('pickedId');
    for (var i = 0, length = radios.length; i < length; i++) {

      if (radios[i].checked) {

        fn = radios[i].labels[0].innerText;
        fn = fn.trim();

        break;
      }
    }

    this.showFilePicker = false;

    fetch( this.baseURL + "/load_preloaded_file/" + fn )
      .then(function(r) { return r.text(); })
      .then(function(res) {

        this.loadedId = res;
        this.loadModel( this.loadedId );

    }.bind( this ));

  },

    wktFootprintSettings() {

      this.modalParams.title = "Floor footprint WKT";
      this.modalParams.fields = {"Floor number": "floorNumber"}
      this.modalParams.function = "wktFootprint";
      this.modalParams.info = "Returns the footprint of the selected floor in WKT (well-known text) format."
      this.modalParams.input[ "floorNumber" ] = "";
      this.showModal = true;

    },

    wktFootprint() {

      fetch( this.baseURL + "/analysis/" + this.loadedId + "/wkt/" + this.modalParams.input[ "floorNumber" ] )
        .then(function(r) { return r.json(); })
        .then(function(res) {

          console.log( res.wkt );
          this.modalParams.result = res.wkt;

      }.bind( this ));

    },

  analysisCall( functionName ) {

    this[ functionName ]();

  },

  overhangSingleSettings() {

    this.modalParams.title = "Single floor overhang";
    this.modalParams.fields = {"Floor number": "floorNumber"}
    this.modalParams.function = "overhangSingle";
    this.modalParams.info = "Calculates the overhang in metres of the specified floor over the adjacent streets."
    this.modalParams.input[ "floorNumber" ] = "";
    this.showModal = true;

  },

  async overhangSingle() {

    return fetch( this.baseURL + "/analysis/" + this.loadedId + "/overhangsingle/" + this.modalParams.input[ "floorNumber" ] )
      .then(function(r) { return r.json(); })
      .then(function(res) {

        console.log( res );
        this.modalParams.result = JSON.stringify(res, null, 2 );

    }.bind( this ));

  },

  overhangAllSettings() {

    this.modalParams.title = "All floors overhang";
    this.modalParams.function = "overhangAll";
    this.modalParams.info = "Calculates the overhang in metres of all floors over the adjacent streets."
    this.showModal = true;

  },

  async overhangAll() {

    return fetch( this.baseURL + "/analysis/" + this.loadedId + "/overhangall" )
      .then(function(r) { return r.json(); })
      .then(function(res) {

        console.log( res );
        this.modalParams.result = JSON.stringify(res, null, 2 );

    }.bind( this ));

  },

  overhangRoadsSettings() {

    this.modalParams.title = "Roads overhang";
    this.modalParams.fields = { "Floor number (leave empty for all floors)": "floorNumber" }
    this.modalParams.fieldsBig = { "Guidelines (type 'streetname: maxHeight' per line).\nFor example:\n\nBoompjes: 5\nHertekade: 3": "guidelines" };
    this.modalParams.function = "overhangRoads";
    this.modalParams.info = "Calculates the overhang in metres of all floors over the adjacent streets."
    this.modalParams.input[ "floorNumber" ] = "";
    this.modalParams.input[ "guidelines" ] = "";
    this.showModal = true;

  },

  async overhangRoads() {

    if ( this.modalParams.input[ "floorNumber" ] == "" ) {
      var floornum = "none";
    } else {
      var floornum = this.modalParams.input[ "floorNumber" ];
    }

    const guidelines = this.modalParams.input.guidelines.replace( '\n', '|' );

    return fetch( this.baseURL + "/analysis/" + this.loadedId + "/overhangroads/" + floornum + "/" + guidelines )
      .then(function(r) { return r.json(); })
      .then(function(res) {

        console.log( res );

        this.modalParams.result = JSON.stringify(res, null, 2);

        for ( let i = 0; i < res[ "all_checks" ].length; i++ ) {

          for ( const [ key, values ] of Object.entries( res[ "all_checks" ][ i ] ) ) {

            var linestring = values[ 3 ];
            var coordinatesString = linestring.split( "(" )[ 1 ].slice( 0, -1 ).split( ", " );
            var coordinates = [];
            var p1 = coordinatesString[ 0 ].split(" ");
            var p2 = coordinatesString[ 1 ].split(" ");
            var coordinates = [ [ [ parseFloat( p1[0] ), - parseFloat( p1[1] ) ], [ parseFloat( p2[0] ), - parseFloat( p2[1] ) ] ] ];
            
            var pass = values[ 0 ];
            var color = ( pass == "Pass" ) ? 0x00ff00 : 0xff0000;

            this.v.loadLine( this.georef, coordinates, color, "overhangLine" );

          }

          for ( const [ key, value ] of Object.entries( res[ "rogue_checks" ][ i ] ) ) {

            var linestring = value;
            var coordinatesString = linestring.split( "(" )[ 1 ].slice( 0, -1 ).split( ", " );
            var coordinates = [];
            var p1 = coordinatesString[ 0 ].split(" ");
            var p2 = coordinatesString[ 1 ].split(" ");
            var coordinates = [ [ [ parseFloat( p1[0] ), - parseFloat( p1[1] ) ], [ parseFloat( p2[0] ), - parseFloat( p2[1] ) ] ] ];

            var color = 0x000000;

            this.v.loadLine(this.georef, coordinates, color, "overhangLine" );

          }

        }

    }.bind( this ));

  },

  heightSettings() {

    this.modalParams.title = "Get height";
    this.modalParams.function = "height";
    this.modalParams.info = "Calculates the height of the building";
    this.showModal = true;

  },

  async height() {

    return fetch( this.baseURL + "/analysis/" + this.loadedId + "/height" )
      .then(function(r) { return r.text(); })
      .then(function(res) {

        console.log( res );
        this.modalParams.result = res;

    }.bind( this ));

  },

  heightNewSettings() {

    this.modalParams.title = "Get height";
    this.modalParams.function = "heightNew";
    this.modalParams.fields = {"Maximum height": "maxHeight"}
    this.modalParams.input[ "maxHeight" ] = "";
    this.modalParams.info = "Calculates the height of the building, with the base height being the highest height of the adjacent streets.";
    this.showModal = true;

  },

  async heightNew() {

    return fetch( this.baseURL + "/analysis/" + this.loadedId + "/heightcheck/" + this.modalParams.input.maxHeight )
      .then(function(r) { return r.json(); })
      .then(function(res) {

        console.log( res );
        this.modalParams.result = JSON.stringify(res, null, 2 );

        const height = this.modalParams.input.maxHeight;
        const wkt = res[ "wkt" ];

        if ( res[ "height_check" ][ 0 ] == "Pass" ) {
          var color = 0x00ff00;
        } else {
          var color = 0xff0000;
        }

        var coordinates = [];
        var coordinatesString = wkt.split("(")[ 2 ].split(", ").slice( 0, -2 );
        console.log(coordinatesString);
        for ( var i = 0; i < coordinatesString.length; i++ ) {

          const split = coordinatesString[i].split(" ");
          coordinates.push( [ parseFloat( split[0] ), parseFloat( split[1] ) ] );

        }

        var geom = earcut.flatten([coordinates]);
        var triangles = earcut(geom.vertices, geom.holes, geom.dimensions);

        var vertices3d = [];
        for ( var t = 0; t < triangles.length; t++ ) {

          const v = triangles[t];
          vertices3d.push(geom.vertices[v*2], height, - geom.vertices[v*2+1]);

        }

        var threeGeom = new THREE.BufferGeometry();
        threeGeom.addAttribute( 'position', new THREE.Float32BufferAttribute( vertices3d, 3 ) );

        const material = new THREE.MeshBasicMaterial( { color: color, side: THREE.DoubleSide, transparent: true, opacity: 0.8 } );

        const mesh = new THREE.Mesh( threeGeom, material );
        var group = new THREE.Group();
        group.name = "heightPlane";
        group.add( mesh );

        const location = this.georef.location;
        
        group.translateX(- location[0]);
        group.translateY(- location[2]);
        group.translateZ( location[1] );

        this.v.loadGroup( group );

    }.bind( this ));

  },

  baseHeightSettings() {

    this.modalParams.title = "Get floor height";
    this.modalParams.fields = {"Floor number": "floorNumber"}
    this.modalParams.function = "baseHeight";
    this.modalParams.info = "";
    this.modalParams.input[ "floorNumber" ] = "";
    this.showModal = true;

  },

  baseHeight() {

    fetch( this.baseURL + "/analysis/" + this.loadedId + "/baseheight/" + this.modalParams.input[ "floorNumber" ] )
      .then(function(r) { return r.json(); })
      .then(function(res) {

        console.log( res );
        this.modalParams.result = JSON.stringify(res, null, 2 );

    }.bind( this ));

  },

  overlapSingleSettings() {

    this.modalParams.title = "One floor overlap";
    this.modalParams.fields = {"Floor number": "floorNumber"}
    this.modalParams.function = "overlapSingle";
    this.modalParams.info = "Calculates the overlap area and percentage of the specified floor, over the base floor (which is by default the ground floor, and can be altered through 'Preprocess -> Set base floor number')";
    this.modalParams.input[ "floorNumber" ] = "";
    this.showModal = true;

  },

  async overlapSingle() {

    return fetch( this.baseURL + "/analysis/" + this.loadedId + "/overlapsingle/" + this.modalParams.input[ "floorNumber" ] )
      .then(function(r) { return r.json(); })
      .then(function(res) {

        console.log( res );
        this.modalParams.result = JSON.stringify(res, null, 2 );

    }.bind( this ));

  },

  parcelLimitSettings() {

    this.modalParams.title = "Parcel limit check";
    this.modalParams.function = "parcelLimit";
    this.modalParams.info = "Checks if the building fits within the parcel limit.";
    this.showModal = true;

  },

  async parcelLimit() {

    return fetch( this.baseURL + "/analysis/" + this.loadedId + "/boundarycheck" )
      .then(function(r) { return r.json(); })
      .then(function(res) {

        console.log( res );
        this.modalParams.result = JSON.stringify(res, null, 2 );

    }.bind( this ));

  },

  overlapSingleBboxSettings() {

    this.modalParams.title = "One floor overlap bounding box";
    this.modalParams.fields = {"Floor number": "floorNumber"}
    this.modalParams.function = "overlapSingleBbox";
    this.modalParams.info = "Calculates the overlap area and percentage of the specified floor, over the base floor (which is by default the ground floor, and can be altered through 'Preprocess -> Set base floor number'). Takes the bounding boxes of the floors, instead of the actual shapes.";
    this.modalParams.input[ "floorNumber" ] = "";
    this.showModal = true;

  },

  overlapSingleBbox() {

    fetch( this.baseURL + "/analysis/" + this.loadedId + "/overlapsinglebbox/" + this.modalParams.input[ "floorNumber" ] )
      .then(function(r) { return r.json(); })
      .then(function(res) {

        console.log( res );
        this.modalParams.result = JSON.stringify(res, null, 2 );

    }.bind( this ));

  },

  overlapAllSettings() {

    this.modalParams.title = "All floors overlap";
    this.modalParams.function = "overlapAll";
    this.modalParams.info = "Calculates the overlap area and percentage of the all floors, over the base floor (which is by default the ground floor, and can be altered through 'Preprocess -> Set base floor number')";
    this.showModal = true;

  },

  async overlapAll() {

    return fetch( this.baseURL + "/analysis/" + this.loadedId + "/overlapall" )
      .then(function(r) { return r.json(); })
      .then(function(res) {

        console.log( res );
        this.modalParams.result = JSON.stringify(res, null, 2 );

    }.bind( this ));

  },

  overlapAllBboxSettings() {

    this.modalParams.title = "All floors overlap bounding box";
    this.modalParams.function = "overlapAllBbox";
    this.modalParams.info = "Calculates the overlap area and percentage of all floors, over the base floor (which is by default the ground floor, and can be altered through 'Preprocess -> Set base floor number'). Takes the bounding boxes of the floors, instead of the actual shapes.";
    this.showModal = true;

  },

  overlapAllBbox() {

    fetch( this.baseURL + "/analysis/" + this.loadedId + "/overlapallbbox" )
      .then(function(r) { return r.json(); })
      .then(function(res) {

        console.log( res );
        this.modalParams.result = JSON.stringify(res, null, 2 );

    }.bind( this ));

  },

  setBaseFloorNumSettings() {

    this.modalParams.title = "Set base floor number";
    this.modalParams.fields = {"Floor number": "floorNumber"}
    this.modalParams.function = "setBaseFloorNum";
    this.modalParams.info = "Set the base floor for the overlap calculations.";
    this.modalParams.input[ "floorNumber" ] = "";
    this.showModal = true;

  },

  setBaseFloorNum() {

    fetch( this.baseURL + "/analysis/" + this.loadedId + "/setbasefloornum/" + this.modalParams.input[ "floorNumber" ] )
      .then(function(r) { return r.text(); })
      .then(function(res) {

        console.log( res );
        this.modalParams.result = res;

    }.bind( this ));

  },

  setOverlapParamsSettings() {

    this.modalParams.title = "Set overlap parameters";
    this.modalParams.fields = {"s": "s", "dbscan": "dbscan", "k": "k"}
    this.modalParams.function = "setOverlapParams";
    this.modalParams.info = "";
    this.modalParams.input[ "s" ] = "";
    this.modalParams.input[ "dbscan" ] = "";
    this.modalParams.input[ "k" ] = "";
    this.showModal = true;

  },

  setOverlapParams() {

    fetch( this.baseURL + "/analysis/" + this.loadedId + "/setoverlapparameters/" + this.modalParams.input[ "s" ] + "/" + this.modalParams.input[ "dbscan" ] + "/" + this.modalParams.input[ "k" ] )
      .then(function(r) { return r.text(); })
      .then(function(res) {

        console.log( res );
        this.modalParams.result = res;

    }.bind( this ));

  },

  addGeoreferencePointSettings() {

    this.modalParams.title = "Add georeference point";
    this.modalParams.fields = {"Point (\"x, y, z\")": "point"}
    this.modalParams.function = "addGeoreferencePoint";
    this.modalParams.info = "";
    this.modalParams.input[ "point" ] = "";
    this.showModal = true;

  },

  addGeoreferencePoint() {

    fetch( this.baseURL + "/analysis/" + this.loadedId + "/addgeoreferencepoint/" + this.modalParams.input[ "point" ] )
      .then(function(r) { return r.text(); })
      .then(function(res) {

        console.log( res );

    }.bind( this ));

  },

  parkingUnitsSettings() {

    this.modalParams.title = "Parking units calculation";
    this.modalParams.fields = {"Zone type (A, B, C)": "zoneType"}
    this.modalParams.function = "parkingUnits";
    this.modalParams.info = "Calculate parking requirements. Upload of XLSX file currently not supported.";
    this.modalParams.input[ "zoneType" ] = "";
    // this.modalParams.file = true;
    this.showModal = true;

  },

  parkingUnits(){

    fetch( this.baseURL + '/analysis/' + this.loadedId + "/parking/" + this.modalParams.input.zoneType )
      .then(function(r) { return r.text(); })
      .then(function(res) {

        console.log( res );
        this.modalParams.result = res 

    }.bind( this ));

    // POST request with XLSX file:
    // const file = this.modalParams.file;
    // const form = new FormData();
    // form.append("file", file);

    // if ( !file || file.name.slice(-5) != ".xlsx" ) {

    //   alert( "Please choose an XLSX file!" );
    //   return;

    // }

    // axios.post( this.baseURL + '/analysis/' + this.loadedId + "/parking/" + this.modalParams.input.zoneType, form, {

    //     headers: {

    //       'Content-Type': 'multipart/form-data'

    //     }

    // })

    // .then( function ( res ) {

    // }
    
    // .bind( this ))
    // .catch(console.error);

  },

  downloadFile(data, type) {

    var filename = this.filename;
    var mime;

    if ( type == "text" ) {

      mime = "text/plain";
      filename += ".txt";

    } else if ( type == "json" ) {

      mime = "application/json";
      filename += ".json";
      data = JSON.stringify(data);

    }

    const file = new Blob([data], {type: mime});
    if (window.navigator.msSaveOrOpenBlob) // IE10+
        window.navigator.msSaveOrOpenBlob(file, filename);
    else { // Others
        const a = document.createElement("a"),
                url = URL.createObjectURL(file);
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        setTimeout(function() {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);  
        }, 0); 
    }

  }

  }
}

</script>

<style>

    body {
      overflow: hidden;
    }

    #analysis, #navbar {

      min-height: unset;
      height: 30px;

    }

    #overhang, #height {

      background-color: LightBlue;

    }

    /* BIMsurfer CSS */

    #left, #right {
        top: 0;
        bottom: 32px;            
        position: absolute;
        padding-top: 70px;
    }
    #left {
        left: 0;
        right: 75%;
        border-right: solid 1px gray;
    }
    #right {
        left: 25%;
        right: 0;
        overflow: hidden;
    }
    #left > div {
        height: 33%;
        border-bottom: solid 1px gray;
    }
    #left > div:last-child {
        height: 34%;
        border-bottom: none;
    }
    #footer {
        bottom: 0px;
        height: 30px;
        text-align: center;
        position: absolute;
        width: 100%;
        background: #eee;
        border-top: solid 1px gray;
        line-height: 24px;
    }
    #footer i, #footer span {
        vertical-align: middle;
    }
    #errors {
        display: block;
        float: right;
        padding-right: 10px;
        text-decoration: none !important;
    }
    #footer a {
        text-decoration: none;
        color: #666;
    }
    #footer a:hover {
        color: #000;
        text-decoration: underline;
    }
    #footer a i {
        font-size: 24px;
    }

</style>