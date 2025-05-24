from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, func
from database import Base
from geoalchemy2 import Geometry
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSONB


Base = declarative_base()

class GeoFeature(Base):
    __tablename__ = "geo_features"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    geom = Column(Geometry(geometry_type='GEOMETRY', srid=4326), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=True)   
         
