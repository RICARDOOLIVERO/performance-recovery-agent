# Performance & Recovery Agent

Agente Python para cruzar métricas de recuperación/sueño/esfuerzo de wearables con una planificación de gimnasio y generar una recomendación diaria.

> Educativo y de apoyo a la planificación. No diagnostica ni sustituye a un profesional sanitario.

## Arquitectura

```text
Wearable REST APIs -> Adapter -> Biometrics
                         |
                         v
                  Readiness Engine
                         |
                         v
                  Training Plan
                         |
                         v
              Recommendation Engine
                  |            |
             Rules/Safety      LLM
                  \            /
                   -> JSON API
```

La capa determinista tiene prioridad sobre el LLM.

## Inicio rápido

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

API: http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs

## Ejemplo

```bash
curl -X POST http://127.0.0.1:8000/v1/recommendations/daily ^
  -H "Content-Type: application/json" ^
  -d "{"user_id":"demo","date":"2026-09-09","wearable":"mock","training":{"session_type":"strength","target_rpe":8,"planned_volume":100,"priority":"high","exercises":[{"name":"Squat","sets":4,"reps":6,"load_kg":100}]}}"
```

## Wearables

El proyecto incluye un `MockWearableAdapter` y un adaptador REST genérico. Para conectar Garmin, Oura, WHOOP, Fitbit u otro proveedor, implementa `WearableAdapter` y transforma su respuesta a `BiometricSnapshot`.

Nunca guardes tokens en Git.

## Readiness

El MVP combina sueño, calidad del sueño, HRV relativo a baseline, frecuencia cardiaca en reposo, carga cardiovascular y esfuerzo reciente. Los umbrales están centralizados en `app/services/readiness.py`.

Modos:

- `intense`
- `moderate`
- `active_recovery`
- `rest`

## LLM

El LLM es opcional. `LLM_ENABLED=false` mantiene el agente operativo con reglas deterministas. Cuando se active, debe recibir datos normalizados y respetar las restricciones calculadas por el motor de seguridad.

## Producción

Antes de datos reales: autenticación/autorización, cifrado, consentimiento, política de retención, PostgreSQL, observabilidad, auditoría y validación de umbrales con profesionales adecuados.

## CI

GitHub Actions ejecuta los tests automáticamente.

## Licencia

MIT
