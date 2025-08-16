import sys
import threading
from PyQt5.QtWidgets import QApplication
from .hud import HUD

class HUDThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.app = None
        self.hud = None

    def run(self):
        self.app = QApplication(sys.argv)
        self.hud = HUD()
        sys.exit(self.app.exec_())

    def set_mode(self, mode):
        if self.hud:
            self.hud.set_mode(mode)

    def activate_mode(self):
        if self.hud:
            self.hud.activate_mode()

    def deactivate_mode(self):
        if self.hud:
            self.hud.deactivate_mode()
