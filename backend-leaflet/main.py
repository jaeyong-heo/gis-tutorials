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
    


        
@app.post("/features/")
def create_feature(feature: schemas.GeoFeatureCreate, db: Session = Depends(get_db)):

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
    