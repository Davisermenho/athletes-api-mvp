from fastapi import APIRouter, HTTPException
from starlette.concurrency import run_in_threadpool

from app.db import upsert_athlete
from app.schemas import AthleteCreate, AthleteRead

router = APIRouter()


@router.get("/", tags=["root"])
async def root():
    return {"message": "Athletes API MVP"}


@router.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}


@router.post("/athletes", response_model=AthleteRead, tags=["athletes"])
async def create_athlete(payload: AthleteCreate):
    """Create or upsert an athlete by `athlete_id`.

    Uses a Postgres `INSERT ... ON CONFLICT` upsert.

    DATABASE_URL must point to Postgres.
    """
    try:
        data = payload.dict()
        # run DB upsert in threadpool to avoid blocking the event loop
        row = await run_in_threadpool(upsert_athlete, data)
        if not row:
            raise HTTPException(status_code=500, detail="Upsert failed")
        return row
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
