from datetime import datetime
from pydantic import BaseModel

class TelemetryBase(BaseModel):
    timestamp: datetime
    tle_id: int
    battery: float | None = None
    temperature: float | None = None
    signal: float | None = None

class TelemetryCreate(TelemetryBase):
    pass

class TelemetryRead(TelemetryBase):
    id: int

    class Config:
        orm_mode = True