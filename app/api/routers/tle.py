from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import TLE
from app.schemas.tle import TLECreate, TLERead
from app.api.deps import get_db

router = APIRouter(prefix="/api/tle", tags=["TLE"])

@router.post("/", response_model=TLERead, status_code=status.HTTP_201_CREATED)
async def create_tle(tle_in: TLECreate, db: AsyncSession = Depends(get_db)):
    tle = TLE(**tle_in.dict())
    db.add(tle)
    await db.commit()
    await db.refresh(tle)
    return tle

@router.get("/", response_model=List[TLERead])
async def list_tle(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TLE).order_by(TLE.id))
    return result.scalars().all()