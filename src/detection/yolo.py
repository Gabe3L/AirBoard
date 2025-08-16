import os
import sys
from typing import Tuple, List, Optional

import torch
import numpy as np

###############################################################

CONFIDENCE_THRESHOLD: float = 0.6

LABELS = {
    0: 'hand_closed',
    1: 'hand_open',
    2: 'hand_pinching',
    3: 'three_fingers_down',
    4: 'thumbs_down',
    5: 'thumbs_up',
    6: 'two_fingers_up',
}


class YOLODetector:
    def __init__(self) -> None:
        self._suppress_output()
        from ultralytics import YOLO
        self._restore_output()
        self.device: torch.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')
        self.model: YOLO = YOLO("train\\weights\\windows_best.engine" if torch.cuda.is_available(
        ) else "train\\weights\\windows_best.onnx", task='detect')

    def _suppress_output(self):
        self._stdout = sys.stdout
        self._stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

    def _restore_output(self):
        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = self._stdout
        sys.stderr = self._stderr

    def detect(self, frame: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        with torch.no_grad():
            self._suppress_output()
            results = self.model.predict(frame)[0]
            self._restore_output()
        return self.extract_detections(results)

    def extract_detections(self, results) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        boxes: List[List[int]] = []
        confidences: List[float] = []
        class_ids: List[int] = []

        for box in results.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
            confidence: float = float(box.conf[0])

            if confidence >= CONFIDENCE_THRESHOLD:
                boxes.append([x1, y1, x2, y2])
                confidences.append(confidence)
                class_ids.append(int(box.cls[0]))

        return np.array(boxes), np.array(confidences), np.array(class_ids)

    def most_confident_box(self, boxes: List[List[int]], confidences: List[float], class_ids: List[int]) -> Optional[Tuple[List[int], int]]:
        if not confidences:
            return None

        max_index = np.argmax(confidences)
        box = boxes[max_index]
        label = class_ids[max_index]

        return box, label

    def find_box_center(self, box: List[int], webcam_to_screen_ratio, screen_res) -> Tuple[int, int]:
        x0, y0, x1, y1 = box
        x = (x0 + x1) // 2
        y = (y0 + y1) // 2

        x = max(
            0, min(int(x * webcam_to_screen_ratio[0]), screen_res[0] - 1))
        y = max(
            0, min(int(y * webcam_to_screen_ratio[1]), screen_res[1] - 1))

        return x, y
