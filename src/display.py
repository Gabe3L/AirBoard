import cv2
import numpy as np
from typing import List


LABEL_COLOURS = {
    0: (0, 0, 255),
    1: (208, 224, 64),
    2: (0, 255, 255),
    3: (203, 192, 255),
    4: (255, 0, 255),
    5: (0, 225, 0),
    6: (0, 165, 225)
}

class VideoDisplay:
    @staticmethod
    def show_frame(window_name: str, frame: np.ndarray) -> None:
        cv2.imshow(window_name, frame)

    @staticmethod
    def annotate_frame(frame: np.ndarray, box: List[int], class_id: int) -> np.ndarray:
        color = LABEL_COLOURS.get(class_id, (255, 255, 255))
        return cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 2)

    @staticmethod
    def insert_text_onto_frame(frame: np.ndarray, message: str, row: int) -> np.ndarray:
        if message:
            cv2.putText(frame, message, (10, (30 + (row * 50))),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 2)
        
        return frame