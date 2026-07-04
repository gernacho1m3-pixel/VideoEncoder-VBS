from pathlib import Path

from fastapi import APIRouter, HTTPException

from app.services.ffprobe_service import get_video_metadata

router = APIRouter()

UPLOAD_FOLDER = Path("uploads")


@router.get("/metadata/{filename}")
def metadata(filename: str):

    video = UPLOAD_FOLDER / filename

    if not video.exists():
        raise HTTPException(404, "Video not found")

    return get_video_metadata(str(video))
