from fastapi import APIRouter

router = APIRouter()


@router.get("/health", tags=["System"])
def health():
    return {
        "status": "online",
        "version": "0.1.0",
        "service": "VideoConverter API"
    }
    