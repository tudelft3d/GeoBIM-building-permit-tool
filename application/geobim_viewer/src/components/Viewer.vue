<template>

    <div id='toolbar'>

    </div>

</template>

<script>

export default {
  name: 'Viewer',
  props: {
    msg: String
  },
  beforeCreate() {

    console.log("hoi");

  },
  mounted() {

  },

  methods: {

    hoi() {
      console.log(v);
      v.load2d();
      v.load3d();
      v.loadMetadata('middle');
      v.loadTreeView('top');
    }

  }
}
</script>

