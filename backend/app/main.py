from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import llm_routes, rag_routes
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(llm_routes.router, prefix="/llm", tags=["LLM"])
app.include_router(rag_routes.router, prefix="/rag", tags=["RAG"])

@app.get("/")
async def root():
    return {"message": "Hello World"}
