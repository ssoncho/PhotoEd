from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import (Qt)
class FunctionalButton(QPushButton):
    def __init__(self, text=""):
        super().__init__()
        self.setFixedSize(30, 30)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setText(text)

class AddImageButton(FunctionalButton):
    def __init__(self, text="Add image"):
        super().__init__(text=text)

class DrawFigureButton(FunctionalButton):
    def __init__(self, text="Draw figure"):
        super().__init__(text=text)

class EraseButton(FunctionalButton):
    def __init__(self, text="Erase"):
        super().__init__(text=text)

class AddTextButton(FunctionalButton):
    def __init__(self, text="Add text"):
        super().__init__(text=text)

class CutImageButton(FunctionalButton):
    def __init__(self, text="Cut image"):
        super().__init__(text=text)

class UndoButton(FunctionalButton):
    def __init__(self, text="Undo"):
        super().__init__(text=text)

class RedoButton(FunctionalButton):
    def __init__(self, text="Redo"):
        super().__init__(text=text)

class SaveButton(FunctionalButton):
    def __init__(self, text="Save"):
        super().__init__(text=text)