from fastapi import APIRouter, Depends
from app.schemas.message import MessageRequest, MessageResponse
from app.api.services.llm_service import LLMService

router = APIRouter()

@router.post("/generate_message", response_model=MessageResponse)
async def generate_message(request: MessageRequest, service: LLMService = Depends()):
    return await service.generate_message(request.content)


