# app/routers/vision.py
from fastapi import APIRouter, UploadFile, File
from app.services.vision_service import VisionService

router = APIRouter()
vision_service = VisionService()

@router.post("/detect-objects/")
async def detect_objects(file: UploadFile = File(...)):
    contents = await file.read()
    image_path = f"temp_{file.filename}"
    with open(image_path, 'wb') as f:
        f.write(contents)

    result = vision_service.detect_objects(image_path)
    return result
