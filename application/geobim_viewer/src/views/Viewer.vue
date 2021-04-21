<template>

  <div id="analysis">
    
      <nav
      class="navbar is-light is-size-7"
      role="navigation"
      aria-label="flask navigation"
      id="navbartje"
    >
      
          <div
            class="navbar-item has-dropdown is-hoverable"
          >
            <a class="navbar-link">
              File
            </a>
            <div class="navbar-dropdown">
              <a class="navbar-item">

                <input class="file-input" type="file" ref="ifcFiles" @change="selectedFile">
                Upload IFC

              </a>

              <a class="navbar-item" @click="hoi()">
                Pick
              </a>
              
            </div>

          </div>

          <div
            class="navbar-item has-dropdown is-hoverable"
          >
            <a class="navbar-link">
              View
            </a>
            <div class="navbar-dropdown">

                <a class="navbar-item" @click="hoi()">
                Clear viewer
                </a>

                <a class="navbar-item" @click="hoi()">
                Show floor
                </a>

                <a class="navbar-item" @click="hoi()">
                Show all floors
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

                <a class="navbar-item" @click="hoi()">
                Set base floor number
                </a>

                <a class="navbar-item" @click="hoi()">
                Add georeference point
                </a>

                <a class="navbar-item" @click="hoi()">
                Set overhang direction
                </a>

                <a class="navbar-item" @click="hoi()">
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

                <a class="navbar-item" @click="hoi()">
                Single floor overlap
                </a>

                <a class="navbar-item" @click="hoi()">
                Single floor overlap bounding box
                </a>

                <a class="navbar-item" @click="hoi()">
                All floors overlap
                </a>

                <a class="navbar-item" @click="hoi()">
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

                <a class="navbar-item" @click="hoi()">
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

                <a class="navbar-item" @click="hoi()">
                Height
                </a>

                <a class="navbar-item" @click="hoi()">
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

                <a class="navbar-item" @click="hoi()">
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
            @click="showModal = false"
          />
        </header>
        <section class="modal-card-body">
          <div class="content">

            {{ modalParams.info }}

            <b-field v-for="(input, label) in modalParams.fields" v-bind:key="(input, label)" v-bind:label="label">

              <b-input v-model="modalParams.input[ input ]"></b-input>
            </b-field>

            <b-field label="Result">
              <textarea class="textarea" :value="modalParams.result"></textarea>
            </b-field>

            <div class="buttons">
              <b-button type="is-light" @click="analysisCall(modalParams.function)">OK</b-button>
              <b-button type="is-light" v-if="modalParams.result.length != 0" @click="downloadFile">Save result</b-button>
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
      default: "http://godzilla.bk.tudelft.nl/geobim-tool/analyse"
    },

    filename: {
      type: String,
      default: "result.txt"
    },

    modalParams: {

      type: Object,
      default() {

         return { "fields": {}, "title": "", "info": "", "result": "", "function": "", "input": {} }

        }

    }

  },

  data() {

    return {

      showModal: false

    };

  },

  methods: {

    poll( url ) {

      fetch( url )

      .then(function(r) { return r.json(); })

      .then(function(r) {

        if ( r.progress === 100 ) {

          const split = url.split( "/" );
          const id = split[ split.length - 1 ];
          
          this.loadModel( id );

          return;

        }

        setTimeout( () => {

          console.log( r.progress );

          this.poll( url );

        }, 1000);

      }.bind( this ));

    },

  async selectedFile() {

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

      this.poll( this.baseURL + url );

    }
    
    .bind( this ))
    .catch(console.error);

  },

    loadModel( id ) {

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
    v.load3d();
    v.loadMetadata('middle');
    v.loadTreeView('top');


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

      fetch( this.baseURL + "/analysis/" + "/wkt/" + this.modalParams.input[ "floorNumber" ] )
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
    this.modalParams.info = "";
    this.modalParams.input[ "floorNumber" ] = "";
    this.showModal = true;

  },

  overhangSingle() {

    fetch( this.baseURL + "/analysis/" + "/overhangsingle/" + this.modalParams.input[ "floorNumber" ] )
      .then(function(r) { return r.json(); })
      .then(function(res) {

        console.log( res );
        this.modalParams.result = "floorname: " + res.floorname + "\n" + "low_overhang: " + res.low_overhang + "\n" + "up_overhang: " + res.up_overhang;

    }.bind( this ));

  },

  downloadFile() {

    const data = this.modalParams.result;
    const filename = this.filename;
    const type = "text/plain";

    const file = new Blob([data], {type: type});
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

    #analysis, #navbartje {

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