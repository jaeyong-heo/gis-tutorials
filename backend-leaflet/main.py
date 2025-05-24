import httpx
from typing import Union
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import models, schemas
from sqlalchemy.orm import Session
from database import get_db
from utils import geojson_to_geom, geom_to_geojson
from geoalchemy2.shape import from_shape
from shapely.geometry import shape
import service as services


from geoalchemy2.shape import to_shape
from shapely.geometry.base import BaseGeometry
from typing import Optional, Dict, Any
from datetime import datetime

def to_geojson_dict(geom) -> Optional[Dict[str, Any]]:
    if geom is None:
        return None
    # WKBElement -> shapely 객체 -> geojson dict
    shapely_geom: BaseGeometry = to_shape(geom)
    return shapely_geom.__geo_interface__

def serialize_geo_feature(db_obj) -> dict:
    return {
        "id": db_obj.id,
        "name": db_obj.name,
        "description": db_obj.description,
        "geom": to_geojson_dict(db_obj.geom),
        "created_at": db_obj.created_at.isoformat() if db_obj.created_at else None,
    }

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    print({"Hello": "World"})
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# 401번 버스 100100062
@app.get("/bus-pos")
async def get_bus_pos(busRouteId: str):
    # key_enc = 'VZPZLxcnYIKVmnmw%2BZ9M4GTVRGmH3i%2BHu9GwqkIcULY1wdK9t7IUaM%2BiYE5Ska1YCakZ2mJWaSB7M2k0Z3VjKA%3D%3D'
    key_dec = 'VZPZLxcnYIKVmnmw+Z9M4GTVRGmH3i+Hu9GwqkIcULY1wdK9t7IUaM+iYE5Ska1YCakZ2mJWaSB7M2k0Z3VjKA=='
    url = "http://ws.bus.go.kr/api/rest/buspos/getBusPosByRouteSt"
    params = {
        "serviceKey": key_dec,
        "busRouteId": busRouteId,
        "startOrd": 1,
        "endOrd": 30,
        "resultType": "json"
    }
    print(params)
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        return response.json()
    

# geojson 저장
"""
{
  "name": "My Location",
  "description": "A point feature example",
  "geom": {
    "type": "Point",
    "coordinates": [127.001, 37.567]
  }
}
"""
@app.post("/add", response_model=schemas.GeoFeatureCreate, )
def create_feature(feature: schemas.GeoFeatureCreate, db: Session = Depends(get_db)):
    return serialize_geo_feature(services.create_feature_service(db, feature))

# geojson 조회
@app.get("/get", response_model=list[schemas.GeoFeatureOut])
def get_features(db: Session = Depends(get_db)):
    db_features = services.get_features_service(db)     
    # SQLAlchemy + GeoAlchemy2에서 Geometry 타입 컬럼은 쿼리 결과를 WKB (Well-Known Binary) 형태의 WKBElement 객체로 반환합니다.
    # 이 객체를 GeoJSON 딕셔너리로 변환해야 합니다.
    # 변환 방법: geoalchemy2.shape.to_shape() 함수로 Shapely 객체로 변환 후 . __geo_interface__ 속성을 이용해 GeoJSON 딕셔너리로 변환
    return [serialize_geo_feature(f) for f in db_features]


@app.post("/features/")
def create_feature(feature: schemas.GeoFeatureBase, db: Session = Depends(get_db)):

    try:
        db_feature = models.GeoFeature(
            name=feature.name,
            description=feature.description,
            geom=geojson_to_geom(feature.geom) if feature.geom else None,
        )
        db.add(db_feature)
        db.commit()
        db.refresh(db_feature)
        return db_feature
    except Exception as e:
        print(f"오류 발생: {str(e)}")
    # convert geom to GeoJSON for response
    # result = schemas.GeoFeatureOut.from_orm(db_feature)
    # result.geom = geom_to_geojson(db_feature.geom)
    # return result



if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="localhost", port=7080, reload=True)
    