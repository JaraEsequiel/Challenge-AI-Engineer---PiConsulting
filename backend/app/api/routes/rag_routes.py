from fastapi import APIRouter, UploadFile, File, Depends
from app.schemas.document import DocumentResponse
from app.services.rag_service import RAGService

router = APIRouter()

@router.post("/upload_document", response_model=DocumentResponse)
async def upload_document(file: UploadFile = File(...), service: RAGService = Depends()):
    return await service.upload_document(file)
