<template>
  <div id="app">
    <nav
      class="navbar is-fixed-top is-white has-shadow"
      role="navigation"
      aria-label="dropdown navigation"
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
        <div class="navbar-start">
          <div class="navbar-item">
          <span class="logo-text">GeoBIM Tool</span>
          </div>
          <div class="navbar-item tags has-addons">
            
            <span class="tag">v2.0</span>
            <div
              class="tag is-blue"
            >beta</div>
          </div>
        </div>
        <div class="navbar-end">
          <router-link
            to="/viewer"
            active-class="is-active"
            class="navbar-item"
          >
            Viewer
          </router-link>
          <router-link
            to="/documentation"
            active-class="is-active"
            class="navbar-item"
          >
            Documentation
          </router-link>
          <router-link
            to="/github"
            active-class="is-active"
            class="navbar-item"
          >
            Repository
          </router-link>
        </div>
      </div>
    </nav>
    <div
      class="modal"
    >
    </div>
    <router-view />
  
  </div>
</template>

<script>
export default {
  data() {
    return {
      open: false,
      overlay: false,
      fullheight: true,
      fullwidth: false,
    };
  }
};
</script>

<style>

#app {

  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 3.25rem 0 0 0;

}


</style>
