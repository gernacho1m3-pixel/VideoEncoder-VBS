from fastapi import APIRouter

from app.services.progress_service import get_progress

router = APIRouter()


@router.get("/progress/{filename}")
def progress(filename: str):

    return {
        "progress": get_progress(filename)
    }
