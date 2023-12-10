from PyQt6 import QtWidgets
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton)
import buttons
import drawing_area

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        self.setGeometry(50, 50, 300, 300)
        self.setWindowTitle('PhotoEd')
        widget = QtWidgets.QWidget()
        layout = QVBoxLayout()
        layout.addWidget(buttons.AddImageButton(self))
        layout.addWidget(buttons.DrawFigureButton(self))
        layout.addWidget(buttons.DrawButton(self))
        layout.addWidget(buttons.EraseButton(self))
        layout.addWidget(buttons.AddTextButton(self))
        layout.addWidget(buttons.ChangeImageColorButton(self))
        layout.addWidget(buttons.CutImageButton(self))
        layout.addWidget(buttons.UndoButton(self))
        layout.addWidget(buttons.RedoButton(self))
        layout.addWidget(buttons.SaveButton(self))
        layout.addWidget(drawing_area.DrawingArea())
        widget.setLayout(layout)
        self.setCentralWidget(widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())