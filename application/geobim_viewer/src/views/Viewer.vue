<template>

  <div class="viewer">

    <nav
      class="navbar is-light is-size-7"
      role="navigation"
      aria-label="flask navigation"
    >
      <div class="navbar-brand">
        <router-link
          to="/viewer"
          class="navbar-item"
        >
        </router-link>
      </div>
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
              <label class="file-label">
                <input class="file-input" type="file" name="resume" ref="ifcFiles" @change="selectedFile">

                Upload IFC
                </label>

                <a class="navbar-item" @click="hoi()">
                Pick
                </a>
              
            </div>

          </div>

          <div
            class="navbar-item has-dropdown is-hoverable"
          >
            <a class="navbar-link">
              File
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

                <a class="navbar-item" @click="hoi()">
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

                <a class="navbar-item" @click="hoi()">
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
    
    <div class="columns is-fullheight">
      <div class="column is-2 is-sidebar-menu" id="sidebar">

        <div class="file">
          <label class="file-label">
            <input class="file-input" type="file" name="resume" ref="ifcFiles" @change="selectedFile">
            <span class="file-cta">
              <span class="file-label">
                Upload IFC
              </span>
            </span>
          </label>
        </div>

      </div>



      <div class="column is-main-content">
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