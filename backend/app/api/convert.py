from pathlib import Path

from fastapi import APIRouter
from pydantic import BaseModel
from app.services.task_service import run_background

from app.services.ffmpeg_service import convert_video
from app.services.cleanup_service import delete_later

router = APIRouter()


class ConvertRequest(BaseModel):
    filename: str
    output_format: str
    vcodec: str
    resolution: str
    fps: int
    vbitrate: int
    abitrate: int

def worker(req):

    output_file = convert_video(
        req.filename,
        req.output_format,
        req.vcodec,
        req.resolution,
        req.fps,
        req.vbitrate,
        req.abitrate
    )

    upload_file = Path("uploads") / req.filename
    output_path = Path("output") / output_file

    delete_later(upload_file)
    delete_later(output_path)


@router.post("/convert")
def convert(req: ConvertRequest):

    run_background(
        req.filename,
        worker,
        req
    )

    return {
        "success": True,
        "started": True
    }