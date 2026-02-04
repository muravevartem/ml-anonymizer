from typing import Any

from fastapi import APIRouter

from app.schemas.message import MessageResponse, MessageRequest
from app.services.anonymizer import anonymizer

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageResponse)
async def create_message(message: MessageRequest) -> dict[str, Any]:
    return {
        "message": anonymizer.anonymize(message.message)
    }
