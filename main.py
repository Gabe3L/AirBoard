import time

import cv2

from src.os import OS
from src.gesture_detection import GestureDetector
from src.mode_manager import ModeManager
from src.detection.yolo import YOLODetector

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

LABEL_COLOURS = {
    0: (0, 0, 255),
    1: (208, 224, 64),
    2: (0, 255, 255),
    3: (203, 192, 255),
    4: (255, 0, 255),
    5: (0, 225, 0),
    6: (0, 165, 225)
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

def perform_action(x, y, class_id: int, os: OS) -> None:
    label: str = LABELS[class_id]

    match label:
        case 'hand_open':
            os.left_mouse_up()
            os.move_mouse(x, y)
            return

        case 'hand_closed':
            os.left_mouse_up()
            return

        case 'hand_pinching':
            os.clicking = True
            os.move_mouse(x, y)
            os.left_mouse_down()
            return

        case 'two_fingers_up':
            os.move_mouse(x, y)
            os.right_mouse_click()
            return

        case 'thumbs_up':
            os.left_mouse_up()
            os.mouse_scroll('up')
            return

        case 'thumbs_down':
            os.left_mouse_up()
            os.mouse_scroll('down')
            return
        
        case 'three_fingers_down':
            os.open_start_menu()
            return

def main() -> None:
    cap = load_webcam()
    mediapipe_detector = GestureDetector()
    yolo_detector = YOLODetector()
    mode_manager = ModeManager()
    os = OS()

    screen_res = os.get_screen_res()
    
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

        x, y = mediapipe_detector.get_index_base_coords(screen_res)

        if box is not None and label is not None:
            perform_action(x, y, label, os)
            color = LABEL_COLOURS.get(label, (255, 255, 255))
            frame_for_display = cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), color, 2)
        
        frame_for_display = mediapipe_detector.draw(frame)
        
        cv2.imshow("AirBoard", frame_for_display)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

###############################################################

if __name__ == "__main__":
    main()
