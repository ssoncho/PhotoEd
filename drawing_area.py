from PyQt6.QtWidgets import (QLabel, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsLineItem)
from PyQt6.QtGui import (QPixmap, QPainter, QPen, QColor, QImage)
from PyQt6.QtCore import (Qt, QPoint, QLineF, QPointF, QRectF)
from PyQt6 import QtGui

from enum import Enum

class Mode(Enum):
    DRAGGING = 1
    DRAWING = 2
    ERASING = 3

class HandDrawingScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mouse_pressed = False
        self.mode = Mode.DRAGGING
        self.last_pos = QPointF()
        self.pen_color = Qt.GlobalColor.blue
        self.pen = QPen(self.pen_color, 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)

    def set_pen_color(self, color: QColor):
        self.pen_color = color

    def set_drawing(self):
        self.mode = Mode.DRAWING

    def set_erasing(self):
        self.mode = Mode.ERASING

    def mousePressEvent(self, event):
        current_position = event.scenePos()
        self.mouse_pressed = True
        if self.mode == Mode.DRAWING:
            self.last_pos = current_position
            self.pen.setColor(self.pen_color)
        # elif self.mode == Mode.ERASING:
        #     item_to_remove = self.itemAt(current_position, QtGui.QTransform())
        #     if item_to_remove:
        #         self.removeItem(item_to_remove)

    def mouseMoveEvent(self, event):
        if self.mode == Mode.DRAWING and self.mouse_pressed:
            new_pos = event.scenePos()

            if not self.parent().pixmap.rect().contains(new_pos.toPoint()):
                return

            line_item = self.addLine(QLineF(self.last_pos, new_pos), self.pen)
            line_item.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable, True)

            self.last_pos = new_pos

        elif self.mode == Mode.ERASING and self.mouse_pressed:
            item_to_remove = self.itemAt(event.scenePos(), QtGui.QTransform())
            if isinstance(item_to_remove, QGraphicsLineItem):
                self.removeItem(item_to_remove)

    def mouseReleaseEvent(self, event):
        self.mouse_pressed = False

class Viewer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_hand_drawing_scene = HandDrawingScene(self)
        self.setScene(self.m_hand_drawing_scene)
        self.m_pixmapItem = self.scene().addPixmap(QPixmap(self.size()))
        initial_pixmap = self.pixmap
        initial_pixmap.fill(Qt.GlobalColor.lightGray)
        self.pixmap = initial_pixmap

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.m_pixmapItem.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

    def save_image(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.bmp)")
        if file_name:
            image = QImage(self.pixmap.size(), QImage.Format.Format_ARGB32)
            painter = QPainter(image)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            self.scene().render(painter)
            painter.end()
            image.save(file_name)

    def add_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Add Image", "")
        if file_name:
            image = QPixmap(file_name)
            self.scene().clear()
            self.m_pixmapItem = self.scene().addPixmap(image)
            self.fitInView(self.m_pixmapItem, Qt.AspectRatioMode.KeepAspectRatio)

    @property
    def hand_drawing_scene(self):
        return self.m_hand_drawing_scene

    @property
    def pixmap(self):
        return self.m_pixmapItem.pixmap()

    @pixmap.setter
    def pixmap(self, newPixmap):
        self.m_pixmapItem.setPixmap(newPixmap)
        self.fitInView(self.m_pixmapItem, Qt.AspectRatioMode.KeepAspectRatio)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.m_pixmapItem, Qt.AspectRatioMode.KeepAspectRatio)

    def wheelEvent(self, event):
        zoom = 0
        if event.angleDelta().y() > 0:
                factor = 1.25
                zoom += 1
        else:
            factor = 0.8
            zoom -= 1

        if zoom == 0:
            factor = 1

        self.scale(factor, factor)