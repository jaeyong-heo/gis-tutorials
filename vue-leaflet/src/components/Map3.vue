<template>
    <div id="map"></div>
    zoomLevel({{ userMK.zoom }})
    <button @click="info">info</button>
    <button @click="printBound">print bound</button>
    <input type:number ref="busnum"><button @click="getBus(busnum)">bus</button>
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
import leaflet from "leaflet"
import "leaflet-draw"
import "leaflet-draw/dist/leaflet.draw.css"
import { onMounted, watchEffect, onBeforeMount } from "vue";
import { useGeolocation } from '@vueuse/core'
import { userMarker, useMapStore } from "@/stores/mapStore"
import {convertToGeoJSON} from "@/composables/geoJsonConvert.ts"
import { storeToRefs } from "pinia";
import crosswalk from "@/assets/crosswalk.json"
// import hangjeongdong_seoul from "@/assets/hangjeongdong_seoul.geojson"
import {useGeom} from "@/composables/useGeom.ts"

// Values and types.
// Types only.

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
const tileRef = ref();
const attribution = ref();
onBeforeMount(() => {
    tileRef.value = import.meta.env.VITE_TILE_LAYER_URL;
    attribution.value = import.meta.env.VITE_TILE_ATTRIVUTION;
})
onMounted(()=>{

    map = leaflet
    .map('map')
    .setView([userMarker.value.latitude, userMarker.value.longtitude ], userMK.value.zoom);
    
    // Control options
    map.zoomControl.remove(); // 줌 컨트롤 제거
    
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

    console.log("======== leaflet ======== ")
    console.log(tileRef.value); // 1.9.4
    console.log(attribution.value);
    // =================================================== 타일 적용 ===================================================
    leaflet.tileLayer(import.meta.env.VITE_TILE_LAYER_URL, {
        attribution: import.meta.env.VITE_TILE_ATTRIVUTION
    }).addTo(map);
    
    

    if(userGeoMaker){
        map.removeLayer(userGeoMaker)
    }
    
    // 핀 추가
    userGeoMaker  = leaflet.marker([userMarker.value.latitude, userMarker.value.longtitude]).addTo(map).bindPopup("You are here!").openPopup();
    leaflet.marker([37.58195902773145, 127.01622722048013]).addTo(map).bindPopup("You are here!")


    const crosswalkGeojson: any = convertToGeoJSON(crosswalk);
    // 횡단보도 geojson 데이터 출력
    // leaflet.geoJSON(crosswalkGeojson).addTo(map);

    var drawItems = new leaflet.FeatureGroup();
    map.addLayer(drawItems);
    var drawControl = new leaflet.Control.Draw({
        edit: {
            featureGroup: drawItems
        },
        position: 'topright',
        draw: {
            polygon: {
                allowIntersection: false,
                showArea: false,
                shapeOptions: {
                    color: '#97009c'
                }
            },
            polyline: {
                metric: false,
                shapeOptions: {
                    color: '#97009c'
                }
            },
            rectangle: {
                shapeOptions: {
                    interactive: false
                }
            },
            circle: {
                shapeOptions: {
                    interactive: false
                }
            },
            marker: {
                icon: leaflet.divIcon({
                    className: 'my-div-icon',
                    html: '<div style="background-color: red; width: 20px; height: 20px; border-radius: 50%;"></div>',
                    iconSize: [20, 20]
                })
            }
        }
    });
    map.addControl(drawControl);

    map.on(leaflet.Draw.Event.CREATED, (e: any) => {
        const layer = e.layer;

        // 저장할 도형을 FeatureGroup에 추가
        drawItems.addLayer(layer);

        // GeoJSON으로 변환
        const geojsonData = layer.toGeoJSON();

        // 필요시 여러 개 저장할 수 있게 배열에 push
        console.log("Drawn GeoJSON:", geojsonData);

        // 여기에 저장 로직 (ex. API 호출)
        saveDrawnLayer(geojsonData);
    });

    getAllGeom();
})

const getAllGeom = async () => {
    const response = await useGeom().getGeom();
    console.log("getAllGeom", response);
    if(response){
        response.forEach((item: any) => {
            const geojson = item.geom;
            const layer = leaflet.geoJSON(geojson, {
                style: { color: 'blue', weight: 1 },
                onEachFeature: (feature, layer) => {
                    const name = feature?.properties?.name || "Unnamed Feature";
                    layer.bindPopup(`<b>${name}</b>`);
                },
            }).addTo(map);
            geojsonLayers[item.name] = layer;
        });
    }
}
const saveDrawnLayer = async (geojsonData: any) => {
    // 여기에 저장 로직을 구현합니다.
    console.log("Saving drawn layer:", geojsonData);
    const wrappedGeojson = {
        name: 'Drawn Feature',
        description: 'A feature drawn on the map',
        geom: geojsonData
    };

    const add = await useGeom().addGeom(wrappedGeojson)
    
    console.log("Saved:", add);
}

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

const getBus = async (busRouteId: any) => {
    const busNum = Number(busRouteId.value)
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