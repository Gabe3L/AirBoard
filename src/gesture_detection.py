from typing import Tuple, Literal, Optional, Any

import mediapipe as mp
import cv2
import numpy as np

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands # type: ignore
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.mp_draw = mp.solutions.drawing_utils # type: ignore
        self.landmarks = None

    def detect(self, frame) -> Optional[Literal['1_finger', '2_fingers', '3_fingers']]:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(frame_rgb)
        gesture = None

        if result.multi_hand_landmarks:
            self.landmarks = result.multi_hand_landmarks[0]
            gesture = self.recognize_gesture(self.landmarks)

        return gesture

    def draw(self, frame: np.ndarray) -> np.ndarray:
        if self.landmarks:
            self.mp_draw.draw_landmarks(
                frame,
                self.landmarks,
                self.mp_hands.HAND_CONNECTIONS
            )
        return frame
    
    def get_index_base_coords(self, screen_res):
        if not self.landmarks:
            return None, None

        fingertip = self.landmarks.landmark[5]  # index finger base
        x_norm, y_norm = fingertip.x, fingertip.y
        
        x_screen = int(x_norm * screen_res[0])
        y_screen = int(y_norm * screen_res[1])
        
        return x_screen, y_screen
    
    def get_index_fingertip_coords(self, screen_res):
        if not self.landmarks:
            return None, None

        fingertip = self.landmarks.landmark[8]  # index finger tip
        x_norm, y_norm = fingertip.x, fingertip.y
        
        x_screen = int(x_norm * screen_res[0])
        y_screen = int(y_norm * screen_res[1])
        
        return x_screen, y_screen
    
    def get_thumb_coords(self, screen_res):
        if not self.landmarks:
            return None, None

        fingertip = self.landmarks.landmark[4]  # thumb tip
        x_norm, y_norm = fingertip.x, fingertip.y
        
        x_screen = int(x_norm * screen_res[0])
        y_screen = int(y_norm * screen_res[1])
        
        return x_screen, y_screen

    def recognize_gesture(self, hand_landmarks):
        finger_count = 0
        tips_ids = [4, 8, 12, 16, 20]
        landmarks = hand_landmarks.landmark

        if landmarks[tips_ids[1]].y < landmarks[tips_ids[1]-2].y:
            finger_count += 1
        if landmarks[tips_ids[2]].y < landmarks[tips_ids[2]-2].y:
            finger_count += 1
        if landmarks[tips_ids[3]].y < landmarks[tips_ids[3]-2].y:
            finger_count += 1

        if finger_count == 1:
            return "1_finger"
        elif finger_count == 2:
            return "2_fingers"
        elif finger_count == 3:
            return "3_fingers"
        else:
            return None
