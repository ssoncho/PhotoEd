from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame)
from drawing_area import DrawingLayer, Viewer
class LayersPanel(QFrame):
    def __init__(self, viewer: Viewer):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QPushButton("+", clicked=self.add_layer_widget))
        self.setFixedHeight(200)
        self.setMaximumWidth(200)
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(1)
        
        self.viewer = viewer
        self.layers = {}
        self.last_layer_number = 1

    def add_layer_widget(self):
        layer_widget = LayerWidget(f"{self.last_layer_number} Layer")
        self.last_layer_number += 1
        self.viewer.add_drawing_layer()
        self.layers[layer_widget] = self.viewer.current_layer

        self.layout.addWidget(layer_widget)

    # def add_layer(self, layer):
    #     self.layers[layer_widget] = layer
    #     self.layout.addWidget(layer_widget)

    def remove_layer(self, layer_widget: QWidget):
        if layer_widget in self.layers.keys():
            del self.layers[layer_widget]
            self.layout.removeWidget(layer_widget)
            layer_widget.setParent(None)

class LayerWidget(QWidget):
    def __init__(self, layer_name=""):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.title = QLabel(layer_name)
        self.button = QPushButton()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.button)