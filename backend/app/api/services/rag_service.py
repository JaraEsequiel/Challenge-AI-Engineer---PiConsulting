from fastapi import UploadFile
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.documents import Document
from app.schemas.document import DocumentResponse, DocumentRetrievalResponse, Qna
import os
import tempfile
from app.api.core.config import settings


class RAGService:
    """Service class for managing RAG (Retrieval Augmented Generation) operations.
    
    Handles document uploading, querying, and QnA management using Pinecone vector store.
    
    Attributes:
        _vector_store (PineconeVectorStore): Vector store for document embeddings
        _embeddings (OpenAIEmbeddings): OpenAI embeddings model
    """
    def __init__(self):
        """Initialize RAG service with OpenAI embeddings and Pinecone vector store."""
        self._embeddings = OpenAIEmbeddings(
            model="text-embedding-3-large", 
            api_key=settings.get("OPENAI_API_KEY")
        )
        
        self._vector_store = PineconeVectorStore(
            pinecone_api_key=settings.get("PINECONE_API_KEY"),
            index_name="piconsulting",
            embedding=self._embeddings
        )

    def _identify_source_type(self, text: str) -> str:
        """Identify the type of content based on keywords.
        
        Args:
            text (str): Text to identify source type for
            
        Returns:
            str: Identified source type
        """
        if "Ficción Espacial" in text:
            return "Ficcion Espacial"
        elif "Ficción Tecnológica" in text:
            return "Ficcion Tecnologica" 
        elif "Naturaleza" in text:
            return "Naturaleza"
        elif "Cuento Corto" in text:
            return "Cuento Corto"
        elif "Héroe" in text:
            return "Características del Héroe Olvidado"
        return "Unknown"

    async def upload_document(self, file: UploadFile) -> DocumentResponse:
        """Upload and process a document file.
        
        Args:
            file (UploadFile): Document file to upload
            
        Returns:
            DocumentResponse: Response containing filename and size
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name

        try:
            loader = Docx2txtLoader(tmp_path)
            data = loader.load()
            chunks = data[0].page_content.split('\n\n')

            documents = [
                Document(
                    page_content=chunk,
                    metadata={"source": self._identify_source_type(chunk)}
                ) for chunk in chunks
            ]
            
            self._vector_store.add_documents(documents)
            return {"filename": file.filename, "size": len(content)}
            
        finally:
            os.unlink(tmp_path)

    async def query_document(self, query: str, k: int = 3) -> DocumentRetrievalResponse:
        """Query the vector store for relevant documents.
        
        Args:
            query (str): Query string to search for
            k (int): Number of results to return
            
        Returns:
            DocumentRetrievalResponse: Response containing matched documents
        """
        return self._vector_store.similarity_search(query, k)
    
    async def upload_qna(self, qna: Qna) -> dict:
        """Upload a QnA pair to the vector store.
        
        Args:
            qna (Qna): Question and answer pair to upload
            
        Returns:
            dict: Success message
        """
        content = f"Questions: {qna.question}\n\nAnswer: {qna.answer}"
        document = Document(page_content=content, metadata={"source": "QnA"})
        self._vector_store.add_documents([document])
        
        return {"message": "QnA uploaded successfully"}
