import Vue from 'vue'
import VueRouter from 'vue-router'
import Viewer from '../views/Viewer.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect: '/viewer',
  },
  {
    path: '/viewer',
    name: 'Viewer',
    component: Viewer,
  },
  {
    path: '/documentation',
    name: 'Documentation',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/Documentation.vue'),
  },
  {
    path: '/github',
    beforeEnter() {location.href = 'https://github.com/jliempt/ifc-pipeline'}
}
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
