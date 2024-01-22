from PyQt6.QtWidgets import (QLabel, QVBoxLayout, QFrame, QPushButton)
from PyQt6.QtGui import (QColor)
from PyQt6.QtCore import (Qt)

class ColorPanel(QFrame):
    def __init__(self, parent=None):
       super().__init__(parent)

       self.layout = QVBoxLayout(self)
       self.setFixedHeight(200)
       self.setMaximumWidth(200)
       self.setFrameStyle(QFrame.Shape.Box)
       self.setLineWidth(1)

       self.m_color_button = ColorButton(QColor(Qt.GlobalColor.black))
       
       self.layout.addWidget(QLabel("Выбрать цвет"))
       self.layout.addWidget(self.m_color_button)

    @property
    def color_button(self):
        return self.m_color_button

class ColorButton(QPushButton):
    def __init__(self, color, parent=None):
       super().__init__(parent)
       self.setAutoFillBackground(True)
       self.setFixedSize(50, 50)

       self.m_color = color
       self.setStyleSheet("background-color: %s;" % color.name())
    
    @property
    def color(self):
        return self.m_color

    @color.setter
    def color(self, color):
        self.m_color = color
        self.setStyleSheet("background-color: %s;" % color.name())