from pydantic import BaseModel
from langchain_core.documents import Document

class DocumentResponse(BaseModel):
    filename: str
    size: int

class DocumentRetrievalResponse(BaseModel):
    documents: list[Document]
