from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QScrollArea)
from PyQt6.QtGui import (QIcon, QPalette, QColor)
from widgets.drawing_area import DrawingLayer, Viewer

class LayerWidget(QFrame):
    def __init__(self, layer_name=""):
        super().__init__()
        self.m_is_active = True

        self.layout = QHBoxLayout(self)
        self.title = QLabel(layer_name)
        self.m_delete_button = QPushButton()
        self.m_delete_button.setIcon(QIcon("img/delete.png"))

        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(1)
        self.setFixedHeight(40)
        self._switch_active()

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.m_delete_button)

    @property
    def delete_button(self):
        return self.m_delete_button

    @property
    def is_active(self):
        return self.m_is_active

    @is_active.setter
    def is_active(self, is_active):
        self.m_is_active = is_active
        self._switch_active()

    def _switch_active(self):
        palette = self.palette()
        if self.is_active:
            palette.setColor(QPalette.ColorRole.Window, QColor(167, 184, 171))
        else:
            palette.setColor(QPalette.ColorRole.Window, QColor(255, 255, 255))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

class LayersPanel(QFrame):
    def __init__(self, viewer: Viewer):
        super().__init__()

        self.layout = QVBoxLayout(self)
        self.m_add_layer_button = QPushButton("+", clicked=lambda: self.add_layer_widget(Viewer.DrawingLayer))
        self.layout.addWidget(self.m_add_layer_button)

        self.layers_layout = QVBoxLayout()

        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        
        self.widget = QWidget()
        self.widget.setLayout(self.layers_layout)
        self.layout.addWidget(self.widget)
        
        self.scrollArea.setWidget(self.widget)
        self.layout.addWidget(self.scrollArea)
        
        self.setFixedHeight(200)
        self.setMaximumWidth(200)
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(1)
        
        self.viewer = viewer
        self.layers_per_widgets = {}
        self.widgets_per_layers = {}
        self.last_layer_number = 1

    def add_layer_widget(self, layer):
        layer_widget = LayerWidget(f"{self.last_layer_number} Слой")
        layer_widget.delete_button.clicked.connect(lambda: self.remove_layer(layer_widget))
        self.last_layer_number += 1

        if len(self.widgets_per_layers) > 0:
            self.widgets_per_layers[self.viewer.current_layer].is_active = False
        self.viewer.add_layer(layer)
        self.layers_per_widgets[layer_widget] = self.viewer.current_layer
        self.widgets_per_layers[self.viewer.current_layer] = layer_widget

        self.layers_layout.addWidget(layer_widget)

    def remove_all_layers(self):
        for layer_widget in self.layers_per_widgets.keys():
            #self.layers_per_widgets[layer_widget] = None
            self.layers_layout.removeWidget(layer_widget)
            layer_widget.setParent(None)

        self.last_layer_number = 1
        self.layers_per_widgets = {}
        self.widgets_per_layers = {}

    def remove_layer(self, layer_widget: LayerWidget):
        if layer_widget in self.layers_per_widgets.keys():
            self.widgets_per_layers[self.viewer.current_layer].is_active = False
            self.viewer.remove_layer(self.layers_per_widgets[layer_widget])
            del self.widgets_per_layers[self.layers_per_widgets[layer_widget]]
            del self.layers_per_widgets[layer_widget]
            self.layers_layout.removeWidget(layer_widget)
            layer_widget.setParent(None)
        if len(self.widgets_per_layers) > 0:
            self.widgets_per_layers[self.viewer.current_layer].is_active = True

    @property
    def add_layer_button(self):
        return self.m_add_layer_button