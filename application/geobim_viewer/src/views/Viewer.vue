<template>
  <div class="viewer">
    <ThreeViewer
      ref="threeviewer"
    />
  </div>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';
import ThreeViewer from '@/components/ThreeViewer.vue';
// import HelloWorld from '@/components/HelloWorld.vue'; // @ is an alias to /src

@Component({
  components: {
    ThreeViewer,
  },
})
export default class Viewer extends Vue {}
</script>
