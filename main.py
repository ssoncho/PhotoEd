from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout)
import buttons
import drawing_area
from layers import LayersArea

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
        
        main_layout.addWidget(LayersArea())
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(drawing_area.DrawingArea())
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())