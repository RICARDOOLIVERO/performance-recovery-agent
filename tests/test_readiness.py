from datetime import date
from app.models.schemas import BiometricSnapshot, TrainingMode
from app.services.readiness import calculate_readiness

def metrics(**changes):
    data = dict(user_id="test", date=date(2026,9,9), sleep_hours=8,
        sleep_score=90, hrv_ms=65, hrv_baseline_ms=60,
        resting_hr_bpm=52, resting_hr_baseline_bpm=55,
        cardio_load=30, recent_strain=4, source="test")
    data.update(changes)
    return BiometricSnapshot(**data)

def test_good_recovery():
    r = calculate_readiness(metrics())
    assert r.score >= 70
    assert r.mode in {TrainingMode.INTENSE, TrainingMode.MODERATE}

def test_short_sleep():
    r = calculate_readiness(metrics(sleep_hours=5))
    assert "short_sleep" in r.flags
    assert r.mode in {TrainingMode.ACTIVE_RECOVERY, TrainingMode.REST}

def test_elevated_resting_hr():
    r = calculate_readiness(metrics(resting_hr_bpm=65))
    assert "elevated_resting_hr" in r.flags
