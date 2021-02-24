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
        <a
          role="button"
          class="navbar-burger"
          :class="{ 'is-active': showBurgerMenu }"
          aria-label="menu"
          aria-expanded="false"
          data-target="navMenu"
          @click="showBurgerMenu=!showBurgerMenu"
        >
          <span aria-hidden="true" />
          <span aria-hidden="true" />
          <span aria-hidden="true" />
        </a>
      </div>
      <div
        class="navbar-menu"
        :class="{ 'is-active': showBurgerMenu }"
      >
        <div class="navbar-start">
          <div class="navbar-item tags has-addons">
            <span class="tag">v0.1</span>
            <a
              class="tag is-danger"
              @click="showWelcome=true"
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
      :class="{ 'is-active' : showWelcome }"
    >
      <div class="modal-background" />
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">
            Welcome to 3D BAG v2
          </p>
          <button
            class="delete"
            aria-label="close"
            @click="showWelcome = false"
          />
        </header>
        <section class="modal-card-body">
          <div class="content">
            <p>This is a beta release of the renewed version of the 3D BAG service.</p>
            <ul>
              <li>Everything is still under development. Expect broken things.</li>
              <li>We'll release an improved version of 3DBAG once a month.</li>
              <li>
                Check the <router-link to="/docs#changelog">
                  changelog
                </router-link> for what is new.
              </li>
              <li>
                Check the <router-link to="/docs#faq">
                  FAQ
                </router-link> for a list of known issues.
              </li>
              <li>If you find another issue you can use one of the red feedback buttons to report it.</li>
              <li>You can see the attributes of a building by clicking on it.</li>
              <li>
                You can download the data by clicking on a tile on the <router-link to="/download">
                  download page
                </router-link>.
              </li>
            </ul>

            <h2 class="title is-5">
              Terms of use
            </h2>
            <ul>
              <li>Please do not publicly share or promote this website at this time.</li>
            </ul>
          </div>
        </section>
      </div>
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
