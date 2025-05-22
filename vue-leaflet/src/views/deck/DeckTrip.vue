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

const deckContainer = ref(null);

const DATA_URL = {
  // BUILDINGS: 'https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/trips/buildings.json',
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
  longitude: -74,
  latitude: 40.72,
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
  // const buildings = await fetch(DATA_URL.BUILDINGS).then(res => res.json());
  const trips = await fetch(DATA_URL.TRIPS).then(res => res.json());

  let time = 0;
  const trailLength = 180;
  const loopLength = 1800;
  const animationSpeed = 1;

  const updateLayers = () => [
    new PolygonLayer({
      id: 'ground',
      data: landCover,
      getPolygon: f => f,
      stroked: false,
      getFillColor: [0, 0, 0, 0]
    }),
    new TripsLayer({
      id: 'trips',
      data: trips,
      getPath: d => d.path,
      getTimestamps: d => d.timestamps,
      getColor: d => (d.vendor === 0 ? theme.trailColor0 : theme.trailColor1),
      opacity: 0.3,
      widthMinPixels: 2,
      rounded: true,
      trailLength,
      currentTime: time,
      shadowEnabled: false
    }),
    // new PolygonLayer({
    //   id: 'buildings',
    //   data: buildings,
    //   extruded: true,
    //   wireframe: false,
    //   opacity: 0.5,
    //   getPolygon: f => f.polygon,
    //   getElevation: f => f.height,
    //   getFillColor: theme.buildingColor,
    //   material: theme.material
    // })
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
