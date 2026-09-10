from abc import ABC, abstractmethod
from datetime import date
from app.models.schemas import BiometricSnapshot

class WearableAdapter(ABC):
    @abstractmethod
    async def get_daily_metrics(self, user_id: str, target_date: date) -> BiometricSnapshot:
        raise NotImplementedError
