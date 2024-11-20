# Pi Consulting RAG Project - Frontend

A modern React frontend built with Vite, TypeScript, and Tailwind CSS.

## 🚀 Features

- Built with React 18 and TypeScript for robust type safety
- Vite for lightning-fast development and builds
- Tailwind CSS for utility-first styling
- ESLint configuration for code quality
- Docker support for containerized deployment
- Beautiful, production-ready UI components
- Lucide React for consistent iconography

## 🛠️ Technologies

Referenced from package.json:

```json
  "dependencies": {
    "dotenv": "^16.4.5",
    "lucide-react": "^0.344.0",
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  }
```

## 🔧 Local Installation

1. Install dependencies:

```bash
npm install
```


2. Start the development server:
```bash
npm run dev
```

## 🐳 Docker Setup

1. Build the Docker image:

```bash
docker build -t pi-consulting-rag-frontend .
```


2. Run the container:

```bash
docker run -p 80:80 pi-consulting-rag-frontend
```


The application will be available at http://localhost:80

## 📁 Project Structure

- `/src` - Source code directory
  - `/components` - React components
  - `/utils` - Utility functions and configurations
- `index.html` - Entry HTML file
- `tailwind.config.js` - Tailwind CSS configuration
- `vite.config.ts` - Vite configuration
- `tsconfig.json` - TypeScript configuration

