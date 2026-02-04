from fastapi import FastAPI

from app.api.router import api_router

app = FastAPI(title="ML-Anonymizer", version="1.0")

app.include_router(api_router, prefix="/api")
