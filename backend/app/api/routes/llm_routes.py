from fastapi import APIRouter, Depends
from app.schemas.message import MessageRequest, MessageResponse
from app.api.services.langgraph_service import LangGraphService

# Create FastAPI router instance
router = APIRouter()

@router.post("/generate_message", response_model=MessageResponse)
async def generate_message(request: MessageRequest, service: LangGraphService = Depends()):
    """
    Endpoint to generate a message response using the LangGraph service.
    
    Args:
        request (MessageRequest): The incoming message request containing the question
        service (LangGraphService): Injected LangGraph service instance
        
    Returns:
        MessageResponse: The generated message response
    """
    print(f"Received message generation request with question")
    
    # Call LangGraph service to generate response
    response = await service.generate_message(request.question)
    
    return response


