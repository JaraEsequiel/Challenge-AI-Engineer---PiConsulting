from pydantic import BaseModel

class MessageRequest(BaseModel):
    user_name: str
    quetion: str

class MessageResponse(BaseModel):
    answer: str
