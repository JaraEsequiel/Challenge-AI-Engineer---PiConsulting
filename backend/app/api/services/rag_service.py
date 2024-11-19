from fastapi import UploadFile
import shutil
import os

class RAGService:
    async def upload_document(self, file: UploadFile) -> dict:
        file_location = f"uploaded_files/{file.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(file.file, file_object)
        return {"filename": file.filename, "size": os.path.getsize(file_location)}
