import pyautogui

def handle_gesture(action):
    if action == "move_cursor":
        pyautogui.moveTo(500, 500)
    elif action == "left_click":
        pyautogui.click()
    elif action == "right_click":
        pyautogui.click(button='right')
    elif action == "scroll":
        pyautogui.scroll(20)