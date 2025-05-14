from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class UserCreate(BaseModel):
    name: str
    email: str

class UserOut(UserCreate):
    id: int

    model_config = {
        "from_attributes": True
    }

class Geom(BaseModel):
    geom: Optional[Dict[str, Any]] = None  # GeoJSON object
    
class GeoFeatureBase(BaseModel):
    name: str
    description: Optional[str] = None
    geom: Optional[Dict[str, Any]] = None  # GeoJSON object

class GeoFeatureCreate(GeoFeatureBase):
    pass

class GeoFeatureOut(GeoFeatureBase):
    id: int
    created_at: Optional[str]

    model_config = {
        "from_attributes": True
    }