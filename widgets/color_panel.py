from PyQt6.QtWidgets import (QLabel, QHBoxLayout, QFrame, QPushButton, QSlider, QSpinBox)
from PyQt6.QtGui import (QColor)
from PyQt6.QtCore import (Qt)

class ColorPanel(QFrame):
    def __init__(self, parent=None):
       super().__init__(parent)

       self.layout = QHBoxLayout(self)
       self.setFixedHeight(150)
       self.setFixedWidth(300)
       self.setFrameStyle(QFrame.Shape.Box)

       self.m_color_button = ColorButton(QColor(Qt.GlobalColor.black), self)
       self.m_color_button.setFixedSize(100, 100)
       self.layout.addWidget(self.m_color_button)

       self.m_slider = QSlider(Qt.Orientation.Vertical)
       self.m_slider.setMinimum(10)
       self.m_slider.setMaximum(20)
       self.layout.addWidget(self.m_slider)

       self.m_spin_box = QSpinBox()
       self.m_spin_box.setFixedSize(40, 25)
       self.m_spin_box.setMinimum(20)
       self.m_spin_box.setMaximum(50)
       self.m_spin_box.setSingleStep(2)
       self.layout.addWidget(self.m_spin_box)


    @property
    def color_button(self):
        return self.m_color_button

    @property
    def slider(self):
        return self.m_slider

    @property
    def spin_box(self):
        return self.m_spin_box
        

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