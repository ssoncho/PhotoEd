from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (QLabel)
from PyQt6.QtGui import (QPixmap, QPainter, QPen, QColor)
from PyQt6.QtCore import (Qt, QPoint, QLineF, QSize)

class DrawingArea(QLabel):
    def __init__(self):
        super().__init__()
        self.pixmap = QPixmap(self.size())
        self.pixmap.fill(Qt.GlobalColor.white)
        self.setPixmap(self.pixmap)
        self.last_x, self.last_y = None, None
        self.setMinimumSize(50,50)
        self.pen_color = Qt.GlobalColor.blue

    def set_pen_color(self, color: QColor):
        self.pen_color = color

    def mouseMoveEvent(self, e):
        if self.last_x is None: # First event.
            self.last_x = e.position().x()
            self.last_y = e.position().y()
            return # Ignore the first time.

        painter = QPainter(self.pixmap)
        pen = QPen(self.pen_color, 10)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)
        line = QLineF(self.last_x, self.last_y, e.position().x(), e.position().y())
        painter.drawLine(line)
        painter.end()
        self.setPixmap(self.pixmap)

        # Update the origin for next time.
        self.last_x = e.position().x()
        self.last_y = e.position().y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None

    def resizeEvent(self, e):
        newPixmap = self.pixmap.scaled(e.size())
        newPixmap.fill(Qt.GlobalColor.white)
        painter = QPainter(newPixmap)
        painter.drawPixmap(QPoint(), self.pixmap)
        self.pixmap = newPixmap

        self.setPixmap(self.pixmap)
        super().resizeEvent(e)