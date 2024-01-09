from PyQt6.QtWidgets import (QLabel, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsLineItem, QGraphicsRectItem)
from PyQt6.QtGui import (QPixmap, QPainter, QPen, QColor, QImage)
from PyQt6.QtCore import (Qt, QPoint, QLineF, QPointF, QRectF, QRect, QSize, QSizeF)
from PyQt6 import QtGui

class LayerItem(QGraphicsRectItem):
    DrawState, EraseState = range(2)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_state = LayerItem.DrawState
        self.setPen(QtGui.QPen(Qt.PenStyle.NoPen))

        self.m_line_eraser = QLineF()
        self.m_line_draw = QLineF()
        self.m_pixmap = QPixmap()

    def reset(self):
        r = self.parentItem().pixmap().rect()
        self.setRect(QRectF(r))
        self.m_pixmap = QPixmap(r.size())
        self.m_pixmap.fill(Qt.GlobalColor.transparent)

    def paint(self, painter, option, widget=None):
        super().paint(painter, option, widget)
        painter.save()
        painter.drawPixmap(QPoint(), self.m_pixmap)
        painter.restore()

    def mousePressEvent(self, event):
        if self.current_state == LayerItem.EraseState:
            self._clear(event.pos().toPoint())
        elif self.current_state == LayerItem.DrawState:
            self.m_line_draw.setP1(event.pos())
            self.m_line_draw.setP2(event.pos())
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.current_state == LayerItem.EraseState:
            self._clear(event.pos().toPoint())
        elif self.current_state == LayerItem.DrawState:
            self.m_line_draw.setP2(event.pos())
            self._draw_line(
                self.m_line_draw, QtGui.QPen(self.pen_color, 15, cap=Qt.PenCapStyle.RoundCap, join=Qt.PenJoinStyle.RoundJoin)
            )
            self.m_line_draw.setP1(event.pos())
        super().mouseMoveEvent(event)

    def _draw_line(self, line, pen):
        painter = QtGui.QPainter(self.m_pixmap)
        painter.setPen(pen)
        painter.drawLine(line)
        painter.end()
        self.update()

    def _clear(self, pos):
        painter = QtGui.QPainter(self.m_pixmap)
        r = QRect(QPoint(), 25 * QSize())
        r.moveCenter(pos)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_Clear)
        painter.eraseRect(r)
        painter.end()
        self.update()

    def set_state(self, state):
        self.current_state = state

    def set_pen_color(self, color):
        self.pen_color = color

    @property
    def pen_color(self):
        return self._pen_color

    @pen_color.setter
    def pen_color(self, color):
        self._pen_color = color

class Viewer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)

        self.background_item = QGraphicsPixmapItem()
        self.m_drawing_layer = LayerItem(self.background_item)
        self.m_drawing_layer.pen_color = Qt.GlobalColor.transparent

        self.scene().addItem(self.background_item)

    def set_image(self, image):
        self.scene().setSceneRect(
            QRectF(QPointF(), QSizeF(image.size()))
        )
        self.background_item.setPixmap(image)
        self.m_drawing_layer.reset()
        self.fitInView(self.background_item, Qt.AspectRatioMode.KeepAspectRatio)
        self.centerOn(self.background_item)

    def save_image(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.bmp)")
        if file_name:
            image = QImage(self.background_item.boundingRect().size().toSize(), QImage.Format.Format_ARGB32)
            painter = QPainter(image)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
            self.scene().render(painter)
            painter.end()
            image.save(file_name)

    def add_image(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Add Image", "")
        if file_name:
            image = QPixmap(file_name)
            self.set_image(image)

    @property
    def drawing_layer(self):
        return self.m_drawing_layer

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.fitInView(self.background_item, Qt.AspectRatioMode.KeepAspectRatio)

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