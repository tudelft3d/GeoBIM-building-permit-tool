import Vue from 'vue';
import Buefy from 'buefy';
import '@/styles/bulma.scss';
import router from './router';
import App from './App.vue';

Vue.config.productionTip = false;
Vue.use(Buefy);

new Vue({
  router,
  render: (h) => h(App),
}).$mount('#app');
