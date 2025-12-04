from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["root"])
async def root():
    return {"message": "Athletes API MVP"}


@router.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}
