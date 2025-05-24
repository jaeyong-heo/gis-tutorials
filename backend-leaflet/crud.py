from sqlalchemy.orm import Session
from geoalchemy2.shape import from_shape
from shapely.geometry import shape


from models import GeoFeature
from schemas import GeoFeatureCreate

def create_geo_feature(db: Session, feature: GeoFeatureCreate):
    db_feature = GeoFeature(
        name=feature.name,
        description=feature.description
    )

    if feature.geom:
        # Convert GeoJSON to WKBElement using Shapely
        shapely_geom = shape(feature.geom)
        db_feature.geom = from_shape(shapely_geom, srid=4326)

    db.add(db_feature)
    db.commit()
    db.refresh(db_feature)
    return db_feature

def get_all_features(db: Session):
    return db.query(GeoFeature).all()
