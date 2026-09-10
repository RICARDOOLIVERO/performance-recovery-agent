from fastapi import FastAPI, HTTPException
from app.core.config import settings
from app.models.schemas import DailyRecommendationRequest, Recommendation
from app.services.orchestrator import RecommendationOrchestrator

app = FastAPI(title=settings.app_name, version="0.1.0")
orchestrator = RecommendationOrchestrator()

@app.get("/health")
async def health():
    return {"status": "ok", "environment": settings.environment}

@app.post("/v1/recommendations/daily", response_model=Recommendation)
async def daily_recommendation(payload: DailyRecommendationRequest):
    try:
        return await orchestrator.recommend(
            payload.user_id, payload.date, payload.wearable, payload.training
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
