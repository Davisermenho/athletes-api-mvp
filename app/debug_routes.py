import os

from fastapi import APIRouter, Depends, Header, HTTPException
from starlette.concurrency import run_in_threadpool

from app.db import get_athlete_by_athlete_id
from app.schemas import AthleteRead

router = APIRouter(prefix="/_debug")


def require_admin_api_key(x_admin_api_key: str | None = Header(None)):
    """Require an ADMIN_API_KEY when not in development.

    Behavior:
    - If `APP_ENV` == 'development': allow without checking (developer convenience).
    - Else: require `ADMIN_API_KEY` to be set and match `x-admin-api-key` header.

    Note: for staging/ops you should also ensure TLS and network ACLs.
    """
    app_env = os.getenv("APP_ENV", "development")
    admin_key = os.getenv("ADMIN_API_KEY")
    if app_env == "development":
        return None
    if not admin_key:
        raise HTTPException(
            status_code=500,
            detail="ADMIN_API_KEY not configured for protected debug endpoints",
        )
    if x_admin_api_key != admin_key:
        raise HTTPException(status_code=401, detail="Invalid admin API key")
    return None


@router.get("/athletes/{athlete_id}", response_model=AthleteRead, tags=["debug"])
async def read_athlete(athlete_id: str, _=Depends(require_admin_api_key)):
    """Debug route to retrieve an athlete by `athlete_id`.

    This route is intended for development and debugging only. It is mounted
    under `/_debug`. Inclusion in the application is conditional (see
    `app.main`): by default it should only be available when
    `ALLOW_DEBUG_ENDPOINTS=1` and `APP_ENV=development`.
    """
    try:
        row = await run_in_threadpool(get_athlete_by_athlete_id, athlete_id)
        if not row:
            raise HTTPException(status_code=404, detail="Athlete not found")
        return row
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
