from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame)

class LayersArea(QWidget):
    def __init__(self):
        super().__init__()

        self.frame = QFrame(self)
        self.layout = QVBoxLayout(self)
        self.setFixedHeight(200)
        self.setMaximumWidth(200)

        self.layers = []
        self.add_layer(Layer("First Layer"))
        self.add_layer(Layer("Second Layer"))

    def add_layer(self, layer: QWidget):
        self.layers.append(layer)
        self.layout.addWidget(layer)

    def remove_layer(self, layer: QWidget):
        if layer in self.layers:
            self.layers.remove(layer)
            self.layout.removeWidget(layer)
            layer.setParent(None)

class Layer(QWidget):
    def __init__(self, text=""):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.title = QLabel(text)
        self.button = QPushButton()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.button)