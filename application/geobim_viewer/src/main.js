import Vue from 'vue';
import Buefy from 'buefy';
import './styles/bulma.scss';
import App from './App.vue';
import router from './router'

Vue.config.productionTip = false
Vue.use(Buefy);

new Vue({
  router,
  render: h => h(App)
}).$mount('#app')