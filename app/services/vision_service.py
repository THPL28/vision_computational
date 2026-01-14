import cv2
import numpy as np
import os
import logging
from typing import List, Dict, Any, Optional
from models.vision_model import VisionModel

logger = logging.getLogger(__name__)

class VisionService:
    """Enterprise-grade service for all Computer Vision operations."""
    
    _instance = None

    def __new__(cls):
        """Implement Singleton Pattern to prevent multiple model instances."""
        if cls._instance is None:
            cls._instance = super(VisionService, cls).__new__(cls)
            cls._instance.model = VisionModel()
            logger.info("VisionService initialized with Singleton model.")
        return cls._instance

    def detect_objects(self, image_path: str) -> Dict[str, Any]:
        """
        Detects objects in an image using YOLOv3.
        
        Args:
            image_path: Path to the local image file.
            
        Returns:
            A dictionary containing a list of detections with class and confidence.
        """
        try:
            image = cv2.imread(image_path)
            if image is None:
                return {"error": "Invalid image path"}
            
            detections = self.model.detect(image)
            return {"success": True, "detections": detections}
        except Exception as e:
            logger.error(f"Error in detect_objects: {e}")
            return {"error": str(e)}

    def generate_annotated_image(self, image_path: str, detections: List[Dict[str, Any]]) -> str:
        """
        Draws bounding boxes and labels on an image.
        
        Args:
            image_path: Path to the original image.
            detections: List of detection dictionaries.
            
        Returns:
            Path to the saved annotated image.
        """
        image = cv2.imread(image_path)
        for det in detections:
            x, y, w, h = det["box"]
            label = f"{det['class']} {det['confidence']:.2f}"
            # Material 3 Primary Color: D0BCFF (BGR: 255, 188, 208)
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 188, 208), 2)
            cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 188, 208), 2)
        
        output_path = image_path.replace(".", "_annotated.")
        cv2.imwrite(output_path, image)
        return output_path

    def process_video(self, video_path: str, output_path: str, mode: str = "detection") -> Optional[str]:
        """
        Processes a video file frame-by-frame for objects or motion.
        
        Args:
            video_path: Source video path.
            output_path: Target video path.
            mode: Either 'detection' or 'motion'.
            
        Returns:
            The output path if successful, None otherwise.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None

        # Get video properties
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30
        
        # Use mp4v codec for better browser compatibility
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        backSub = cv2.createBackgroundSubtractorMOG2()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if mode == "motion":
                fgMask = backSub.apply(frame)
                fgMask = cv2.dilate(fgMask, None, iterations=2)
                contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    if cv2.contourArea(contour) < 500:
                        continue
                    (x, y, w, h) = cv2.boundingRect(contour)
                    # Material 3 Tertiary: EFB8C8 (BGR: 200, 184, 239)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (200, 184, 239), 2)
            else:
                detections = self.model.detect(frame)
                for det in detections:
                    x, y, w, h = det["box"]
                    # Material 3 Primary: D0BCFF (BGR: 255, 188, 208)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 188, 208), 2)
                    cv2.putText(frame, det["class"], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 188, 208), 2)

            out.write(frame)

        cap.release()
        out.release()
        return output_path
