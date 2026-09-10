from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200

def test_daily_recommendation():
    r = client.post("/v1/recommendations/daily", json={
        "user_id": "demo", "date": "2026-09-09", "wearable": "mock",
        "training": {
            "session_type": "strength", "target_rpe": 8,
            "planned_volume": 100, "priority": "high",
            "exercises": [{"name": "Squat", "sets": 4, "reps": 6, "load_kg": 100}]
        }
    })
    assert r.status_code == 200
    assert "readiness" in r.json()
