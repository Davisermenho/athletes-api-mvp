import os

from fastapi import FastAPI

from app.routes import router

app = FastAPI(title="Athletes API MVP", version="0.1.0")

app.include_router(router)

# Conditionally include debug-only endpoints.
# - Developers can enable debug endpoints with ALLOW_DEBUG_ENDPOINTS=1 and APP_ENV=development
# - Debug endpoints are never included in production builds (APP_ENV=production)
if (
    os.getenv("ALLOW_DEBUG_ENDPOINTS") == "1"
    and os.getenv("APP_ENV", "development") != "production"
):
    try:
        from app.debug_routes import router as debug_router

        app.include_router(debug_router)
    except Exception:
        # If debug routes cannot be imported, do not fail app startup.
        pass
