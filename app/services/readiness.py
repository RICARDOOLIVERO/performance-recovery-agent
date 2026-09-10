from app.models.schemas import BiometricSnapshot, ReadinessAssessment, TrainingMode

def clamp(v, lo=0, hi=100):
    return max(lo, min(hi, v))

def calculate_readiness(m: BiometricSnapshot) -> ReadinessAssessment:
    score = 50.0
    reasons, flags = [], []

    score += min(m.sleep_hours / 8.0, 1.0) * 25 - 12.5
    if m.sleep_hours < 6:
        flags.append("short_sleep")
        reasons.append("Sleep duration is below the conservative threshold.")
    elif m.sleep_hours >= 7.5:
        reasons.append("Sleep duration supports normal training.")

    if m.sleep_score < 65:
        flags.append("low_sleep_quality")
        score -= 10
    elif m.sleep_score >= 80:
        score += 5

    hrv_ratio = m.hrv_ms / m.hrv_baseline_ms
    if hrv_ratio < 0.85:
        score -= 18
        flags.append("low_hrv_vs_baseline")
        reasons.append("HRV is materially below baseline.")
    elif hrv_ratio >= 1.05:
        score += 8

    rhr_delta = m.resting_hr_bpm - m.resting_hr_baseline_bpm
    if rhr_delta >= 7:
        score -= 18
        flags.append("elevated_resting_hr")
    elif rhr_delta <= -2:
        score += 3

    if m.cardio_load >= 80:
        score -= 12
        flags.append("high_cardio_load")
    elif m.cardio_load <= 40:
        score += 2

    if m.recent_strain >= 8.5:
        score -= 8
        flags.append("high_recent_strain")

    score = round(clamp(score), 1)

    if "short_sleep" in flags or "elevated_resting_hr" in flags:
        mode = TrainingMode.REST if score < 45 else TrainingMode.ACTIVE_RECOVERY
    elif score >= 78:
        mode = TrainingMode.INTENSE
    elif score >= 62:
        mode = TrainingMode.MODERATE
    elif score >= 45:
        mode = TrainingMode.ACTIVE_RECOVERY
    else:
        mode = TrainingMode.REST

    confidence = min(0.95, 0.55 + (0.2 if not flags else 0) + (0.1 if score >= 78 or score < 45 else 0))
    return ReadinessAssessment(
        score=score, mode=mode, confidence=round(confidence, 2),
        reasons=reasons, flags=flags
    )
