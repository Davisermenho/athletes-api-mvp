# Athletes API - MVP (skeleton)

Rápido esqueleto FastAPI para desenvolvimento local.

Run locally:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Docker:

```bash
docker build -t athletes-api .
docker run -p 8000:8000 athletes-api
```

Endpoints:

- `GET /` — root
- `GET /health` — health check
