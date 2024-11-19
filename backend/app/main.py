from fastapi import FastAPI
from app.api.routes import llm_routes, rag_routes

app = FastAPI()

app.include_router(llm_routes.router, prefix="/llm", tags=["LLM"])
app.include_router(rag_routes.router, prefix="/rag", tags=["RAG"])

@app.get("/")
async def root():
    return {"message": "Hello World"}
