import time
from typing import List

import cv2

from src.windows import Windows
from src.gesture_detection import GestureDetector
from src.mode_manager import ModeManager
from src.calibration import Calibration
from src.detection.yolo import YOLODetector
from src.display import VideoDisplay

###############################################################

LABELS = {
    0: 'hand_closed',
    1: 'hand_open',
    2: 'hand_pinching',
    3: 'three_fingers_down',
    4: 'thumbs_down',
    5: 'thumbs_up',
    6: 'two_fingers_up',
}

###############################################################

def load_webcam() -> cv2.VideoCapture:
    cap = None
    for _ in range(500):
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            break
        else:
            time.sleep(0.3)
    if cap is None or not cap.isOpened():
        print("Webcam not found.")
        raise RuntimeError("Webcam initialization failed.")
    return cap

def perform_action(x, y, class_id: int, windows: Windows) -> None:
    label: str = LABELS[class_id]

    match label:
        case 'hand_open':
            windows.left_mouse_up()
            windows.move_mouse(x, y)
            return

        case 'hand_closed':
            windows.left_mouse_up()
            return

        case 'hand_pinching':
            windows.clicking = True
            windows.move_mouse(x, y)
            windows.left_mouse_down()
            return

        case 'two_fingers_up':
            windows.move_mouse(x, y)
            windows.right_mouse_click()
            return

        case 'thumbs_up':
            windows.left_mouse_up()
            windows.mouse_scroll('up')
            return

        case 'thumbs_down':
            windows.left_mouse_up()
            windows.mouse_scroll('down')
            return
        
        case 'three_fingers_down':
            windows.open_start_menu()
            return

def main() -> None:
    cap = load_webcam()
    mediapipe_detector = GestureDetector()
    yolo_detector = YOLODetector()
    mode_manager = ModeManager()
    windows = Windows()

    screen_res = windows.get_screen_res()
    
    calib = Calibration()
    calib.load_homography()

    print("AirBoard running. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        frame_for_inference = frame.copy()

        gesture = mediapipe_detector.detect(frame_for_inference)
        mode_manager.process_mode(gesture, frame)

        boxes, confidences, class_ids = yolo_detector.detect(frame_for_inference)
        detection = yolo_detector.most_confident_box(boxes.tolist(), confidences.tolist(), class_ids.tolist())
        box, label = detection if detection else (None, None)
        
        frame_for_display = frame.copy()

        if box is not None and label is not None:
            x, y = mediapipe_detector.get_fingertip_coords(screen_res)
            perform_action(x, y, label, windows)
            frame_for_display = VideoDisplay.annotate_frame(frame, box, label)
        frame_for_display = mediapipe_detector.draw(frame)
        
        cv2.imshow("AirBoard", frame_for_display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

###############################################################

if __name__ == "__main__":
    main()
