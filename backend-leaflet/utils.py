from typing import Optional
from shapely.geometry import shape, mapping
from geoalchemy2.shape import from_shape, to_shape
from geoalchemy2.elements import WKBElement

def geojson_to_geom(geojson_obj: dict) -> WKBElement:
    shapely_obj = shape(geojson_obj)
    return from_shape(shapely_obj, srid=4326)

def geom_to_geojson(geom: WKBElement) -> Optional[dict]:
    if geom is None:
        return None
    shapely_obj = to_shape(geom)
    return mapping(shapely_obj)  # returns GeoJSON dict
