from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.api.deps import get_db
from app.services.anomalies import AnomalyDetector
from app.db.models import Anomaly
from app.schemas.anomaly import AnomalyRead

router = APIRouter(prefix="/api/anomalies", tags=["Anomalies"])
detector = AnomalyDetector(contamination=0.01)

@router.post("/run/{tle_id}", response_model=List[AnomalyRead])
async def run_detection(
    tle_id: int,
    db: AsyncSession = Depends(get_db),
    window: int = Query(1000, ge=100, le=10000)
):
    result = await detector.train_and_detect(db, tle_id=tle_id, window=window)
    if not result:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return result

@router.get("/", response_model=List[AnomalyRead])
async def list_anomalies(
    tle_id: int | None = Query(None),
    limit: int = Query(100, gt=0, le=1000),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Anomaly).order_by(Anomaly.timestamp.desc()).limit(limit)
    if tle_id is not None:
        stmt = stmt.where(Anomaly.tle_id == tle_id)
    res = await db.execute(stmt)
    return res.scalars().all()