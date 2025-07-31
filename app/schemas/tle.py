from datetime import datetime
from pydantic import BaseModel

class TLEBase(BaseModel):
    name: str
    line1: str
    line2: str

class TLECreate(TLEBase):
    pass

class TLERead(TLEBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True