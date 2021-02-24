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
          <div class="navbar-item tags has-addons">
            <span class="tag">v0.1</span>
            <a
              class="tag is-danger"
            >beta</a>
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

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
