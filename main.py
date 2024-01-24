from PyQt6 import QtWidgets
from PyQt6 import QtCore
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QScrollArea)
from buttons import FunctionalButton
from drawing_area import Viewer, DrawingLayer, Layer, TextLayer
from layers import LayersPanel
from color_panel import (ColorPanel)

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_UI()
        self.init_signals()

    def init_UI(self):
        self.setGeometry(50, 50, 950, 600)
        self.setWindowTitle('PhotoEd')
        main_container = QtWidgets.QWidget()
        main_layout = QHBoxLayout()
        buttons_layout = QVBoxLayout()
        drawing_settings_layout = QVBoxLayout()

        
        self.viewer = Viewer()
        self.layers_panel = LayersPanel(self.viewer)
        self.color_panel = ColorPanel()
        drawing_settings_layout.addWidget(self.color_panel)
        drawing_settings_layout.addWidget(self.layers_panel)

        self.add_image_button = FunctionalButton(img_path="img/add.png")
        self.draw_button = FunctionalButton(img_path="img/draw.png")
        self.draw_spray_button = FunctionalButton(img_path="img/spray.png")
        self.erase_button = FunctionalButton(img_path="img/erase.png")
        self.add_text_button = FunctionalButton(img_path="img/text.png")
        self.save_button = FunctionalButton(img_path="img/save.png")
        buttons_layout.addWidget(self.add_image_button)
        buttons_layout.addWidget(self.draw_button)
        buttons_layout.addWidget(self.draw_spray_button)
        buttons_layout.addWidget(self.erase_button)
        buttons_layout.addWidget(self.add_text_button)
        buttons_layout.addWidget(self.save_button)

        main_layout.addLayout(drawing_settings_layout)
        main_layout.addLayout(buttons_layout)
        main_layout.addWidget(self.viewer)
        main_container.setLayout(main_layout)
        self.setCentralWidget(main_container)

    def init_signals(self):
        self.color_panel.color_button.clicked.connect(self.showColorDialog)

        self.save_button.clicked.connect(self.viewer.save_image)
        self.add_image_button.clicked.connect(self.viewer.add_image)
        self.add_image_button.clicked.connect(self.layers_panel.remove_all_layers)#deletes all layers even if photo wasn't chosen
        self.erase_button.clicked.connect(self.onStateChanged)
        self.draw_button.clicked.connect(self.onStateChanged)
        self.draw_spray_button.clicked.connect(self.onStateChanged)
        self.add_text_button.clicked.connect(lambda: self.layers_panel.add_layer_widget(Viewer.TextLayer))
        
        self.viewer.layer_added.connect(self.onLayerAdded)
        self.viewer.layer_deleted.connect(self.onLayerDeleted)

    @QtCore.pyqtSlot()
    def onLayerAdded(self):
        if isinstance(self.viewer.current_layer, DrawingLayer):
            self.viewer.current_layer.pen_color = self.color_panel.color_button.color
        elif isinstance(self.viewer.current_layer, TextLayer):
            self.viewer.current_layer.text_color = self.color_panel.color_button.color

    @QtCore.pyqtSlot()
    def onLayerDeleted(self):
        if isinstance(self.viewer.current_layer, DrawingLayer):
            self.viewer.current_layer.pen_color = self.color_panel.color_button.color

    @QtCore.pyqtSlot(bool)
    def onStateChanged(self):
        if isinstance(self.viewer.current_layer, DrawingLayer):
            self.viewer.current_layer.current_state = (
                DrawingLayer.EraseState
                if self.sender() == self.erase_button
                else (DrawingLayer.DrawState if self.sender() == self.draw_button else DrawingLayer.SprayState)
        )

    @QtCore.pyqtSlot()
    def showColorDialog(self):
        color = self.sender().color
        selected_color = QtWidgets.QColorDialog.getColor(color, self)
        if selected_color.isValid():
            color = selected_color
        elif isinstance(self.viewer.m_current_layer, TextLayer):
            return
        if isinstance(self.viewer.m_current_layer, Layer):
            self.viewer.m_current_layer.pen_color = color
        elif isinstance(self.viewer.m_current_layer, TextLayer):
            self.viewer.m_current_layer.text_color = color
        self.sender().color = color

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())