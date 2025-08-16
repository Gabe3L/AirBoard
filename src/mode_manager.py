import time
from threading import Timer, Lock
from functools import wraps

from src.gui.hud_runner import HUDThread
from PyQt5.QtCore import QObject, pyqtSignal

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

class ModeManager(QObject):
    mode_changed = pyqtSignal(str)
    active_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.current_mode = 0
        self.active = False
        self.previous_fingers_raised: bool = False
        self._toggle_pressed = False

        self.hud_thread = HUDThread()
        self.hud_thread.start()

        while self.hud_thread.hud is None:
            time.sleep(0.1)
            
        self.mode_changed.connect(self.hud_thread.hud.set_mode)
        self.active_changed.connect(self.hud_thread.hud.set_active)

    @cooldown(1.5, True)
    def activate_mode(self, active: bool):
        self.active = active
        self.active_changed.emit(active)

    @cooldown(0.5, True)
    def set_mode(self, mode: int):
        self.current_mode = mode
        mode_str = {0: "Default", 1: "Presentation", 2: "Drawing"}.get(mode, "Default")
        self.mode_changed.emit(mode_str)

    def process_mode(self, fingers_raised, frame):
        if fingers_raised != self.previous_fingers_raised:
            self.previous_fingers_raised = fingers_raised        

        if fingers_raised == 1:
            self.set_mode(0) # Default
        elif fingers_raised == 2:
            self.set_mode(1) # Presentation
        elif fingers_raised == 3:
            self.set_mode(2) # Drawing