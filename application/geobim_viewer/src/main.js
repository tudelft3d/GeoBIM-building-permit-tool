import Vue from 'vue';
import './styles/bulma.scss';
import App from './App.vue';
import router from './router'

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')