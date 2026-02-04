from fastapi import APIRouter

from app.api.v1.messages import router as messages_router
from app.api.v1.connections import router as connections_router

api_router = APIRouter()

api_router.include_router(messages_router)
api_router.include_router(connections_router)
