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
    _vector_store: PineconeVectorStore
    _embeddings: OpenAIEmbeddings

    def __init__(self):
        """Initialize RAG service with OpenAI embeddings and Pinecone vector store."""
        print("Initializing RAG service...")
        self._embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=settings.get("OPENAI_API_KEY"))
        print("Configured OpenAI embeddings model")
        
        self._vector_store = PineconeVectorStore(pinecone_api_key=settings.get("PINECONE_API_KEY"), index_name="piconsulting", embedding=self._embeddings)
        print("Connected to Pinecone vector store")

    def _identify_source_type(self, text: str) -> str:
        """Identify the type of content based on keywords.
        
        Args:
            text (str): Text to identify source type for
            
        Returns:
            str: Identified source type
        """
        print(f"Identifying source type for text")
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

    async def upload_document(self, file: UploadFile) -> DocumentResponse:
        """Upload and process a document file.
        
        Args:
            file (UploadFile): Document file to upload
            
        Returns:
            DocumentResponse: Response containing filename and size
        """
        print(f"Processing upload for file: {file.filename}")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp_file:
            # Write uploaded file content to temporary file
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
            print(f"Created temporary file at: {tmp_path}")

        try:
            # Load document from temporary file
            print("Loading document content...")
            loader = Docx2txtLoader(tmp_path)
            data = loader.load()

            chunks = data[0].page_content.split('\n\n')
            print(f"Split document into {len(chunks)} chunks")

            for chunk in chunks:
                document = Document(page_content=chunk, metadata={"source": self._identify_source_type(chunk)})
                self._vector_store.add_documents([document])
                print(f"Added chunk to vector store with source: {document.metadata['source']}")
            
            return {"filename": file.filename, "size": len(content)}
        finally:
            # Clean up temporary file
            print(f"Cleaning up temporary file: {tmp_path}")
            os.unlink(tmp_path)

    async def query_document(self, query: str, k: int = 3) -> DocumentRetrievalResponse:
        """Query the vector store for relevant documents.
        
        Args:
            query (str): Query string to search for
            
        Returns:
            DocumentRetrievalResponse: Response containing matched documents
        """
        print(f"Querying vector store with: {query}")
        results = self._vector_store.similarity_search(query, k)
        return results
    
    async def upload_qna(self, qna: Qna) -> dict:
        """Upload a QnA pair to the vector store.
        
        Args:
            qna (Qna): Question and answer pair to upload
            
        Returns:
            DocumentRetrievalResponse: Response containing similar QnA pairs
        """
        print(f"Processing QnA upload - Question: {qna.question}")
        content = f"Questions: {qna.question}\n\nAnswer: {qna.answer}"
        self._vector_store.add_documents([Document(page_content=content, metadata={"source": "QnA"})])
        print("Added QnA to vector store")
        
        return {"message": "QnA uploaded successfully"}
