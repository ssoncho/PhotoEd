from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import (Qt)
class FunctionalButton(QPushButton):
    def __init__(self, img_path="", text=""):
        super().__init__()
        self.setFixedSize(40, 40)
        self.setIcon(QIcon(img_path))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setText(text)