import numpy as np
from sklearn.ensemble import IsolationForest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.models import Telemetry, Anomaly

class AnomalyDetector:
    def __init__(self, contamination: float = 0.01):
        self.model = IsolationForest(contamination=contamination, random_state=42)

    async def train_and_detect(self, db: AsyncSession, tle_id: int, window: int = 1000):
        # 1) Récupérer les dernières lignes de télémétrie
        stmt = (
            select(Telemetry)
            .where(Telemetry.tle_id == tle_id)
            .order_by(Telemetry.timestamp.desc())
            .limit(window)
        )
        result = await db.execute(stmt)
        data = result.scalars().all()
        if not data:
            return []

        # 2) Préparer le tableau numpy [n_samples, n_features]
        X = np.array([[t.battery, t.temperature, t.signal] for t in data])

        # 3) Entraîner et prédire
        self.model.fit(X)
        preds = self.model.decision_function(X)  # score
        labels = self.model.predict(X)           # -1 anomalie, 1 normal

        # 4) Collecter les anomalies
        anomalies = []
        for t, score, label in zip(data, preds, labels):
            if label == -1:
                anomalies.append(
                    Anomaly(
                        tle_id=t.tle_id,
                        timestamp=t.timestamp,
                        feature="all",
                        value=score,
                        score=float(score),
                    )
                )
        # 5) Stocker en base
        db.add_all(anomalies)
        await db.commit()
        return anomalies