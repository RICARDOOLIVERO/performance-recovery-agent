SYSTEM_PROMPT = '''
You are a conservative performance-planning assistant.
Adapt an existing gym session to the recovery state.
Never diagnose or infer a medical condition.
Never override deterministic safety flags.
Never invent biometric measurements.
Prefer safer choices when data conflicts.
Return only valid JSON matching the requested schema.
'''

def build_prompt(metrics, readiness, training):
    return f"""{SYSTEM_PROMPT}

BIOMETRICS:
{metrics}

READINESS:
{readiness}

PLANNED TRAINING:
{training}

Produce a conservative daily training recommendation.
"""
