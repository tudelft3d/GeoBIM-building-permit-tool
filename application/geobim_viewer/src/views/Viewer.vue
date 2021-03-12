<template>

  <div class="viewer">
    
    <div class="columns is-fullheight">
      <div class="column is-2 is-sidebar-menu" id="sidebar">


      </div>


      <div class="column is-main-content">

            <nav
      class="navbar is-light is-size-7"
      role="navigation"
      aria-label="flask navigation"
    >

      <div
        class="navbar-menu"
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

                <a class="navbar-item" @click="overhangSingle()">
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

                <a class="navbar-item" @click="wkt()">
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


      </div>
    </nav>

        <ThreeViewer
          ref="threeviewer"
        />

      </div>
    </div>
  </div>
</template>

<script lang="ts">

import { Component, Vue } from 'vue-property-decorator';
import ThreeViewer from '@/components/ThreeViewer.vue';
import axios from 'axios';
import VueSimpleAlert from "vue-simple-alert";

Vue.use(VueSimpleAlert);

@Component({
  components: {
    ThreeViewer
  },
})

export default class Viewer extends Vue {

  baseURL = "http://127.0.0.1:5000/";

  poll( url: string ) {

    fetch( url )

    .then(function(r) { return r.json(); })

    .then(function(r: any) {

      if ( r.progress === 100 ) {

        const split = url.split( "/" );
        const id = split[ split.length - 1 ];
        
        this.getModelInfo( id );

        return;

      }

      setTimeout( () => {

        console.log( r.progress );

        this.poll( url );

      }, 1000);

    }.bind( this ));

  }

  hoi() {
    console.log("hoi");
  }

  async wkt() {

      const values = await this.$fire({

        title: 'Footprint WKT',
        html:
          '<input id="swal-input1" class="swal2-input" placeholder="Floor number">' +
          '<input id="swal-input2" class="swal2-input" placeholder="Output file name">',
        focusConfirm: false,
        preConfirm: () => {
          return {
            "floor": document.getElementById('swal-input1').value,
            "filename": document.getElementById('swal-input2').value
          }
        }
        
    })

    fetch( this.baseURL + "/analysis/" + "/wkt/" + values.value.floor )
      .then(function(r) { return r.json(); })
      .then(function(res: any) {

        console.log( res.wkt );

        this.downloadFile( res.wkt, values.value.filename, "text/plain")

    }.bind( this ));

  }

  async overhangSingle() {

    const values = await this.$fire({

      title: 'Footprint WKT',
      html:
        '<input id="swal-input1" class="swal2-input" placeholder="Floor number">' +
        '<input id="swal-input2" class="swal2-input" placeholder="Output file name">',
      focusConfirm: false,
      preConfirm: () => {
        return {
          "floor": document.getElementById('swal-input1').value,
          "filename": document.getElementById('swal-input2').value
        }
      }
        
    })

    fetch( this.baseURL + "/analysis/" + "/overhangsingle/" + values.value.floor )
      .then(function(r) { return r.json(); })
      .then(function(res: any) {

        console.log( res );

        // this.downloadFile( res.wkt, values.value.filename, "text/plain")

    }.bind( this ));


  }

  downloadFile( data: any, filename: string, type: string ) {

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

  getModelInfo( id: string ) {

    const url = this.baseURL + "/v/" + id;
    console.log( url );

    fetch( this.baseURL + "/log/" + id + ".json" )
    .then(function(r) { return r.text(); })
    .then(function(log) {

      // console.log( log );

    });

    const glbUrl = this.baseURL + "/m/" + id + "_0.glb"

    this.$refs.threeviewer.loadglTF( glbUrl );


  }

  async selectedFile() {

    console.log(this.$refs.ifcFiles);

    const files: any = this.$refs.ifcFiles; 
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

    .then( function ( res: any ) {

      const url = res.data[ 'url' ];

      this.poll( this.baseURL + url );

    }
    
    .bind( this ))
    .catch(console.error);

  }



}

</script>

<style scoped>

#sidebar {

  height: 100vh;
  padding: 20px;
  border-style: solid;
  border-width: 1px;

}

.navbar {
  min-height: unset;
  max-height: 2rem !important;
}

</style>