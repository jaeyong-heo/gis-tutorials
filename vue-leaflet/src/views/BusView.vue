<template>
    zoomLevel({{ userMK.zoom }})
    <button @click="printBound">print bound</button>
    <input type:number ref="busnum" value="100100062"><button @click="getBus(busnum)">bus</button>
    <div id="map"></div>
    currentTime: {{ currentTime }}<br>
    <button @click="startPolling">startPolling</button>
    
</template>

<script setup lang="ts">

interface BusLocationData {
  sectOrd: string;       // 구간 순번
  sectDist: string;      // 구간 거리 (단위 미상)
  stopFlag: string;      // 정차 여부 (0: 주행중, 1: 정차)
  sectionId: string;     // 구간 ID
  dataTm: string;        // 데이터 수신 시각 (yyyymmddHHMMss 형식)
  tmX: string;           // 중심점 X 좌표 (WGS84 경도)
  tmY: string;           // 중심점 Y 좌표 (WGS84 위도)
  posX: string;          // 실시간 위치 X 좌표 (TM 기준)
  posY: string;          // 실시간 위치 Y 좌표 (TM 기준)
  vehId: string;         // 차량 ID
  plainNo: string;       // 차량 번호판
  busType: string;       // 버스 유형 (예: 1: 일반형, 2: 저상형 등)
  routeId: string;       // 노선 ID
  lastStnId: string;     // 최근 정류소 ID
  isFullFlag: string;    // 만차 여부 (0: 여유, 1: 혼잡)
  congetion: string;     // 혼잡도 (0~3 범위 추정)
}


import { ref, watch  } from "vue";
import leaflet, { bounds } from "leaflet"
import { onMounted, watchEffect, onBeforeMount } from "vue";
import { timestamp, useGeolocation } from '@vueuse/core'
import { userMarker, useMapStore } from "@/stores/mapStore"
import { storeToRefs } from "pinia";

import {LeafletLayer} from 'deck.gl-leaflet';
import {MapView} from '@deck.gl/core';
import {Deck} from '@deck.gl/core';
import {TripsLayer} from '@deck.gl/geo-layers';
import { animate } from 'popmotion' 



const {userMK, controlStatus} = storeToRefs(useMapStore());
const busnum = ref(0);

const map = ref<leaflet.Map | null>(null);
const markerLayer = ref(leaflet.layerGroup());

// 애니메이션 조절
const currentTime = ref(100);
const animationSpeed = ref(10); // 10ms 씩 증가, 조절 가능
const loopLength = ref(6000);   // 데이터 타임스탬프 범위에 맞춰 설정
let animationInstance: any = null

const tripData = ref(
[]
// [
//   {
//     "waypoints": [
//       { "coordinates": [126.9751, 37.5759], "timestamp": 1554772579000 },
//       { "coordinates": [126.9755, 37.5761], "timestamp": 1554772579009 },
//       { "coordinates": [126.9768, 37.5763], "timestamp": 1554772579054 },
//       { "coordinates": [126.9783, 37.5765], "timestamp": 1554772579092 },
//       { "coordinates": [126.9807, 37.5772], "timestamp": 1554772579345 },
//       { "coordinates": [126.9819, 37.5768], "timestamp": 1554772579402 },
//       { "coordinates": [126.9828, 37.5774], "timestamp": 1554772579462 },
//       { "coordinates": [126.9845, 37.5771], "timestamp": 1554772579563 },
//       { "coordinates": [126.9869, 37.5776], "timestamp": 1554772579880 },
//       { "coordinates": [126.9887, 37.5782], "timestamp": 1554772580070 },
//       { "coordinates": [126.9894, 37.5789], "timestamp": 1554772580117 },
//       { "coordinates": [126.9898, 37.5792], "timestamp": 1554772580120 },
//       { "coordinates": [126.9907, 37.5797], "timestamp": 1554772580127 },
//       { "coordinates": [126.9909, 37.5799], "timestamp": 1554772580130 },
//       { "coordinates": [126.9893, 37.5804], "timestamp": 1554772580166 },
//       { "coordinates": [126.9891, 37.5802], "timestamp": 1554772580176 },
//       { "coordinates": [126.9891, 37.5800], "timestamp": 1554772580181 },
//       { "coordinates": [126.9894, 37.5798], "timestamp": 1554772580186 },
//       { "coordinates": [126.9896, 37.5791], "timestamp": 1554772580200 }
//     ]
//   }
// ]
)

// featureGroup 
const featureGroup = ref<leaflet.FeatureGroup>();

let userGeoMaker: leaflet.Marker;
let geojsonLayers= {} as any; // { layerName: layerObject }
const { coords } = useGeolocation()
console.log(coords.value.latitude, coords.value.longitude)
const tileRef = ref();
const attribution = ref();

const deckLayer = ref<LeafletLayer>();
const deckInstance = ref();

onBeforeMount(() => {
    tileRef.value = import.meta.env.VITE_TILE_LAYER_URL;
    attribution.value = import.meta.env.VITE_TILE_ATTRIVUTION;
})
onMounted(() => {

    console.log("======== leaflet ======== ")
    // leaflet 기본 그리기
    if(!map.value){ // map이 아직 초기화되지 않았다면
        map.value = leaflet
        .map('map')
        .setView([userMarker.value.latitude, userMarker.value.longtitude], userMK.value.zoom);

        map.value.zoomControl.remove();

        map.value.on('zoomend', () => {
            userMK.value.zoom = map.value?.getZoom() ?? userMK.value.zoom;
        });

        map.value.on('moveend', () => {
            const c = map.value?.getCenter();
            if (c) {
                userMK.value.center = [c.lat, c.lng];
                updateBounds();
            }
        });

        leaflet.tileLayer(tileRef.value, {
            attribution: attribution.value
        }).addTo(map.value!);

        
        if (userGeoMaker) {
            map.value.removeLayer(userGeoMaker);
        }
        
    }
});





function updateBounds() {
    const b = map?.value?.getBounds();
    if (!b) {
      console.warn("Bounds are undefined.");
      return;
    }
    const bounds = {
      northWest: [b.getNorthWest().lat, b.getNorthWest().lng] as [number, number],
      northEast: [b.getNorthEast().lat, b.getNorthEast().lng] as [number, number],
      southWest: [b.getSouthWest().lat, b.getSouthWest().lng] as [number, number],
      southEast: [b.getSouthEast().lat, b.getSouthEast().lng] as [number, number],
    }

    console.log(bounds)

    userMK.value.bound = bounds;
    
  }
const vehList = ref([]);
const firstBusTime = ref(0);

const getBus = async (busRouteId: any) => {
    const busNum = Number(busRouteId)
    const response = await fetch(`http://localhost:7080/bus-pos?busRouteId=${busNum}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    const result = await response.json();
    const busList = result?.msgBody?.itemList as BusLocationData[];

    console.log(`busRouteId: ${busNum}`)
    console.log(busList)
    busList.forEach((bus: BusLocationData) => {
        if(firstBusTime.value === 0){
            firstBusTime.value = new Date(bus.dataTm).getTime();
        }

        const existing = tripData.value.find((t: any) => t.vehId === bus.vehId);

        if (existing) {
            // 기존 vehId가 있으면 waypoints에 push
            existing.waypoints.push({
            coordinates: [Number(bus.tmY), Number(bus.tmX)],
            timestamp
            });
        } else {
            // 없으면 새 객체 추가
            tripData.value.push({vehId: bus.vehId,coordinates: [Number(bus.tmY), Number(bus.tmX)], timestamp: bus.dataTm  });
        }
        
    })

    console.log('-- tripData.value -- ')
    console.log(tripData.value)

    //////////////// LeafletLayer - TripsLayer /////////////////////////
    const deckLayer = new LeafletLayer({
    layers: [
        new TripsLayer({
            id: 'TripsLayer',
            data: tripData.value,
            getPath: (d: any) => d.waypoints.map((p: { coordinates: [number, number] }) => p.coordinates),
            getTimestamps: (d: any) => d.waypoints.map((p: { timestamp: number }) => p.timestamp - 1554772579000),
            getColor: [253, 128, 93],
            currentTime: 500,
            trailLength: 600,
            capRounded: true,
            jointRounded: true,
            widthMinPixels: 8
        })
    ]
    });
    
    if (map.value) {
        map.value.removeLayer(deckLayer);
    }
    
}  

let polling = true;
const startPolling = async () =>{
  const poll = async () => {
    if (!polling) return;
    
    await getBus('100100062');
    setTimeout(poll, 10000); // 반복 주기 10000으로 설정
  };
  poll();
}


const getGeoJsonSample = async () => {
    const response = await fetch("/src/assets/hangjeongdong_seoul.geojson")
    const geojson = await response.json()
    return geojson
}
const printSeoulDepartment = async () => {
    const response = await fetch("/src/assets/hangjeongdong_seoul.geojson")
    const geojson = await response.json()
    leaflet.geoJSON(geojson).addTo(map.value as any);
    // geojsonLayers
    const seoulLayer = leaflet.geoJSON(geojson, {
        style: { color: 'blue', weight: 1},
        onEachFeature: (feature, layer) => {
            const name = feature.properties.adm_nm
            layer.bindPopup(`<b>${name}</b>`)
        },
    }).addTo(map.value as leaflet.Map);

    geojsonLayers.hangjeongdong_seoul = seoulLayer
    
    leaflet.control.layers(null,  seoulLayer, { collapsed: false }).addTo(map.value as leaflet.Map);
    
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
        map.value.removeLayer(geojsonLayers.hangjeongdong_seoul)
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
    height: 80vh;
    width: 100%;
    /* position: absolute; */
    /* top: 0;
    right: 0; */
}
</style>