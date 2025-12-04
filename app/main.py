from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Athletes API MVP", version="0.1.0")

app.include_router(router)
