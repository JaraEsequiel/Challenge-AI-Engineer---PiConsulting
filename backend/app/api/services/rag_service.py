from fastapi import UploadFile
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import Docx2txtLoader
from langchain_core.documents import Document
from app.schemas.document import DocumentResponse, DocumentRetrievalResponse
import os
import tempfile
from app.api.core.config import settings


class RAGService:
    _vector_store: PineconeVectorStore
    _embeddings: OpenAIEmbeddings

    def __init__(self):

        self._embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=settings.get("OPENAI_API_KEY"))
        self._vector_store = PineconeVectorStore(pinecone_api_key=settings.get("PINECONE_API_KEY"), index_name="piconsulting", embedding=self._embeddings)

    def _identify_source_type(self, text: str) -> str:
        # Identificar el tipo de contenido basado en palabras clave
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
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp_file:
            # Write uploaded file content to temporary file
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name

        try:
            # Load document from temporary file
            loader = Docx2txtLoader(tmp_path)
            data = loader.load()

            chunks = data[0].page_content.split('\n\n')

            for chunk in chunks:
                document = Document(page_content=chunk, metadata={"source": self._identify_source_type(chunk)})
                self._vector_store.add_documents([document])
            
            return {"filename": file.filename, "size": len(content)}
        finally:
            # Clean up temporary file
            os.unlink(tmp_path)

    async def query_document(self, query: str) -> DocumentRetrievalResponse:
        print(self._vector_store.similarity_search(query, k=3))
        return {"documents": self._vector_store.similarity_search(query, k=3)}
