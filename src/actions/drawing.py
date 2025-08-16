import cv2

last_point = None

def handle_gesture(action, frame):
    global last_point
    if action == "draw":
        fingertip = (100, 100)
        if last_point is None:
            last_point = fingertip
        cv2.line(frame, last_point, fingertip, (0,0,255), 5)
        last_point = fingertip
    elif action == "erase":
        print("Erasing...")
    elif action == "clear_all":
        frame[:] = 0
