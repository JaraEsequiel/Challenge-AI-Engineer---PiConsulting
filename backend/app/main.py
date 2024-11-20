# Import required FastAPI components
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import llm_routes, rag_routes

print("Initializing FastAPI application...")
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Frontend development server URL
    allow_credentials=True,  # Allow credentials (cookies, authorization headers)
    allow_methods=["*"],    # Allow all HTTP methods
    allow_headers=["*"],    # Allow all headers
)

print("Adding API route handlers...")
# Include routers for different API endpoints
app.include_router(llm_routes.router, prefix="/llm", tags=["LLM"])  # Language model routes
app.include_router(rag_routes.router, prefix="/rag", tags=["RAG"])  # Retrieval routes

# Root endpoint for basic health check
@app.get("/")
async def root():
    return {"message": "Hello World"}
