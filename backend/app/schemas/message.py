from pydantic import BaseModel

class MessageRequest(BaseModel):
    user_name: str
    question: str

class MessageResponse(BaseModel):
    answer: str
