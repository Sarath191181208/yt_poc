from pathlib import Path
from fastapi import UploadFile
import shutil
from app.config import VIDEO_DIR

def save_upload(file: UploadFile) -> Path:
    dest = VIDEO_DIR / file.filename
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return dest
