import os
from datetime import date
from app.integrations.base import WearableAdapter
from app.models.schemas import BiometricSnapshot

class MockWearableAdapter(WearableAdapter):
    async def get_daily_metrics(self, user_id: str, target_date: date) -> BiometricSnapshot:
        return BiometricSnapshot(
            user_id=user_id, date=target_date,
            sleep_hours=float(os.getenv("MOCK_SLEEP_HOURS", "7.8")),
            sleep_score=float(os.getenv("MOCK_SLEEP_SCORE", "86")),
            hrv_ms=float(os.getenv("MOCK_HRV", "62")),
            hrv_baseline_ms=60,
            resting_hr_bpm=52, resting_hr_baseline_bpm=55,
            cardio_load=float(os.getenv("MOCK_CARDIO_LOAD", "35")),
            recent_strain=float(os.getenv("MOCK_STRAIN", "7")),
            source="mock",
        )
