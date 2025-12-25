from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
import asyncio
import json
from datetime import datetime
from typing import List, Dict
from app.backend.api.dependencies import get_agent

router = APIRouter(prefix="/ws", tags=["chat"])

messages_store: Dict[str, List[Dict]] = {}
threads: Dict[str, Dict] = {}

@router.websocket("/{thread_id}")
async def chat_stream(websocket: WebSocket,
                      thread_id: str,
                      service = Depends(get_agent, scope="app")):
    await websocket.accept()

    # Инициализируем тред если не создан ранее
    if thread_id not in threads:
        threads[thread_id] = {
            "id": thread_id,
            "title": "Новый чат",
            "updated_at": datetime.now().isoformat(),
        }

    try:
        while True:
            raw = await websocket.receive_text()
            message_data = json.loads(raw)

            # Сообщение пользователя
            content = message_data.get("message", "")
            response = ""
            async for token in service.astream_messages(content=content, thread_id=thread_id):
                response += token
                await websocket.send_json({
                    "type": "stream",
                    "data": {"role": "assistant", "content": token}
                })

            assistant_message = {
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat(),
            }

            # Финальное сообщение
            await websocket.send_json({
                "type": "message_complete",
                "data": assistant_message
            })

    except WebSocketDisconnect:
        print(f"WebSocket disconnected: {thread_id}")
