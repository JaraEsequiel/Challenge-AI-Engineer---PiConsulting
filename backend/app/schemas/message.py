from pydantic import BaseModel

class MessageRequest(BaseModel):
    """Request model for message generation.
    
    Attributes:
        user_name (str): Name of the user making the request
        question (str): Question or query text from the user
    """
    user_name: str
    question: str

class MessageResponse(BaseModel):
    """Response model for generated messages.
    
    Attributes:
        answer (str): Generated answer text from the LLM
    """
    answer: str
