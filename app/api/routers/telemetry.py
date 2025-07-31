from typing import List
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Telemetry
from app.schemas.telemetry import TelemetryCreate, TelemetryRead
from app.api.deps import get_db

router = APIRouter(prefix="/api/telemetry", tags=["Telemetry"])

@router.post("/", response_model=TelemetryRead, status_code=status.HTTP_201_CREATED)
async def ingest(data: TelemetryCreate, db: AsyncSession = Depends(get_db)):
    tel = Telemetry(**data.dict())
    db.add(tel)
    await db.commit()
    await db.refresh(tel)
    return tel

@router.get("/", response_model=List[TelemetryRead])
async def list_telemetry(
    tle_id: int | None = Query(None),
    limit: int = Query(100, gt=0, le=1000),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Telemetry).order_by(Telemetry.timestamp.desc()).limit(limit)
    if tle_id:
        stmt = stmt.where(Telemetry.tle_id == tle_id)
    result = await db.execute(stmt)
    return result.scalars().all()