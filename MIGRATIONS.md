# Running migrations

This repository uses Alembic for database migrations. Do NOT run migrations automatically as part of the container start command — running `alembic upgrade head` during start can block application startup and cause health checks (e.g. Render's) to time out.

To run migrations manually against the database used in your environment, run:

```bash
alembic upgrade head
```

Recommended workflow:
- Deploy application image with migrations disabled on start (the image should start quickly and respond to `/health`).
- Run migrations separately (CI job, one-off admin task, or a job runner).
- After migrations succeed, promote the new deployment.
