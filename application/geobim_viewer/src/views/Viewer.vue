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

              
            </div>

          </div>

          <!-- <div
            class="navbar-item has-dropdown is-hoverable"
          >
            <a class="navbar-link">
              View
            </a>
            <div class="navbar-dropdown">

                <a class="navbar-item" @click="clearViewer()">
                Clear viewer
                </a>

                <a class="navbar-item" @click="hoi()">
                Show floor
                </a>

                <a class="navbar-item" @click="hoi()">
                Show all floors
                </a>
              
            </div>

          </div> -->

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

                <a class="navbar-item" @click="addGeoreferencePointSettings()">
                Add georeference point
                </a>

                <a class="navbar-item" @click="hoi()">
                Set overhang direction
                </a>

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

                <a class="navbar-item" @click="baseHeightSettings()">
                Get base height
                </a>
              
            </div>

          </div>

          <div
            class="navbar-item has-dropdown is-hoverable"
          >
            <a class="navbar-link">
              WKT
            </a>
            <div class="navbar-dropdown">

                <a class="navbar-item" @click="wktFootprintSettings">
                Write floor footprint to WKT
                </a>
              
            </div>

          </div>

          <div
            class="navbar-item has-dropdown is-hoverable"
          >
            <a class="navbar-link">
              Parking
            </a>
            <div class="navbar-dropdown">

                <a class="navbar-item" @click="parkingUnitsSettings()">
                Parking units calculation
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
          <div class="content">

            {{ modalParams.info }}

            <b-field v-for="(input, label) in modalParams.fields" v-bind:key="(input, label)" v-bind:label="label">

              <b-input v-model="modalParams.input[ input ]"></b-input>
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

export default {
  name: 'Viewer',

  props: {

    baseURL: {
      type: String,
      default: "http://127.0.0.1:81/"
      // default: "http://godzilla.bk.tudelft.nl/geobim-tool/analyse/"
    },

    filename: {
      type: String,
      default: "result"
    },

    modalParams: {

      type: Object,
      default() {

         return { "fields": {}, "title": "", "info": "", "result": "", "function": "", "input": {}, "file": false }

        }

    },

    permitParams: {

      type: Object,
      default() {

        return {}

      }

    },

    cameraParams: {

      type: Object,
      default() {

        return { "pan": 100, "rotate": 8, "zoom": 5 }

      }

    },

    availableFiles: {

      type: Array,
      default() {

        return [];

      }

    },

    georef: {

      type: Object,
      default() {

        return {
          "direction": [
            0, 
            0, 
            0
          ], 
          "location": [
            0, 
            0, 
            0
          ]
          };

      }

    }

  },

  data() {

    return {

      showModal: false,
      showFilePicker: false,
      loadedId: "",
      v: undefined

    };

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

      this.resetModalParams();
      this.loadedId = "",
      this.v = undefined;
      this.permitParams = {};

    },

    resetModalParams() {

      this.modalParams = { "fields": {}, "title": "", "info": "", "result": "", "function": "", "input": {}, "file": false };

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

  loadModel( id ) {

    fetch( this.baseURL + "/analysis/" + this.loadedId + "/getgeoref" )
      .then(function(r) { 
      
        if (r.status === 200) {

          return r.json(); 
          
        } else {

          return undefined;

        } })
      .then(function(res) {

        if (res != undefined) {
          this.georef = res;
        }

        var v = new ifcViewer({
          domNode: 'right',
          svgDomNode: 'bottom',
          modelId: id,
          withTreeVisibilityToggle: true,
          n_files: window.NUM_FILES
        });
        if (window.SPINNER_CLASS) {
            v.setSpinner({className: window.SPINNER_CLASS});
        } else if (window.SPINNER_URL) {
            v.setSpinner({url: window.SPINNER_URL});
        }
        v.load2d();
        v.load3d(this.georef);
        v.loadMetadata('middle');
        v.loadTreeView('top');

        this.v = v;
        this.v.bimSurfer3D.setCameraControls(this.cameraParams);

        if (res != undefined) {

          this.v.loadShp( "../../../../shp.js/BRK_SelectieCentrum.shp", this.georef );

        }

    }.bind( this ));

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

  heightSettings() {

    this.modalParams.title = "Get height";
    this.modalParams.function = "height";
    this.modalParams.info = "Calculates the height of the building, with the base height being the highest height of the adjacent streets.";
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

  baseHeightSettings() {

    this.modalParams.title = "Get base height";
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

    fetch( this.baseURL + "/analysis/" + this.loadedId + "/setbasefloornum/" + this.modalParams.input[ "floorNumber" ] )
      .then(function(r) { return r.text(); })
      .then(function(res) {

        console.log( res );

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
    this.modalParams.info = "";
    this.modalParams.input[ "zoneType" ] = "";
    this.modalParams.file = true;
    this.showModal = true;

  },

  parkingUnits(){

      const file = this.modalParams.file;
      const form = new FormData();
      form.append("file", file);

      // axios.post( this.baseURL + 'upload_ifc', form, {

      //     headers: {

      //       'Content-Type': 'multipart/form-data'

      //     }

      // })

      // .then( function ( res ) {

      //   const url = res.data[ 'url' ];

      //   this.poll( this.baseURL + url );

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