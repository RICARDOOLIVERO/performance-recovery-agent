from datetime import date
from enum import Enum
from pydantic import BaseModel, Field

class TrainingMode(str, Enum):
    INTENSE = "intense"
    MODERATE = "moderate"
    ACTIVE_RECOVERY = "active_recovery"
    REST = "rest"

class Exercise(BaseModel):
    name: str
    sets: int = Field(ge=1, le=20)
    reps: int = Field(ge=1, le=100)
    load_kg: float = Field(ge=0)
    rpe_target: float | None = Field(default=None, ge=1, le=10)

class TrainingPlan(BaseModel):
    session_type: str
    target_rpe: float = Field(ge=1, le=10)
    planned_volume: float = Field(ge=0)
    priority: str = "normal"
    exercises: list[Exercise] = Field(default_factory=list)

class BiometricSnapshot(BaseModel):
    user_id: str
    date: date
    sleep_hours: float = Field(ge=0, le=24)
    sleep_score: float = Field(ge=0, le=100)
    hrv_ms: float = Field(ge=0)
    hrv_baseline_ms: float = Field(gt=0)
    resting_hr_bpm: float = Field(gt=0)
    resting_hr_baseline_bpm: float = Field(gt=0)
    cardio_load: float = Field(ge=0)
    recent_strain: float = Field(ge=0)
    source: str

class ReadinessAssessment(BaseModel):
    score: float = Field(ge=0, le=100)
    mode: TrainingMode
    confidence: float = Field(ge=0, le=1)
    reasons: list[str]
    flags: list[str]

class Recommendation(BaseModel):
    user_id: str
    date: date
    readiness: ReadinessAssessment
    recommended_mode: TrainingMode
    intensity_modifier: float = Field(ge=0, le=1)
    volume_modifier: float = Field(ge=0, le=1)
    suggested_rpe: float = Field(ge=1, le=10)
    session_focus: str
    recommendations: list[str]
    warnings: list[str]
    rationale: str

class DailyRecommendationRequest(BaseModel):
    user_id: str
    date: date
    wearable: str = "mock"
    training: TrainingPlan
