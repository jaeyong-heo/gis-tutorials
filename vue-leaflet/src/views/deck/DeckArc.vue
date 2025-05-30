<template>
    <div id="map"></div>
</template>

<script setup lang="ts">
import { ref  } from "vue";
import leaflet from "leaflet"
import { onMounted, onBeforeMount } from "vue";
import { userMarker, useMapStore } from "@/stores/mapStore"
import { storeToRefs } from "pinia";
import { LeafletLayer } from "deck.gl-leaflet";
import { MapView, TripsLayer } from "deck.gl";
import { ArcLayer, GeoJsonLayer } from "@deck.gl/layers";
const {userMK} = storeToRefs(useMapStore());
const map = ref<leaflet.Map | null>(null);
// featureGroup 
let userGeoMaker: leaflet.Marker;
const tileRef = ref();
const attribution = ref();

const tripData = ref([
  {
    "waypoints": [
      { "coordinates": [126.9751, 37.5759], "timestamp": 1554772579000 },
      { "coordinates": [126.9755, 37.5761], "timestamp": 1554772579009 },
      { "coordinates": [126.9768, 37.5763], "timestamp": 1554772579054 },
      { "coordinates": [126.9783, 37.5765], "timestamp": 1554772579092 },
      { "coordinates": [126.9807, 37.5772], "timestamp": 1554772579345 },
      { "coordinates": [126.9819, 37.5768], "timestamp": 1554772579402 },
      { "coordinates": [126.9828, 37.5774], "timestamp": 1554772579462 },
      { "coordinates": [126.9845, 37.5771], "timestamp": 1554772579563 },
      { "coordinates": [126.9869, 37.5776], "timestamp": 1554772579880 },
      { "coordinates": [126.9887, 37.5782], "timestamp": 1554772580070 },
      { "coordinates": [126.9894, 37.5789], "timestamp": 1554772580117 },
      { "coordinates": [126.9898, 37.5792], "timestamp": 1554772580120 },
      { "coordinates": [126.9907, 37.5797], "timestamp": 1554772580127 },
      { "coordinates": [126.9909, 37.5799], "timestamp": 1554772580130 },
      { "coordinates": [126.9893, 37.5804], "timestamp": 1554772580166 },
      { "coordinates": [126.9891, 37.5802], "timestamp": 1554772580176 },
      { "coordinates": [126.9891, 37.5800], "timestamp": 1554772580181 },
      { "coordinates": [126.9894, 37.5798], "timestamp": 1554772580186 },
      { "coordinates": [126.9896, 37.5791], "timestamp": 1554772580200 }
    ]
  }
]
)
const AIR_PORTS =
  'https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_10m_airports.geojson';


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
            }
        });

        leaflet.tileLayer(tileRef.value, {
            attribution: attribution.value
        }).addTo(map.value as leaflet.Map);

    }


    const deckLayer = new LeafletLayer({
    // views: [new MapView({repeat: true})],
    layers: [
        new GeoJsonLayer({
        id: 'airports',
        data: AIR_PORTS,
        // Styles
        filled: true,
        pointRadiusMinPixels: 2,
        pointRadiusScale: 2000,
        getPointRadius: f => 11 - f.properties.scalerank,
        getFillColor: [200, 0, 80, 180]
        }),
        new ArcLayer({
        id: 'arcs',
        data: AIR_PORTS,
        dataTransform: (d: any) => d.features.filter((f: any) => f.properties.scalerank < 4),
        // Styles
        getSourcePosition: f => [-0.4531566, 51.4709959], // London
        getTargetPosition: f => f.geometry.coordinates,
        getSourceColor: [0, 128, 200],
        getTargetColor: [200, 0, 80],
        getWidth: 1
        }),
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
    map.value.addLayer(deckLayer);

});

</script>

<style scoped>
#map {
    height: 80vh;
    width: 100%;
}
</style>