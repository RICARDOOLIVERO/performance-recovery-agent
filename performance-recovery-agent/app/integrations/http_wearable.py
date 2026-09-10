from datetime import date
import httpx
from app.integrations.base import WearableAdapter
from app.models.schemas import BiometricSnapshot

class RestWearableAdapter(WearableAdapter):
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.token = token

    async def get_daily_metrics(self, user_id: str, target_date: date) -> BiometricSnapshot:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                f"{self.base_url}/daily-metrics",
                headers={"Authorization": f"Bearer {self.token}"},
                params={"user_id": user_id, "date": target_date.isoformat()},
            )
            response.raise_for_status()
            return BiometricSnapshot(**response.json())
