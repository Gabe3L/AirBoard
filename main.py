from src.gesture_detection import GestureDetector
from src.mode_manager import ModeManager
from src.calibration import Calibration
import cv2

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not found.")
        return

    detector = GestureDetector()
    mode_manager = ModeManager()

    calib = Calibration()
    calib.load_homography()

    print("AirBoard running. Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)

        gesture = detector.detect(frame)

        mode_manager.process_gesture(gesture, frame)

        cv2.imshow("AirBoard", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
