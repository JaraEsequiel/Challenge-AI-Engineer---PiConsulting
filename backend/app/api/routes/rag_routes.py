from fastapi import APIRouter, UploadFile, File, Depends, Query
from app.schemas.document import DocumentResponse, DocumentRetrievalResponse, Qna
from app.api.services.rag_service import RAGService

# Create FastAPI router instance
router = APIRouter()

@router.post("/upload_document", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...), service: RAGService = Depends()):
    """
    Endpoint to upload a document for RAG processing.
    
    Args:
        file (UploadFile): The document file to upload
        service (RAGService): Injected RAG service instance
        
    Returns:
        DocumentResponse: Response containing upload status and document info
    """
    print(f"Received document upload request for file: {file.filename}")
    return await service.upload_document(file)

@router.post("/query_document", response_model=DocumentRetrievalResponse) 
async def query_document(query: str = Query(...), service: RAGService = Depends()):
    """
    Endpoint to query uploaded documents using RAG.
    
    Args:
        query (str): The query string to search for
        service (RAGService): Injected RAG service instance
        
    Returns:
        DocumentRetrievalResponse: Retrieved document chunks and generated response
    """
    print(f"Received document query request: {query}")
    return await service.query_document(query)

@router.post("/upload_qna", response_model=dict)
async def upload_qna(qna: Qna, service: RAGService = Depends()):
    """
    Endpoint to upload Q&A pairs for RAG.
    
    Args:
        qna (Qna): The Q&A data to upload
        service (RAGService): Injected RAG service instance
        
    Returns:
        DocumentRetrievalResponse: Response containing upload status
    """
    print(f"Received Q&A upload request")
    return await service.upload_qna(qna)
