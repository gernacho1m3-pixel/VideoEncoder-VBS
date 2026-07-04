from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

OUTPUT_FOLDER = Path("output")


@router.get("/download/{filename}")
def download(filename: str):

    file = OUTPUT_FOLDER / filename

    if not file.exists():
        return {"success": False, "message": "File tidak ditemukan atau sudah dihapus dari server."}

    return FileResponse(
        path=file,
        filename=file.name,
        media_type="application/octet-stream"
    )