from sqlalchemy.orm import Session


from crud import create_geo_feature, get_all_features
from schemas import GeoFeatureCreate

def create_feature_service(db: Session, feature: GeoFeatureCreate):
    return create_geo_feature(db, feature)

def get_features_service(db: Session):
    features = get_all_features(db)
    
    print(f"features : {features}")
    return features
