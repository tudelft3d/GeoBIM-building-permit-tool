import Vue from 'vue';
import Buefy from 'buefy';
import '@/styles/bulma.scss';
import router from './router';
import App from './App.vue';
import vuetify from './plugins/vuetify';

Vue.config.productionTip = false;
Vue.use(Buefy);

new Vue({
  router,
  vuetify,
  render: (h) => h(App)
}).$mount('#app');
