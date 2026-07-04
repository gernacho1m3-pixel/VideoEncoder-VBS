from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router
from app.api.upload import router as upload_router
from app.api.metadata import router as metadata_router
from app.api.convert import router as convert_router
from app.api.download import router as download_router
from app.api.progress import router as progress_router

app = FastAPI(
    title="VideoConverter API",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(metadata_router)
app.include_router(convert_router)
app.include_router(download_router)
app.include_router(progress_router)

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "VideoConverter API is running."
    }