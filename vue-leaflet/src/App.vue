<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import MyLayout from './components/MyLayout.vue'
import LeafletMap from './components/LeafletMap.vue'
import Map from './components/Map.vue'
import Map2 from './components/Map2.vue'
import Map3 from './components/Map3.vue'
import Gnv from './components/layout/Gnv.vue'
import MapControll from './components/layout/MapControll.vue'
const bypassControlStatus = (val: any) => {
  console.log(val)
}
const closeController = () => {
  showSidebar.value = false
}
import { ref } from 'vue'
const showSidebar = ref(false)
</script>

<template>
  <!-- <Gnv /> -->
  <div class="container-fluid" >
    <div class="row">
      <!-- <div :class="showSidebar? 'col-2' : ''" v-if="showSidebar">
        <MapControll @control-manage="bypassControlStatus" @close-controller="closeController" />
      </div> -->
      <div :class="showSidebar?'col-10' : 'col-12'">
        <Map3 />
      
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
