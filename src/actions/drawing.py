from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QPainter, QPen, QPaintEvent
import sys
import threading

class DrawingOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool) # type: ignore
        self.setAttribute(Qt.WA_TranslucentBackground) # type: ignore
        self.setAttribute(Qt.WA_NoSystemBackground, True) # type: ignore
        self.setAttribute(Qt.WA_TransparentForMouseEvents)  # type: ignore

        screen = QApplication.primaryScreen()
        if screen is not None:
            geometry = screen.geometry()
            self.setGeometry(geometry)

        self.points = []
        self.pen_color = QColor(0, 0, 0)
        self.pen_width = 10

        self.show()

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(self.pen_color, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin) # type: ignore
        painter.setPen(pen)

        for point in self.points:
            painter.drawPoint(point)

    def draw_point(self, coords):
        self.points.append(QPoint(coords))
        self.update()

    def clear(self):
        self.points = []
        self.update()

class OverlayThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.overlay = None
        self.started_event = threading.Event()

    def run(self):
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.overlay = DrawingOverlay()
        self.started_event.set()
        sys.exit(self.app.exec_())