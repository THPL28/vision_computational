# app/routers/vision.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.vision_service import VisionService
import os
import shutil
import uuid

router = APIRouter(tags=["Vision"])
vision_service = VisionService()

# Ensure temp directory exists
TEMP_DIR = "static/uploads"
os.makedirs(TEMP_DIR, exist_ok=True)

@router.post("/detect-objects/")
async def detect_objects(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    image_path = os.path.join(TEMP_DIR, unique_filename)

    try:
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = vision_service.detect_objects(image_path)
        
        if "error" in result:
            return result

        # Generate annotated image
        annotated_filename = f"annotated_{unique_filename}"
        annotated_path = os.path.join(TEMP_DIR, annotated_filename)
        
        # We need to save it where it can be served
        annotated_image_path = vision_service.generate_annotated_image(image_path, result["detections"])
        if annotated_image_path:
            # Move to TEMP_DIR if it's not already there
            if os.path.exists(annotated_image_path):
                shutil.move(annotated_image_path, annotated_path)
        
        return {
            "success": True,
            "filename": unique_filename,
            "original_url": f"/static/uploads/{unique_filename}",
            "annotated_url": f"/static/uploads/{annotated_filename}",
            "detections": result["detections"]
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.post("/detect-video/")
async def detect_video(file: UploadFile = File(...), mode: str = "detection"):
    if not file.content_type.startswith("video/"):
        raise HTTPException(status_code=400, detail="File must be a video.")

    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    video_path = os.path.join(TEMP_DIR, unique_filename)
    output_filename = f"processed_{mode}_{unique_filename}.mp4"
    output_path = os.path.join(TEMP_DIR, output_filename)

    try:
        with open(video_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Process video (This is synchronous for now, but in a real-world app it should be background)
        processed_path = vision_service.process_video(video_path, output_path, mode=mode)
        
        if not processed_path:
            return {"success": False, "error": "Could not process video"}

        return {
            "success": True,
            "filename": unique_filename,
            "original_url": f"/static/uploads/{unique_filename}",
            "processed_url": f"/static/uploads/{output_filename}",
            "mode": mode
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
