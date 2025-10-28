from fastapi import APIRouter, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.file_service import save_upload
from app.services.transcoding_service import transcode_video
from app.config import VIDEO_DIR
import asyncio

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    files = []
    for f in VIDEO_DIR.glob("*"):
        if f.is_file() and f.suffix in [".mp4", ".mov", ".mkv"]:
            files.append(f.name)
    return templates.TemplateResponse("index.html", {"request": request, "files": files})

@router.post("/upload")
async def upload_video(file: UploadFile):
    path = save_upload(file)

    # Run transcoding in a background thread (non-blocking)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, transcode_video, path)

    return {"message": f"Uploaded and transcoded {file.filename}"}
