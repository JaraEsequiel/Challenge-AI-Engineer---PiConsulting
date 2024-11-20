from fastapi import APIRouter, UploadFile, File, Depends, Query
from app.schemas.document import DocumentResponse, DocumentRetrievalResponse
from app.api.services.rag_service import RAGService

router = APIRouter()

@router.post("/upload_document", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...), service: RAGService = Depends()):
    return await service.upload_document(file)

@router.post("/query_document", response_model=DocumentRetrievalResponse)
async def query_document(query: str = Query(...), service: RAGService = Depends()):
    return await service.query_document(query)
