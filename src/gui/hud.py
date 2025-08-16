from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QColor, QPainter, QFont, QPaintEvent
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QWidget


class HUD(QWidget):
    def __init__(self):
        super().__init__()
        self.mode = "Default"
        self.active = False

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool) # type: ignore
        self.setAttribute(Qt.WA_TranslucentBackground) # type: ignore
        self.resize(250, 80)

        screen = QApplication.primaryScreen()
        if screen is not None:
            screen_geometry = screen.geometry()
            self.move(screen_geometry.width() - self.width() - 10, 10)
        else:
            self.move(100, 100)

        self.show()

    @pyqtSlot(str)
    def set_mode(self, mode_name):
        self.mode = mode_name
        self.update()

    @pyqtSlot(bool)
    def set_active(self, active):
        self.active = active
        self.update()

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QColor(0, 0, 0, 150))
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 10, 10)

        color = QColor(0, 255, 0) if self.active else QColor(255, 0, 0)
        painter.setBrush(color)
        painter.drawEllipse(15, 20, 20, 20)

        painter.setPen(QColor(255, 255, 255))
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        painter.drawText(50, 35, f"Mode: {self.mode}")
