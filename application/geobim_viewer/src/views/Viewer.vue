<template>

  <div class="viewer">
    <div class="columns is-fullheight">
      <div class="column is-2 is-sidebar-menu" id="sidebar">

        <div class="file">
          <label class="file-label">
            <input class="file-input" type="file" name="resume" ref="ifcFile" @change="selectedFile">
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
// import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src

@Component({
  components: {
    ThreeViewer,
  },
})
export default class Viewer extends Vue {

  async selectedFile() {

    console.log("jep");
    const file = this.$refs.ifcFile.files[0];

    if ( !file || file.name.slice(-4) != ".ifc" ) {

      alert( "Please choose an IFC file!" );
      return;

    }

    const form = new FormData();
    form.append("file", file);

    axios.post('http://127.0.0.1:5000/upload_ifc', form, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
    })
    .then(console.log)
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

</style>