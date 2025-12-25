from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import uuid
import os

router = APIRouter(prefix="/files", tags=["files"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Загрузить файл"""
    file_id = str(uuid.uuid4())
    file_extension = Path(file.filename).suffix
    file_path = UPLOAD_DIR / f"{file_id}{file_extension}"

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {
        "file_id": file_id,
        "filename": file.filename,
        "file_path": str(file_path),
        "size": len(content)
    }


@router.get("/download/{file_id}")
async def download_file(file_id: str):
    """Скачать файл по ID"""
    # Ищем файл по ID
    for file_path in UPLOAD_DIR.glob(f"{file_id}*"):
        if file_path.exists():
            return FileResponse(
                path=str(file_path),
                filename=file_path.name,
                media_type='application/octet-stream'
            )
    raise HTTPException(status_code=404, detail="File not found")