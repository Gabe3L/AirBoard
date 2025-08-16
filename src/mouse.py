import time
from threading import Timer, Lock
from functools import wraps
from typing import Tuple
from pynput.mouse import Controller as MouseController, Button
from pynput.keyboard import Controller as KeyboardController, Key

def cooldown(cooldown_seconds: float, one_run: bool = True):
    def decorator(func):
        lock = Lock()
        cooldown_active = False
        cooldown_timer = None

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            nonlocal cooldown_active, cooldown_timer

            with lock:
                if cooldown_active:
                    return None
                
                result = func(self, *args, **kwargs)

                def reset_cooldown():
                    nonlocal cooldown_active
                    with lock:
                        cooldown_active = False
                
                if one_run:
                    cooldown_active = True
                    cooldown_timer = Timer(cooldown_seconds, reset_cooldown)
                    cooldown_timer.start()
                else:
                    if cooldown_timer is not None:
                        cooldown_timer.cancel()
                    cooldown_active = True
                    cooldown_timer = Timer(cooldown_seconds, reset_cooldown)
                    cooldown_timer.start()

                return result
        return wrapper
    return decorator

class Mouse:
    def __init__(self) -> None:
        self.clicking = False
        self.mouse = MouseController()
        self.keyboard = KeyboardController()

    def get_cursor_pos(self) -> Tuple[int, int]:
        pos = self.mouse.position
        return int(pos[0]), int(pos[1])

    def get_screen_res(self) -> Tuple[int, int]:
        try:
            import tkinter as tk
            root = tk.Tk()
            width = root.winfo_screenwidth()
            height = root.winfo_screenheight()
            root.destroy()
            return width, height
        except ImportError:
            return 1920, 1080

    def get_webcam_to_screen_ratio(self, screen_res: Tuple[int, int], camera_res: Tuple[int, int]) -> Tuple[float, float]:
        return (screen_res[0] / screen_res[1], camera_res[0] / camera_res[1])

    def move_mouse(self, cursor: Tuple[int, int]) -> None:
        self.mouse.position = (cursor)

    def mouse_scroll(self, direction: str) -> None:
        if direction == 'up':
            self.mouse.scroll(0, 2)
        elif direction == 'down':
            self.mouse.scroll(0, -2)

    @cooldown(1.5, one_run=False)
    def left_mouse_down(self) -> None:
        self.mouse.press(Button.left)
        self.clicking = True

    def left_mouse_up(self) -> None:
        if self.clicking:
            self.mouse.release(Button.left)
            self.clicking = False

    @cooldown(2.0, one_run=True)
    def right_mouse_click(self) -> None:
        self.mouse.click(Button.right)

    @cooldown(2.0, one_run=True)
    def open_start_menu(self) -> None:
        self.keyboard.press(Key.cmd)
        time.sleep(0.05)
        self.keyboard.release(Key.cmd)