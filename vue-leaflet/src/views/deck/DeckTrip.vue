<template>
  <div ref="deckContainer" class="deck-container"></div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { Deck } from '@deck.gl/core';
import { PolygonLayer } from '@deck.gl/layers';
import { TripsLayer } from '@deck.gl/geo-layers';
import { AmbientLight, PointLight, LightingEffect } from '@deck.gl/core';
import maplibregl from 'maplibre-gl';
import { MapView } from '@deck.gl/core';
import { animate } from 'popmotion';
import { userMarker, nearbyMarker, useMapStore } from "@/stores/mapStore"

const deckContainer = ref(null);

const tripData = ref([
  {
    "waypoints": [
      { "coordinates": [126.9751, 37.5759], "timestamp": 0 },
      { "coordinates": [126.9755, 37.5761], "timestamp": 9 },
      { "coordinates": [126.9768, 37.5763], "timestamp": 54 },
      { "coordinates": [126.9783, 37.5765], "timestamp": 92 },
      { "coordinates": [126.9807, 37.5772], "timestamp": 345 },
      { "coordinates": [126.9819, 37.5768], "timestamp": 402 },
      { "coordinates": [126.9828, 37.5774], "timestamp": 462 },
      { "coordinates": [126.9845, 37.5771], "timestamp": 563 },
      { "coordinates": [126.9869, 37.5776], "timestamp": 880 },
      { "coordinates": [126.9887, 37.5782], "timestamp": 1070 },
      { "coordinates": [126.9894, 37.5789], "timestamp": 1117 },
      { "coordinates": [126.9898, 37.5792], "timestamp": 1120 },
      { "coordinates": [126.9907, 37.5797], "timestamp": 1127 },
      { "coordinates": [126.9909, 37.5799], "timestamp": 1130 },
      { "coordinates": [126.9893, 37.5804], "timestamp": 1166 },
      { "coordinates": [126.9891, 37.5802], "timestamp": 1176 },
      { "coordinates": [126.9891, 37.5800], "timestamp": 1181 },
      { "coordinates": [126.9894, 37.5798], "timestamp": 1186 },
      { "coordinates": [126.9896, 37.5791], "timestamp": 1200 }
    ]
  }
])
const DATA_URL = {
  TRIPS: 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/trips/trips-v7.json'
};

const ambientLight = new AmbientLight({ color: [255, 255, 255], intensity: 1.0 });
const pointLight = new PointLight({ color: [255, 255, 255], intensity: 2.0, position: [-74.05, 40.7, 8000] });
const lightingEffect = new LightingEffect({ ambientLight, pointLight });


const theme = {
  buildingColor: [74, 80, 87],
  trailColor0: [253, 128, 93],
  trailColor1: [23, 184, 190],
  material: {
    ambient: 0.1,
    diffuse: 0.6,
    shininess: 32,
    specularColor: [60, 64, 70]
  },
  effects: [lightingEffect]
};

const INITIAL_VIEW_STATE = {
  // longitude: -74,
  // latitude: 40.72,
  longitude: userMarker.value.longtitude,
  latitude: userMarker.value.latitude,
  zoom: 13,
  pitch: 45,
  bearing: 0
};

const landCover = [
  [
    [-74.0, 40.7],
    [-74.02, 40.7],
    [-74.02, 40.72],
    [-74.0, 40.72]
  ]
];

let deck;
let map;

onMounted(async () => {
 

  let time = 1200;
  const trailLength = 180;
  const loopLength = 1800;
  const animationSpeed = 1;

  const updateLayers = () => [
    new TripsLayer({
      id: 'trips',
      data: tripData.value,
      getPath: d => d.waypoints.map(p => p.coordinates),
      getTimestamps: d => d.waypoints.map(p => p.timestamp),
      getColor: d => (d.vendor === 0 ? theme.trailColor0 : theme.trailColor1),
      opacity: 0.3,
      widthMinPixels: 2,
      rounded: true,
      trailLength,
      currentTime: time,
      shadowEnabled: false
    }),
  ];

  deck = new Deck({
    initialViewState: INITIAL_VIEW_STATE,
    controller: true,
    views: new MapView({ repeat: true }),
    effects: theme.effects,
    getTooltip: info => info.object && info.object.name,
    onViewStateChange: ({ viewState }) => {
      if (map) map.jumpTo(viewState);
    },
    layers: updateLayers(),
    parent: deckContainer.value
  });

  // Init MapLibre map (just the basemap)
  map = new maplibregl.Map({
    container: deckContainer.value,
    style: 'https://basemaps.cartocdn.com/gl/dark-matter-nolabels-gl-style/style.json',
    center: [INITIAL_VIEW_STATE.longitude, INITIAL_VIEW_STATE.latitude],
    zoom: INITIAL_VIEW_STATE.zoom,
    pitch: INITIAL_VIEW_STATE.pitch,
    bearing: INITIAL_VIEW_STATE.bearing,
    interactive: false
  });

  // Animate
  animate({
    from: 0,
    to: loopLength,
    duration: (loopLength * 60) / animationSpeed,
    repeat: Infinity,
    onUpdate: newTime => {
      time = newTime;
      deck.setProps({ layers: updateLayers() });
    }
  });
});
</script>

<style>
.deck-container {
  width: 100%;
  height: 100vh;
  position: relative;
}
</style>
