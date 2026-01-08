# PptxAgent

AI-powered agent system for generating and managing PowerPoint presentations with interactive chat capabilities.

## Features

- Interactive chat interface with AI agents
- File upload and processing for PPTX files
- Real-time WebSocket communication
- Agent-based workflow management (planner and research agents)
- Persistent conversation state with Redis
- Modern web UI built with Next.js

## Tech Stack

### Backend
- FastAPI (Python web framework)
- LangChain & LangGraph for AI workflows
- Redis for checkpointer state management
- WebSocket support for real-time chat
- UV for dependency management

### Frontend
- Next.js 16 with React 19
- TypeScript
- Tailwind CSS for styling
- WebSocket client for real-time communication

## Prerequisites

- Docker and Docker Compose
- Git

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd PptxAgent
```

2. Start all services using Docker Compose:
```bash
docker-compose up --build
```

This will start:
- Backend API on http://localhost:8000
- Frontend on http://localhost:3000
- Redis Stack on localhost:6379

## Usage

1. Open your browser and navigate to http://localhost:3000
2. Upload PPTX files through the file endpoint
3. Start chatting with the AI agents via the WebSocket interface
4. Agents will help generate and manage PowerPoint presentations

## API Endpoints

### REST Endpoints
- `POST /api/files/upload` - Upload PPTX files
- `GET /api/users` - User management

### WebSocket
- `ws://localhost:8000/ws/{thread_id}` - Real-time chat with agents

## Development

### Backend
```bash
cd backend
uv sync
uv run uvicorn app.backend.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Create a `.env` file in the backend directory with:
```
# Add your environment variables here
# Example: OPENAI_API_KEY=your_key_here
```

## Project Structure

```
PptxAgent/
├── backend/
│   ├── app/backend/
│   │   ├── api/endpoints/    # API routes
│   │   ├── services/         # Business logic
│   │   └── main.py           # FastAPI app
│   ├── src/
│   │   ├── agents/           # AI agents (planner, research)
│   │   ├── tools/            # Agent tools
│   │   └── utils/            # Utilities
│   └── Dockerfile
├── frontend/
│   ├── app/                  # Next.js app directory
│   ├── components/           # React components
│   └── Dockerfile
└── docker-compose.yml
```