import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BusView from '@/views/BusView.vue'
import DeckTrip from '@/views/deck/DeckTrip.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: '/bus',
      name: 'bus',
      component: BusView,
    },
    {
      path: '/deck/deck-trip',
      name: 'bus',
      component: DeckTrip,
    },
  ],
})

export default router
