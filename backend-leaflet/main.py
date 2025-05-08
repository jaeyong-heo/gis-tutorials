import httpx
from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/bus-pos")
async def get_bus_pos(busRouteId: str):
    url = "http://ws.bus.go.kr/api/rest/buspos/getBusPosByRouteSt"
    params = {
        "serviceKey": "VZPZLxcnYIKVmnmw%2BZ9M4GTVRGmH3i%2BHu9GwqkIcULY1wdK9t7IUaM%2BiYE5Ska1YCakZ2mJWaSB7M2k0Z3VjKA%3D%3D",
        "busRouteId": busRouteId,
        "startOrd": 1,
        "endOrd": 10,
        "resultType": "json"
    }
    print(params)
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        return response.json()