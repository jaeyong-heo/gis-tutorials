<template>
    <div id="map"></div>
    zoomLevel({{ userMK.zoom }})
    <button @click="info">info</button>
    <button @click="printBound">print bound</button>
    <input type:number ref="busnum"><button @click="getBus(busnum)">bus</button>
</template>

<script setup lang="ts">
import { ref, watch  } from "vue";
import leaflet, { bounds } from "leaflet"
import { onMounted, watchEffect } from "vue";
import { useGeolocation } from '@vueuse/core'
import { userMarker, nearbyMarker, useMapStore } from "@/stores/mapStore"
import {convertToGeoJSON} from "@/composables/geoJsonConvert.ts"
import { storeToRefs } from "pinia";
import crosswalk from "@/assets/crosswalk.json"
// import hangjeongdong_seoul from "@/assets/hangjeongdong_seoul.geojson"




// Values and types.
import {LeafletLayer} from 'deck.gl-leaflet';
import DeckGL from '@deck.gl/react';
import {GeoJsonLayer} from '@deck.gl/layers';
import {MapView} from '@deck.gl/core';
// Types only.
import type {DeckGLRef} from '@deck.gl/react';
import type {GeoJsonLayerProps} from '@deck.gl/layers';

const {userMK, controlStatus} = storeToRefs(useMapStore());
const busnum = ref(0);
const info =() =>{
    console.log("======== leaflet ======== ")
    console.log(leaflet.version); // 1.9.4
    console.log(leaflet);
    const userMKVar = userMK.value;
    console.log('userMKVar', userMKVar);
}

let map: leaflet.Map;

let userGeoMaker: leaflet.Marker;
let geojsonLayers= {} as any; // { layerName: layerObject }
const { coords, locatedAt, error, resume, pause } = useGeolocation()
console.log(coords.value.latitude, coords.value.longitude)

onMounted(()=>{

    map = leaflet
    .map('map')
    .setView([userMarker.value.latitude, userMarker.value.longtitude ], userMK.value.zoom);

    
    // Control options
    map.zoomControl.remove(); // 줌 컨트롤 제거

    // =================================================== 레이어어 적용 ===================================================
    // var littleton = leaflet.marker(makeRandomPosition(userMarker.value.latitude, userMarker.value.longtitude)).bindPopup('This is Littleton, CO.'),
    // denver    = leaflet.marker(makeRandomPosition(userMarker.value.latitude, userMarker.value.longtitude)).bindPopup('This is Denver, CO.'),
    // aurora    = leaflet.marker(makeRandomPosition(userMarker.value.latitude, userMarker.value.longtitude)).bindPopup('This is Aurora, CO.'),
    // golden    = leaflet.marker(makeRandomPosition(userMarker.value.latitude, userMarker.value.longtitude)).bindPopup('This is Golden, CO.');

    // var cities = leaflet.layerGroup([littleton, denver, aurora, golden]);

    // var osm = leaflet.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    //     maxZoom: 19,
    //     attribution: '© OpenStreetMap'
    // });

    // var osmHOT = leaflet.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    //     maxZoom: 19,
    //     attribution: '© OpenStreetMap contributors, Tiles style by Humanitarian OpenStreetMap Team hosted by OpenStreetMap France'});

    // map = leaflet.map('map', {
    //     center: [userMarker.value.center[0], userMarker.value.center[1]],
    //     zoom: 10,
    //     layers: [osm, cities]
    // });

    // var baseMaps = {
    //     "OpenStreetMap": osm,
    //     "OpenStreetMap.HOT": osmHOT
    // };

    // var overlayMaps = {
    //     "Cities": cities
    // };

    // var layerControl = leaflet.control.layers(baseMaps, overlayMaps).addTo(map);
    
    // var crownHill = leaflet.marker(makeRandomPosition(userMarker.value.latitude, userMarker.value.longtitude)).bindPopup('This is Crown Hill Park.'),
    //     rubyHill = leaflet.marker(makeRandomPosition(userMarker.value.latitude, userMarker.value.longtitude)).bindPopup('This is Ruby Hill Park.');
        
    // var parks = leaflet.layerGroup([crownHill, rubyHill]);
    // var openTopoMap = leaflet.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    //     maxZoom: 19,
    //     attribution: 'Map data: © OpenStreetMap contributors, SRTM | Map style: © OpenTopoMap (CC-BY-SA)'
    // });

    // layerControl.addBaseLayer(openTopoMap, "OpenTopoMap");
    // layerControl.addOverlay(parks, "Parks");


    // =================================================== 타일 적용 ===================================================
    leaflet.tileLayer(import.meta.env.VITE_TILE_LAYER_URL, {
        attribution: import.meta.env.VITE_TILE_ATTRIVUTION
    }).addTo(map);
    
    
    // 줌 변화 감지
    map.on('zoomend', () => {
        userMK.value.zoom = map.getZoom()
    })

    // 지도 이동(팬, 줌 등) 변화 감지
    map.on('moveend', () => {
        const c = map.getCenter()
        userMK.value.center = [c.lat, c.lng]
        // console.log(`${c.lat}, ${c.lng}`)
        updateBounds()
    })

    if(userGeoMaker){
        map.removeLayer(userGeoMaker)
    }
    userGeoMaker  = leaflet.marker([userMarker.value.latitude, userMarker.value.longtitude]).addTo(map).bindPopup("You are here!").openPopup();

    const crosswalkGeojson: any = convertToGeoJSON(crosswalk);
    // 횡단보도 geojson 데이터 출력
    // leaflet.geoJSON(crosswalkGeojson).addTo(map);

    
    // printSubwayExit()


    


})

const makeRandomPosition = (lat: number, lng: number): [number, number] =>{
    const latOffset = Math.random() * 0.01 - 0.005; // -0.005 ~ 0.005
    const lngOffset = Math.random() * 0.01 - 0.005; // -0.005 ~ 0.005

    return [lat + latOffset, lng + lngOffset];
}

function updateBounds() {
    const b = map.getBounds()
    const bounds = {
      northWest: [b.getNorthWest().lat, b.getNorthWest().lng] as [number, number],
      northEast: [b.getNorthEast().lat, b.getNorthEast().lng] as [number, number],
      southWest: [b.getSouthWest().lat, b.getSouthWest().lng] as [number, number],
      southEast: [b.getSouthEast().lat, b.getSouthEast().lng] as [number, number],
    }

    console.log(bounds)

    userMK.value.bound = bounds;
    
  }

const getBus = async (busRouteId: number) => {
    const result = await fetch(`http://localhost:8000/bus-pos?busRouteId=${busRouteId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    const bus = result;
    console.log(`busRouteId: ${busRouteId}`)
    console.log(bus)

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
const getGeoJsonSample = async () => {
    const response = await fetch("/src/assets/hangjeongdong_seoul.geojson")
    const geojson = await response.json()
    return geojson
}
const printSeoulDepartment = async () => {
    const response = await fetch("/src/assets/hangjeongdong_seoul.geojson")
    const geojson = await response.json()
    leaflet.geoJSON(geojson).addTo(map);
    // geojsonLayers
    const seoulLayer = leaflet.geoJSON(geojson, {
        style: { color: 'blue', weight: 1},
        onEachFeature: (feature, layer) => {
            const name = feature.properties.adm_nm
            layer.bindPopup(`<b>${name}</b>`)
        },
    }).addTo(map)

    geojsonLayers.hangjeongdong_seoul = seoulLayer
    
    leaflet.control.layers(null,  seoulLayer, { collapsed: false }).addTo(map)
    
}

const getColor = (val: string) => {
    const d = Number(val)%5;
     
    return d == 0 ? '#800026' :
           d == 1 ? '#BD0026' :
           d == 2 ? '#E31A1C' :
           d == 3 ? '#E31A1C' :
           '#E31A1C';
}

const printSubwayExit = async () => {
    const response:any = await fetch("/src/assets/tnSubwayEntrc.csv")
    
    const headers = response.slice(0, response.indexOf("\n")).split(",");
    const rows = response.slice(response.indexOf("\n") + 1).split("\n");

    console.log(headers)
    console.log()
    console.log(rows)
}

watchEffect(()=>{
    if(coords.value.latitude !== Number.POSITIVE_INFINITY && coords.value.longitude !== Number.POSITIVE_INFINITY){
        userMarker.value.latitude = coords.value.latitude;
        userMarker.value.longtitude = coords.value.longitude;
        userMK.value.latitude = coords.value.latitude;
        userMK.value.longtitude = coords.value.longitude;
    }
})

watch(
  controlStatus,
  () => {
    if(controlStatus.value.status1){
        printSeoulDepartment()
    }else{
        map.removeLayer(geojsonLayers.hangjeongdong_seoul)
    }



    if(controlStatus.value.status2){
        alert('ddd')
    }else{
        
    }

  },
  { deep: true }
);

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