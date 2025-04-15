<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import MyLayout from './components/MyLayout.vue'
import LeafletMap from './components/LeafletMap.vue'
import Map from './components/Map.vue'
import Gnv from './components/layout/Gnv.vue'
</script>

<template>
  <!-- <MyLayout/> -->
  <!-- <LeafletMap /> -->
  <Gnv />
  <Map />
  
</template>

<style scoped>

</style>
