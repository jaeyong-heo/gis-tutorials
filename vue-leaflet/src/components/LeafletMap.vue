<template>
  <div ref="mapContainer" class="map-container"></div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import L from 'leaflet'

const mapContainer = ref<HTMLDivElement | null>(null)

onMounted(() => {
  if (mapContainer.value) {
    // 지도 인스턴스를 생성합니다
    const map = L.map(mapContainer.value).setView([51.505, -0.09], 13)

    // OpenStreetMap 타일 레이어 추가
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map)

    // 지도에 마커 추가
    L.marker([51.5, -0.09]).addTo(map).bindPopup('A pretty CSS3 popup.').openPopup()
  }
})
</script>

<style scoped>
.map-container {
  height: 400px; /* 맵의 높이를 설정 */
}
</style>
