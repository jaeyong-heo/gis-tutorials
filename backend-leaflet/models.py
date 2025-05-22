from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, func
from database import Base
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)




Base = declarative_base()

class GeoFeature(Base):
    __tablename__ = "geo_features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    geom = Column(Geometry(geometry_type='GEOMETRY', srid=4326), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)   
         
class Region(Base):
    __tablename__ = "regions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    geom = Column(Geometry(geometry_type='POLYGON', srid=4326))  # WGS84 좌표계
    properties = Column(JSONB)  # GeoJSON의 properties 저장용(선택)


class GeoFeatureJson(Base):
    __tablename__ = "geo_features_json"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    geom = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)            


