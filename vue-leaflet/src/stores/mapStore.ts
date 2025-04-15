import { useLocalStorage } from '@vueuse/core';

type Marker = {
    latitude: number;
    longtitude: number
}

export const userMarker = useLocalStorage<Marker>('USER_MARKER', {
    latitude: 0,
    longtitude: 0
});

export const nearbyMarker = useLocalStorage<Marker[]>('NEARBY_MARKER', []);