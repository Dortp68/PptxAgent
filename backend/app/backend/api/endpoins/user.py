from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from app.backend.api.dependencies import get_db
from typing import List, Dict
from datetime import datetime

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/threads", response_model=List[Dict[str, str]])
async def get_threads(request: Request,
                      service = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return JSONResponse(
            {"error": "user_id not found in cookies"},
            status_code=400
        )
    try:
        threads = await service.get_user_threads(user_id)
        return threads
    except Exception as e:
        request.app.state.logger.error(e)
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )

@router.post("/threads/{thread_id}")
async def create_thread(request: Request,
                        thread_id: str,
                        service = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return JSONResponse(
            {"error": "user_id not found in cookies"},
            status_code=400
        )
    try:
        await service.add_thread_to_user(user_id, thread_id)
        thread = {"thread_id": thread_id, "created_at": datetime.now().isoformat()}
        return thread
    except Exception as e:
        request.app.state.logger.error(e)
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )


@router.get("/threads/{thread_id}")
async def get_thread(request: Request,
                     thread_id: str,
                     service = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return JSONResponse(
            {"error": "user_id not found in cookies"},
            status_code=400
        )
    try:
        response = await service.user_has_thread(user_id, thread_id)
        if response:
            history = [msg async for msg in request.app.state.agent.aget_history(thread_id)]
            return history

        else:
            return JSONResponse(
                {"error": "This thread does not belong to this user"},
                status_code=400
            )

    except Exception as e:
        request.app.state.logger.error(e)
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )

@router.delete("/threads/{thread_id}")
async def delete_thread(request: Request,
                        thread_id: str,
                        service = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return JSONResponse(
            {"error": "user_id not found in cookies"},
            status_code=400
        )
    try:
        await request.app.state.agent.adelete_thread(thread_id)
        await service.remove_thread_from_user(user_id=user_id, thread_id=thread_id)
        return JSONResponse(
            status_code=200,
            content={"status": "deleted"}
        )
    except Exception as e:
        request.app.state.logger.error(e)
        return JSONResponse(
            status_code=400,
            content={"error": str(e)}
        )