<template>
    <div id="map"></div>
</template>

<script setup lang="ts">
import leaflet from "leaflet"
import { onMounted, watchEffect } from "vue";
import { useGeolocation } from '@vueuse/core'
import { userMarker, nearbyMarker} from "@/stores/mapStore"

let map: leaflet.Map;
let userGeoMaker: leaflet.Marker;
const { coords, locatedAt, error, resume, pause } = useGeolocation()
console.log(coords.value.latitude, coords.value.longitude)
onMounted(()=>{
    map = leaflet
    .map('map')
    .setView([userMarker.value.latitude, userMarker.value.longtitude ], 13);

    // Control options
    map.zoomControl.remove(); // 줌 컨트롤 제거

    leaflet.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    nearbyMarker.value.forEach((marker) => {
        leaflet.marker([marker.latitude, marker.longtitude]).addTo(map).bindPopup(marker.latitude.toString()).openPopup();
    })

    map.addEventListener('click', (e: leaflet.LeafletMouseEvent) => {
        const lat = e.latlng.lat;
        const lng = e.latlng.lng;
        // userMarker.value.latitude = lat;
        // userMarker.value.longtitude = lng;
        console.log(lat, lng)

        leaflet.marker([lat, lng]).addTo(map).bindPopup(`lat : ${lat.toFixed(4)}, lng : ${lng.toFixed(4)}`).openPopup();
    })

    if(userGeoMaker){
        map.removeLayer(userGeoMaker)
    }
    userGeoMaker  = leaflet.marker([userMarker.value.latitude, userMarker.value.longtitude]).addTo(map).bindPopup("You are here!").openPopup();
    const circle = leaflet.circle([userMarker.value.latitude, userMarker.value.longtitude], {
        color: 'red',
        fillColor: '#f03',
        fillOpacity: 0,
        radius: 500
    }).addTo(map);
    var polygon = leaflet.polygon([
        makeRandomPosition(userMarker.value.latitude, userMarker.value.longtitude),
        makeRandomPosition(userMarker.value.latitude, userMarker.value.longtitude),
        makeRandomPosition(userMarker.value.latitude, userMarker.value.longtitude),
        makeRandomPosition(userMarker.value.latitude, userMarker.value.longtitude),
    ], {
        color: 'green',
        fillColor: 'gold',
        fillOpacity: 0.5
    }).addTo(map);
    map.setView([userMarker.value.latitude, userMarker.value.longtitude], 13);

    const el = userGeoMaker.getElement();
    if(el){
        el.style.filter = "hue-rotate(120deg)";
    }



    var greenIcon = leaflet.icon({
    iconUrl: 'leaf-green.png',
    shadowUrl: 'leaf-shadow.png',

    iconSize:     [38, 95], // size of the icon
    shadowSize:   [50, 64], // size of the shadow
    iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62],  // the same for the shadow
    popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});
    leaflet.marker(makeRandomPosition(userMarker.value.latitude, userMarker.value.longtitude), {icon: greenIcon}).addTo(map);
})

const makeRandomPosition = (lat: number, lng: number): [number, number] =>{
    const latOffset = Math.random() * 0.01 - 0.005; // -0.005 ~ 0.005
    const lngOffset = Math.random() * 0.01 - 0.005; // -0.005 ~ 0.005

    return [lat + latOffset, lng + lngOffset];
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