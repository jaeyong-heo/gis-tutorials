import { useLocalStorage } from '@vueuse/core';
import { defineStore } from 'pinia';
import { ref  } from "vue";

interface bound {
    northWest: [number, number],
    southEast: [number, number],
    northEast: [number, number],
    southWest: [number, number],
  }
interface Marker {
    latitude: number;
    longtitude: number;
    zoom: number;
    center: [number, number];
    bound:bound
}

export const userMarker = useLocalStorage<Marker>('USER_MARKER', {
    latitude: 0,
    longtitude: 0,
    zoom: 0,
    center: [0,0],
    bound: {northWest:[0,0], southEast:[0,0], northEast:[0,0], southWest:[0,0]}
});

export const nearbyMarker = useLocalStorage<Marker[]>('NEARBY_MARKER', []);

export const useMapStore = defineStore(
    "mapStore",
    () => {
        const userMK = ref<Marker>({
            latitude: 0,
            longtitude: 0,
            zoom: 13,
            center: [0,0],
            bound: {northWest:[0,0], southEast:[0,0], northEast:[0,0], southWest:[0,0]}
        });


        return {
            userMK
        }
    },
);
      