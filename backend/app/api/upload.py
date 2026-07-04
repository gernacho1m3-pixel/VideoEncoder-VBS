from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File

router = APIRouter()

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)


@router.post("/upload", tags=["Upload"])
async def upload_video(file: UploadFile = File(...)):

    destination = UPLOAD_FOLDER / file.filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "success": True,
        "filename": file.filename,
        "message": "Upload completed"
    }