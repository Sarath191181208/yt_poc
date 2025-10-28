from fastapi import APIRouter, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.file_service import save_upload
from app.services.hls_service import generate_hls
from app.config import VIDEO_DIR
import asyncio

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # list only original uploaded videos
    files = [f.name for f in VIDEO_DIR.glob("*") if f.is_file()]
    return templates.TemplateResponse("index.html", {"request": request, "files": files})

@router.post("/upload")
async def upload_video(file: UploadFile):
    path = save_upload(file)
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, generate_hls, path)
    return {"message": f"HLS generated for {file.filename}"}
