from src.gui.hud_runner import HUDThread
from .actions import presenting, drawing, navigation
from PyQt5.QtCore import QObject, pyqtSignal

class ModeManager(QObject):
    mode_changed = pyqtSignal(str)
    active_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.current_mode = "Default"
        self.active = False
        self.previous_gesture: bool = False
        self.hud_thread = HUDThread()
        self.hud_thread.start()

    def activate_mode(self):
        self.active = True
        self.active_changed.emit(True)

    def deactivate_mode(self):
        self.active = False
        self.active_changed.emit(False)

    def set_mode(self, mode_name):
        self.current_mode = mode_name
        self.mode_changed.emit(mode_name)

    def process_mode(self, gesture, frame):
        if gesture != self.previous_gesture:
            print(gesture)
            self.previous_gesture = gesture        

        if gesture == "1_finger_up":
            self.set_mode("Present")
        elif gesture == "2_fingers_up":
            self.set_mode("Draw")
        elif gesture == "3_fingers_up":
            self.set_mode("Default")
        elif gesture == "thumbs_up":
            self.activate_mode()
        elif gesture == "thumbs_down":
            self.deactivate_mode()

        if self.current_mode == "Present":
            presenting.handle_gesture(gesture)
        elif self.current_mode == "Draw":
            drawing.handle_gesture(gesture, frame)
        elif self.current_mode == "Default":
            navigation.handle_gesture(gesture)