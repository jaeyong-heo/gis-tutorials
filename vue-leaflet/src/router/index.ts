import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import BusView from '@/views/BusView.vue'
import DeckTrip from '@/views/deck/DeckTrip.vue'
import Map3 from '@/views/Map3.vue'
import DeckArc from '@/views/deck/DeckArc.vue'
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
      name: 'deck-trip',
      component: DeckTrip,
    },
    {
      path: '/deck/deck-arc',
      name: 'deck-arc',
      component: DeckArc,
    },
    {
      path: '/map3',
      name: 'map3',
      component: Map3,
    },
  ],
})

export default router
