from pydantic import BaseModel
from langchain_core.documents import Document

class DocumentResponse(BaseModel):
    """Response model for document upload operations.
    
    Attributes:
        filename (str): Name of the uploaded file
        size (int): Size of the uploaded file in bytes
    """
    filename: str
    size: int

class DocumentRetrievalResponse(BaseModel):
    """Response model for document retrieval operations.
    
    Attributes:
        documents (list[Document]): List of retrieved document chunks with their content and metadata
    """
    documents: list[Document]

class Qna(BaseModel):
    """Model for question-answer pairs.
    
    Attributes:
        question (str): The question text
        answer (str): The corresponding answer text
    """
    question: str
    answer: str