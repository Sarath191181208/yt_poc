from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import video_routes
from app.config import VIDEO_DIR

app = FastAPI(title="Mini YouTube - HLS POC")

app.include_router(video_routes.router)
app.mount("/videos", StaticFiles(directory=VIDEO_DIR), name="videos")
