<template>
    <div id="map"></div>
    zoomLevel({{ userMK.zoom }})
    <button @click="info">info</button>
    <button @click="printBound">print bound</button>
</template>

<script setup lang="ts">
import { ref, watch  } from "vue";
import leaflet, { bounds } from "leaflet"
import { onMounted, watchEffect } from "vue";
import { useGeolocation } from '@vueuse/core'
import { userMarker, nearbyMarker, useMapStore } from "@/stores/mapStore"
import crosswalk from "@/assets/crosswalk.json"
import {convertToGeoJSON} from "@/composables/geoJsonConvert.ts"
import { storeToRefs } from "pinia";

const {userMK} = storeToRefs(useMapStore());

const info =() =>{
    console.log("======== leaflet ======== ")
    console.log(leaflet.version); // 1.9.4
    console.log(leaflet);
    const userMKVar = userMK.value;
    console.log('userMKVar', userMKVar);
    

}
let map: leaflet.Map;
let userGeoMaker: leaflet.Marker;
const { coords, locatedAt, error, resume, pause } = useGeolocation()
console.log(coords.value.latitude, coords.value.longitude)

onMounted(()=>{
    
    map = leaflet
    .map('map')
    .setView([userMarker.value.latitude, userMarker.value.longtitude ], userMK.value.zoom);

    
    // Control options
    map.zoomControl.remove(); // 줌 컨트롤 제거



    // =================================================== 타일 적용 ===================================================
    // 기본 타일
    // leaflet.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //     maxZoom: 19,
    //     attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    // }).addTo(map);

    // vworld 타일
    leaflet.tileLayer('https://xdworld.vworld.kr/2d/Base/service/{z}/{x}/{y}.png', {
        attribution: '© <a href="http://www.vworld.kr/">vworld</a> contributors'
    }).addTo(map);


    // 줌 변화 감지
    map.on('zoomend', () => {
        userMK.value.zoom = map.getZoom()
    })

    // 지도 이동(팬, 줌 등) 변화 감지
    map.on('moveend', () => {
        const c = map.getCenter()
        userMarker.value.center = [c.lat, c.lng]
        // console.log(`${c.lat}, ${c.lng}`)
        updateBounds()
    })

    if(userGeoMaker){
        map.removeLayer(userGeoMaker)
    }
    userGeoMaker  = leaflet.marker([userMarker.value.latitude, userMarker.value.longtitude]).addTo(map).bindPopup("You are here!").openPopup();

    const crosswalkGeojson: any = convertToGeoJSON(crosswalk);
    leaflet.geoJSON(crosswalkGeojson).addTo(map);
})

function updateBounds() {
    const b = map.getBounds()
    const bounds = {
      northWest: [b.getNorthWest().lat, b.getNorthWest().lng] as [number, number],
      northEast: [b.getNorthEast().lat, b.getNorthEast().lng] as [number, number],
      southWest: [b.getSouthWest().lat, b.getSouthWest().lng] as [number, number],
      southEast: [b.getSouthEast().lat, b.getSouthEast().lng] as [number, number],
    }

    console.log(bounds)

    userMarker.value.bound = bounds;
    
  }

const printBound = () => {
    const b = map.getBounds()
    console.log(userMarker.value.bound)
    console.log(typeof userMarker.value.bound)
    leaflet.polygon(
        [
            userMarker.value.bound.northWest,
            userMarker.value.bound.northEast,
            userMarker.value.bound.southEast,
            userMarker.value.bound.southWest,
        ]
    , {
        color: 'green',
        fillColor: 'gold',
        fillOpacity: 0.5
    }).addTo(map);
}



watchEffect(()=>{
    if(coords.value.latitude !== Number.POSITIVE_INFINITY && coords.value.longitude !== Number.POSITIVE_INFINITY){
        userMarker.value.latitude = coords.value.latitude;
        userMarker.value.longtitude = coords.value.longitude
    }
})



</script>

<style scoped>
#map {
    height: 100vh;
    width: 100%;
    /* position: absolute; */
    /* top: 0;
    right: 0; */
}
</style>