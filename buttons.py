from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import (QSize, Qt)

class FunctionalButton(QPushButton):
    def __init__(self, parent, text=""):
        super().__init__(parent=parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setText(text)

class AddImageButton(FunctionalButton):
    def __init__(self, parent, text="Add image"):
        super().__init__(parent=parent, text=text)

class DrawFigureButton(FunctionalButton):
    def __init__(self, parent, text="Draw figure"):
        super().__init__(parent=parent, text=text)

class DrawButton(FunctionalButton):
    def __init__(self, parent, text="Draw"):
        super().__init__(parent=parent, text=text)

class EraseButton(FunctionalButton):
    def __init__(self, parent, text="Erase"):
        super().__init__(parent=parent, text=text)

class AddTextButton(FunctionalButton):
    def __init__(self, parent, text="Add text"):
        super().__init__(parent=parent, text=text)

class ChangeImageColorButton(FunctionalButton):
    def __init__(self, parent, text="Change image color"):
        super().__init__(parent=parent, text=text)

class CutImageButton(FunctionalButton):
    def __init__(self, parent, text="Cut image"):
        super().__init__(parent=parent, text=text)

class UndoButton(FunctionalButton):
    def __init__(self, parent, text="Undo"):
        super().__init__(parent=parent, text=text)

class RedoButton(FunctionalButton):
    def __init__(self, parent, text="Redo"):
        super().__init__(parent=parent, text=text)

class SaveButton(FunctionalButton):
    def __init__(self, parent, text="Save"):
        super().__init__(parent=parent, text=text)