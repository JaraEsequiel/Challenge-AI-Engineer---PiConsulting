# Pi Consulting RAG Project

A robust backend service built with FastAPI and modern Python technologies.

## 🚀 Features

- Built with FastAPI for high performance and easy API development
- Rich terminal output support
- Type safety with Pydantic
- LangGraph for workflow orchestration
- Store documents and QnA pairs in a vector database
- Allow users to enrich the AI Assistant with their interactions.
- Scaleable using a langgraph factory to setup different nodes without dependencies.

## 🛠️ Technologies

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- LangGraph
- Pinecone
- LangChain

## 🔧 Local Installation

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate # On Windows use: venv\Scripts\activate
```

2. Install the dependencies:

```bash
pip install -r requirements.txt

```

3. Visit the API documentation:
   - Swagger UI: http://localhost:8000/docs

## 🐳 Docker Setup

1. Build the Docker image:

```bash
docker build -t pi-consulting-rag .
```

2. Run the container:

```bash
docker run -p 8000:8000 pi-consulting-rag
```

3. Visit the API documentation:
   - Swagger UI: http://localhost:8000/docs

Note: When using Docker, you don't need to set up a virtual environment or install dependencies locally as everything is contained within the Docker container.

## 🚀 Quick Start

1. Start the server:

```bash
uvicorn main:app --reload
```

2. Visit the API documentation:
   - Swagger UI: http://localhost:8000/docs

## 📝 API Documentation

Once the server is running, you can access the interactive API documentation at:

- `/docs` - Swagger UI documentation
