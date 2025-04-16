<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import MyLayout from './components/MyLayout.vue'
import LeafletMap from './components/LeafletMap.vue'
import Map from './components/Map.vue'
import Map2 from './components/Map2.vue'
import Gnv from './components/layout/Gnv.vue'
import MapControll from './components/layout/MapControll.vue'
</script>

<template>
  <!-- <Gnv /> -->
  <div class="container-fluid">
    <div class="row">
      <div class="col-2">
        <MapControll/>
      </div>
      <div class="col-10">
        <Map2 />
      
      </div>
    </div>
    </div>
  
</template>

<style scoped>
.border-coral{
  border: 2px solid coral;
}
.border-bold{
  border: 2px solid gold;
}

</style>
