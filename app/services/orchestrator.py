from datetime import date
from app.integrations.mock import MockWearableAdapter
from app.models.schemas import Recommendation, TrainingMode, TrainingPlan
from app.services.readiness import calculate_readiness

class RecommendationOrchestrator:
    def __init__(self):
        self.mock = MockWearableAdapter()

    async def recommend(self, user_id: str, target_date: date, wearable: str, training: TrainingPlan):
        if wearable != "mock":
            raise ValueError("Only mock is configured. Add your provider adapter in app/integrations/.")

        metrics = await self.mock.get_daily_metrics(user_id, target_date)
        readiness = calculate_readiness(metrics)
        mode = readiness.mode

        if mode == TrainingMode.INTENSE:
            intensity, volume, rpe = 1.0, 1.0, min(training.target_rpe, 9.0)
            focus = "Planned strength/performance session"
            recs = ["Keep planned exercises.", "Use normal loads if warm-up performance is normal.",
                    "Reduce load if technique or perceived effort deteriorates unexpectedly."]
        elif mode == TrainingMode.MODERATE:
            intensity, volume, rpe = 0.90, 0.85, min(training.target_rpe, 7.5)
            focus = "Moderate training with controlled volume"
            recs = ["Keep main lifts but reduce working load modestly.",
                    "Remove 1 accessory set if fatigue accumulates.", "Avoid grinding reps."]
        elif mode == TrainingMode.ACTIVE_RECOVERY:
            intensity, volume, rpe = 0.65, 0.55, 5.5
            focus = "Active recovery / low-fatigue session"
            recs = ["Prioritize easy movement, mobility and technique.",
                    "Reduce load and total sets substantially.", "Avoid maximal or near-failure work."]
        else:
            intensity, volume, rpe = 0.0, 0.0, 3.0
            focus = "Recovery day"
            recs = ["Skip the planned high-intensity lifting session.",
                    "Prefer rest or very easy movement if comfortable."]

        warnings = []
        if readiness.flags:
            warnings.append("Recovery flags detected: " + ", ".join(readiness.flags))

        return Recommendation(
            user_id=user_id, date=target_date, readiness=readiness,
            recommended_mode=mode, intensity_modifier=intensity,
            volume_modifier=volume, suggested_rpe=rpe, session_focus=focus,
            recommendations=recs, warnings=warnings,
            rationale=f"Readiness score {readiness.score}/100 led to {mode.value}. "
                      "The deterministic safety layer has priority over generative output."
        )
