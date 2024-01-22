from PyQt6.QtWidgets import (QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsRectItem, QGraphicsTextItem, QGraphicsItem)
from PyQt6.QtGui import (QPixmap, QPainter, QPen, QColor, QImage, QFont, QTextDocument, QTextCursor)
from PyQt6.QtCore import (Qt, QPoint, QLineF, QPointF, QRectF, QRect, QSize, QSizeF)
from PyQt6 import QtGui
from PyQt6 import QtCore

class Layer(QGraphicsRectItem):
    def __init__(self, parent=None):
        super().__init__(parent)

class TextLayer(QGraphicsTextItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlainText("Текст")
        self.setFont(QFont("Arial", 34))
        self.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.m_is_editable = True
        self.m_text_color = Qt.GlobalColor.black
        self.setDefaultTextColor(self.m_text_color)

    def set_editing(self):
        if self.is_editable:
            self.clearFocus()
            self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
            self.m_is_editable = False
        else:
            self.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
            self.m_is_editable = True

    @property
    def is_editable(self):
        return self.m_is_editable

    @property
    def text_color(self):
        return self.m_text_color

    @text_color.setter
    def text_color(self, color):
        self.m_text_color = color
        self.setDefaultTextColor(color)
            
class DrawingLayer(Layer):
    DrawState, EraseState, NoActionState = range(3)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_state = DrawingLayer.DrawState
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
        if self.current_state == DrawingLayer.EraseState:
            self._clear(event.pos().toPoint())
        elif self.current_state == DrawingLayer.DrawState:
            self.m_line_draw.setP1(event.pos())
            self.m_line_draw.setP2(event.pos())
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event):
        if self.current_state == DrawingLayer.EraseState:
            self._clear(event.pos().toPoint())
        elif self.current_state == DrawingLayer.DrawState:
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
    DrawingLayer, TextLayer = range(2)
    layer_added = QtCore.pyqtSignal()
    layer_deleted = QtCore.pyqtSignal()
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
        self.layers = []
        self.m_current_layer = self.background_item

        self.scene().addItem(self.background_item)

    def mouseDoubleClickEvent(self, event):
        if isinstance(self.m_current_layer, TextLayer) and not self.m_current_layer.isVisible():
            self.m_current_layer.setPos(self.mapToScene(event.pos()))
            self.m_current_layer.setVisible(True)

    def add_layer(self, layer):
        if isinstance(self.m_current_layer, TextLayer) and self.m_current_layer.is_editable:
            self.m_current_layer.set_editing()
        if layer == Viewer.DrawingLayer:
            self.m_current_layer = DrawingLayer(self.background_item)
            self.m_current_layer.pen_color = Qt.GlobalColor.transparent
            self.m_current_layer.reset()
        elif layer == Viewer.TextLayer:
            if isinstance(self.m_current_layer, DrawingLayer):
                self.m_current_layer.set_state(DrawingLayer.NoActionState)
            self.m_current_layer = TextLayer(self.background_item)
            #self.m_current_layer.setPos(QPointF(self.background_item.boundingRect().width()/2, self.background_item.boundingRect().height()/2))
            self.m_current_layer.setVisible(False)
        self.layers.append(self.m_current_layer)
        self.trigger_layer_added()

    def remove_layer(self, layer):
        if layer == self.m_current_layer:
            if len(self.layers) == 1:
                self.m_current_layer = self.background_item
            else:
                self.m_current_layer = self.layers[-2]
        self.layers.remove(layer)
        layer.setParentItem(None)
        if isinstance(self.m_current_layer, TextLayer) and self.m_current_layer.is_editable == False:
            self.m_current_layer.set_editing()
        self.trigger_layer_deleted()

    def set_image(self, image):
        self.scene().setSceneRect(
            QRectF(QPointF(), QSizeF(image.size()))
        )
        self.background_item.setPixmap(image)
        for layer in self.layers:
            layer.setParentItem(None)
        self.m_current_layer = self.background_item
        self.layers = []
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

    def trigger_layer_added(self):
        self.layer_added.emit()

    def trigger_layer_deleted(self):
        self.layer_deleted.emit()

    @property
    def current_layer(self):
        return self.m_current_layer

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