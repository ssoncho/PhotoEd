from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame)
from PyQt6.QtGui import QIcon
from drawing_area import DrawingLayer, Viewer
class LayersPanel(QFrame):
    def __init__(self, viewer: Viewer):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.m_add_layer_button = QPushButton("+", clicked=lambda: self.add_layer_widget(Viewer.DrawingLayer))
        self.layout.addWidget(self.m_add_layer_button)
        self.setFixedHeight(200)
        self.setMaximumWidth(200)
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(1)
        
        self.viewer = viewer
        self.layers = {}
        self.last_layer_number = 1

        self.m_current_layer_widget = None

    def add_layer_widget(self, layer):
        layer_widget = LayerWidget(f"{self.last_layer_number} Layer")
        layer_widget.button.clicked.connect(lambda: self.remove_layer(layer_widget))
        self.last_layer_number += 1
        self.m_current_layer_widget = layer_widget

        self.viewer.add_layer(layer)
        self.layers[layer_widget] = self.viewer.current_layer

        self.layout.addWidget(layer_widget)

    def remove_all_layers(self):
        for layer_widget in self.layers.keys():
            self.layers[layer_widget] = None
            self.layout.removeWidget(layer_widget)
            layer_widget.setParent(None)
        self.last_layer_number = 1
        self.m_current_layer_widget = None

    def remove_layer(self, layer_widget: QWidget):
        if layer_widget in self.layers.keys():
            self.viewer.remove_layer(self.layers[layer_widget])
            del self.layers[layer_widget]
            self.layout.removeWidget(layer_widget)
            layer_widget.setParent(None)

    @property
    def current_layer_widget(self):
        return self.m_current_layer_widget

    @property
    def add_layer_button(self):
        return self.m_add_layer_button

class LayerWidget(QWidget):
    def __init__(self, layer_name=""):
        super().__init__()
        self.layout = QHBoxLayout(self)
        self.title = QLabel(layer_name)
        self.button = QPushButton()
        self.button.setIcon(QIcon("img/delete.png"))
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.button)