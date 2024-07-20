# app/services/vision_service.py
from models.vision_model import VisionModel
# app/services/vision_service.py
import cv2
import numpy as np
import traceback  # Importe o módulo traceback para obter informações de rastreamento de exceção
# app/services/vision_service.py
import cv2
import numpy as np
import traceback

class VisionService:
    def __init__(self):
        self.model = VisionModel()

    def detect_objects(self, image_path: str):
        try:
            image = cv2.imread(image_path)
            height, width, _ = image.shape
            
            # caminho para os arquivos YOLOv3 
            net = cv2.dnn.readNet("path_to_yolov3_weights/yolov3.weights", "path_to_yolov3_cfg/yolov3.cfg")
            
            layer_names = net.getLayerNames()
            output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
            
            blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            net.setInput(blob)
            outs = net.forward(output_layers)
            
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
                        class_ids.append(class_id)

            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
            result = {"boxes": boxes, "class_ids": class_ids, "confidences": confidences}
            return result
        except Exception as e:
            traceback.print_exc()
            return {"error": str(e)}
