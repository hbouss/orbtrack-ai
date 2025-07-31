from datetime import datetime
from pydantic import BaseModel

class AnomalyRead(BaseModel):
    id: int
    tle_id: int
    timestamp: datetime
    feature: str
    value: float
    score: float

    class Config:
        from_attributes = True