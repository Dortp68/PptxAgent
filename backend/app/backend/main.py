from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from langchain.messages import HumanMessage
from langgraph.types import Command
from app.backend.api.endpoins.user import router as users_router
from app.backend.api.endpoins.file import router as file_router
from app.backend.services.agent import Agent

from contextlib import asynccontextmanager
from datetime import datetime

@asynccontextmanager
async def lifespan(app: FastAPI):
    from src.checkpointer import init_checkpointer
    from src.utils import logger, langsmith_
    app.state.checkpointer = await init_checkpointer()
    app.state.logger = logger
    langsmith_()
    app.state.agent = Agent(checkpointer=app.state.checkpointer)
    yield
    #Close checkpointer connection

app = FastAPI(lifespan=lifespan)

# CORS настройки
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(file_router)

@app.websocket("/ws/{thread_id}")
async def chat_stream(websocket: WebSocket,
                      thread_id: str):
    await websocket.accept()


    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type", "message")
            content = data.get("content")
            app.state.logger.info(f"Received message: {message_type} ___ {content}")

            if message_type == "message":
                message = {"messages": [HumanMessage(content=content)]}
            elif message_type == "decision":
                message = Command(resume=content)
            else:
                await websocket.send_json({"error": "Invalid message type"})
                continue

            full_response = ""
            async for event_type, event_data in app.state.agent._astream(thread_id=thread_id, message=message):
                app.state.logger.info(f"Received event: {event_type} ___ {event_data}")
                if event_type == "assistant":
                    full_response += event_data
                    await websocket.send_json({
                        "type": "stream",
                        "data": {"role": "assistant", "content": event_data}})
                elif event_type == "interrupt":
                    await websocket.send_json({
                        "type": "interrupt",
                        "data": event_data})
                    break
                else:
                    await websocket.send_json({
                        "type": event_type,
                        "data": event_data})

            assistant_message = {
                "role": "assistant",
                "content": full_response,
                "timestamp": datetime.now().isoformat(),
            }

            await websocket.send_json({
                "type": "message_complete",
                "data": assistant_message
            })

    except WebSocketDisconnect:
        print(f"WebSocket disconnected: {thread_id}")
