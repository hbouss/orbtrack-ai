# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from app.api.routers import tle, telemetry, anomalies
from app.services.anomalies import AnomalyDetector
from app.db.session import AsyncSessionLocal
from app.db.models import TLE

# Initialise ton détecteur et le scheduler
detector = AnomalyDetector()
scheduler = AsyncIOScheduler()

# Job asynchrone pour toutes les TLE
async def anomaly_job():
    async with AsyncSessionLocal() as db:
        # Récupère tous les IDs de TLE
        result = await db.execute(select(TLE.id))
        tle_ids = result.scalars().all()
        # Lance la détection pour chacun
        for tle_id in tle_ids:
            await detector.train_and_detect(db, tle_id=tle_id)

# Lifespan handler (startup / shutdown)
@asynccontextmanager
async def lifespan(_app: FastAPI):
    # startup
    scheduler.add_job(
        anomaly_job,
        trigger="interval",
        seconds=30,
        id="anomaly_job_all_tles",
        replace_existing=True,
    )
    scheduler.start()
    yield
    # shutdown
    scheduler.shutdown()

# Crée ton app une fois avec le lifespan
app = FastAPI(
    title="OrbTrack AI",
    description="Monitoring et prédiction IA de CubeSats",
    lifespan=lifespan,
)

# Enregistre tes routers
app.include_router(tle.router)
app.include_router(telemetry.router)
app.include_router(anomalies.router)

@app.get("/")
async def root():
    return {"message": "Hello, OrbTrack AI is up and running!"}