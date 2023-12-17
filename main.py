from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout)
import buttons
from drawing_area import DrawingArea
from layers import LayersArea
from color_panel import (ColorPanel)

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.setGeometry(50, 50, 300, 300)
        self.setWindowTitle('PhotoEd')
        main_container = QtWidgets.QWidget()
        main_layout = QHBoxLayout()
        buttons_layout = QVBoxLayout()
        drawing_settings_layout = QVBoxLayout()

        buttons_layout.addWidget(buttons.AddImageButton())
        buttons_layout.addWidget(buttons.DrawFigureButton())
        buttons_layout.addWidget(buttons.DrawButton())
        buttons_layout.addWidget(buttons.EraseButton())
        buttons_layout.addWidget(buttons.AddTextButton())
        buttons_layout.addWidget(buttons.ChangeImageColorButton())
        buttons_layout.addWidget(buttons.CutImageButton())
        buttons_layout.addWidget(buttons.UndoButton())
        buttons_layout.addWidget(buttons.RedoButton())
        buttons_layout.addWidget(buttons.SaveButton())

        drawing_area = DrawingArea()
        color_panel = ColorPanel(['red', 'green', 'blue'], drawing_area)
        drawing_settings_layout.addWidget(color_panel)
        drawing_settings_layout.addWidget(LayersArea())
        
        main_layout.addLayout(drawing_settings_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(drawing_area)
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())