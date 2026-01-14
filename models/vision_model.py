# models/vision_model.py
import cv2
import numpy as np
import os

class VisionModel:
    def __init__(self, weights_path="yolov3.weights", cfg_path="yolov3.cfg", names_path="coco.names"):
        self.weights_path = weights_path
        self.cfg_path = cfg_path
        self.names_path = names_path
        self.classes = []
        self.net = None
        self._load_model()

    def _load_model(self):
        if os.path.exists(self.names_path):
            with open(self.names_path, "r") as f:
                self.classes = [line.strip() for line in f.readlines()]
        
        if os.path.exists(self.weights_path) and os.path.exists(self.cfg_path):
            self.net = cv2.dnn.readNet(self.weights_path, self.cfg_path)
            self.layer_names = self.net.getLayerNames()
            self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]
        else:
            print(f"Warning: YOLO files not found at {self.weights_path} or {self.cfg_path}")

    def detect_objects(self, image_path: str):
        if self.net is None:
            return {"error": "Model not loaded. Check weights and cfg files."}

        image = cv2.imread(image_path)
        if image is None:
            return {"error": "Could not read image."}

        height, width, _ = image.shape
        
        blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        
        class_ids = []
        confidences = []
        boxes = []
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(int(class_id))

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
        detections = []
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]]) if class_ids[i] < len(self.classes) else str(class_ids[i])
                detections.append({
                    "class": label,
                    "confidence": confidences[i],
                    "box": [x, y, w, h]
                })

        return {"detections": detections, "width": width, "height": height}

    def draw_detections(self, image_path: str, detections: list):
        image = cv2.imread(image_path) if isinstance(image_path, str) else image_path
        if image is None:
            return None
        
        for det in detections:
            x, y, w, h = det["box"]
            label = f"{det['class']} {det['confidence']:.2f}"
            color = (0, 255, 0) # Green
            cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
            cv2.putText(image, label, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            
        return image

    def detect_motion(self, frame, fgbg):
        fgmask = fgbg.apply(frame)
        # Limpar o ruído
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        
        # Encontrar contornos de movimento
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_boxes = []
        for contour in contours:
            if cv2.contourArea(contour) < 500: # Ignorar pequenos movimentos
                continue
            (x, y, w, h) = cv2.boundingRect(contour)
            motion_boxes.append([int(x), int(y), int(w), int(h)])
            
        return motion_boxes, fgmask

    def process_frame(self, frame):
        # Versão simplificada do detect_objects para frames de vídeo (numpy array)
        if self.net is None:
            return []

        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)
        
        class_ids = []
        confidences = []
        boxes = []
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.6: # Maior threshold para vídeo
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(int(class_id))

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        
        detections = []
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(self.classes[class_ids[i]]) if class_ids[i] < len(self.classes) else str(class_ids[i])
                detections.append({
                    "class": label,
                    "confidence": confidences[i],
                    "box": [x, y, w, h]
                })
        return detections
