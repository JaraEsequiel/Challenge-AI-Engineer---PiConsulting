from pydantic import BaseModel

class DocumentResponse(BaseModel):
    filename: str
    size: int
