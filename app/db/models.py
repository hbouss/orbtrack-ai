from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    TIMESTAMP,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TLE(Base):
    __tablename__ = "tle"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    line1 = Column(String, nullable=False)
    line2 = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default="now()")

class Telemetry(Base):
    __tablename__ = "telemetry"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, index=True)
    tle_id = Column(Integer, nullable=False, index=True)
    battery = Column(Float)
    temperature = Column(Float)
    signal = Column(Float)

class Anomaly(Base):
    __tablename__ = "anomaly"
    id = Column(Integer, primary_key=True, index=True)
    tle_id = Column(Integer, nullable=False, index=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, index=True)
    feature = Column(String, nullable=False)    # e.g. "battery" ou "temperature"
    value = Column(Float, nullable=False)       # valeur observée
    score = Column(Float, nullable=False)       # score de l’IsolationForest