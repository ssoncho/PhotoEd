from PyQt6.QtWidgets import (QWidget, QHBoxLayout, QFrame, QPushButton)
from PyQt6.QtGui import (QColor)

class ColorPanel(QFrame):
   def __init__(self, colors: list[str], drawing_area):
       super().__init__()

       self.layout = QHBoxLayout(self)
       self.setFixedHeight(200)
       self.setMaximumWidth(200)
       self.setFrameStyle(QFrame.Shape.Box)
       self.setLineWidth(1)

       for color in colors:
           color_button = ColorButton(color)
           self.layout.addWidget(color_button)
           #color_button.pressed.connect(lambda color=color: drawing_area.set_pen_color(QColor(color)))


class ColorButton(QPushButton):
   def __init__(self, color):
       super().__init__()
       self.setAutoFillBackground(True)
       self.setFixedSize(40, 30)

       self.color = color
       self.setStyleSheet("background-color: %s;" % color)