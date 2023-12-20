from PyQt6.QtWidgets import (QLabel, QFileDialog, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem)
from PyQt6.QtGui import (QPixmap, QPainter, QPen, QColor, QImage)
from PyQt6.QtCore import (Qt, QPoint, QLineF, QPointF, QRectF)

# class DrawingArea(QLabel):
#     def __init__(self):
#         super().__init__()
#         self.pixmap = QPixmap(self.size())
#         self.pixmap.fill(Qt.GlobalColor.white)
#         self.setPixmap(self.pixmap)
#         self.last_x, self.last_y = None, None
#         self.setMinimumSize(50,50)
#         self.pen_color = Qt.GlobalColor.blue

#     def add_image(self):
#         image = QPixmap("dog.jpg")
#         self.pixmap = image.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)
#         self.setPixmap(self.pixmap)
#         self.resize(self.pixmap.size())
#         # file_name, _ = QFileDialog.getOpenFileName(self, "Add Image", "")
#         # if file_name:
#         #     image = QPixmap(file_name)
#         #     self.pixmap = image.scaled(self.size(),
#         #      Qt.AspectRatioMode.KeepAspectRatio, 
#         #      Qt.TransformationMode.SmoothTransformation)
#         #     self.setPixmap(self.pixmap)

#     def save_image(self):
#         file_name, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "Images (*.png *.jpg *.bmp)")
#         if file_name:
#             self.pixmap.save(file_name)

#     def set_pen_color(self, color: QColor):
#         self.pen_color = color

#     def mouseMoveEvent(self, e):
#         if self.last_x is None: # First event.
#             self.last_x = e.position().x()
#             self.last_y = e.position().y()
#             return # Ignore the first time.

#         painter = QPainter(self.pixmap)
#         pen = QPen(self.pen_color, 7)
#         pen.setCapStyle(Qt.PenCapStyle.RoundCap)
#         painter.setPen(pen)
#         line = QLineF(self.last_x, self.last_y, e.position().x(), e.position().y())
#         painter.drawLine(line)
#         painter.end()
#         self.setPixmap(self.pixmap)

#         # Update the origin for next time.
#         self.last_x = e.position().x()
#         self.last_y = e.position().y()

#     def mouseReleaseEvent(self, e):
#         self.last_x = None
#         self.last_y = None

#     def resizeEvent(self, e):
#         newPixmap = self.pixmap.scaled(e.size())
#         newPixmap.fill(Qt.GlobalColor.white)
#         painter = QPainter(newPixmap)
#         painter.drawPixmap(QPoint(), self.pixmap)
#         self.pixmap = newPixmap

#         self.setPixmap(self.pixmap)
#         super().resizeEvent(e)

class HandDrawingScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.drawing = False
        self.last_pos = QPointF()
        self.pen_color = Qt.GlobalColor.blue
        self.pen = QPen(self.pen_color, 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)

    def set_pen_color(self, color: QColor):
        self.pen_color = color

    def mousePressEvent(self, event):
        self.last_pos = event.scenePos()
        self.drawing = True
        self.pen.setColor(self.pen_color)

    def mouseMoveEvent(self, event):
        if self.drawing:
            new_pos = event.scenePos()

            if not self.parent().pixmap.rect().contains(new_pos.toPoint()):
                return

            line_item = self.addLine(QLineF(self.last_pos, new_pos), self.pen)
            line_item.setFlag(QGraphicsPixmapItem.GraphicsItemFlag.ItemIsSelectable, True)

            self.last_pos = new_pos

    def mouseReleaseEvent(self, event):
        self.drawing = False

class Viewer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_hand_drawing_scene = HandDrawingScene(self)
        self.setScene(self.m_hand_drawing_scene)
        self.m_pixmapItem = self.scene().addPixmap(QPixmap(self.size()))
        white_pixmap = self.pixmap
        white_pixmap.fill(Qt.GlobalColor.lightGray)
        self.pixmap = white_pixmap

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