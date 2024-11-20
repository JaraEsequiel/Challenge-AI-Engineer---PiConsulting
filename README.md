# Pi Consulting RAG Project

A modern full-stack application with React frontend and FastAPI backend for RAG (Retrieval Augmented Generation).

## 🌟 Overview

This project consists of:
- A React frontend built with TypeScript and Tailwind CSS
- A FastAPI backend with LangGraph for workflow orchestration
- Docker support for easy deployment

## 🚀 Features

### Frontend
- React 18 with TypeScript for type safety
- Vite for fast development
- Tailwind CSS for styling
- Interactive chat interface
- Message reactions and editing
- Real-time API integration

### Backend
- FastAPI for high-performance API
- LangGraph for workflow orchestration
- Vector database storage for documents and QnA
- Rich terminal logging
- Swagger UI documentation

## 🛠️ Quick Start with Docker Compose

1. Clone the repository:

2. Create a `.env` file in the root directory with your environment variables:
```bash
cp .env.example .env
```

3. Start the application using Docker Compose:
```bash
docker compose up -d
```

4. Access the application:
- Frontend: http://localhost:80
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## 📁 Project Structure

```
pi-consulting-rag/
├── frontend/          # React frontend application
├── backend/           # FastAPI backend service
├── docker-compose.yml # Docker Compose configuration
└── README.md         # Project documentation
```

## 🔧 Development

For local development without Docker, please refer to the README files in the respective frontend and backend directories:
- [Frontend Development Guide](./frontend/README.md)
- [Backend Development Guide](./backend/README.md)