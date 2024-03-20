from PyQt5.QtCore import QEvent, QSize, Qt, QVariantAnimation, QRect, QPoint, QSequentialAnimationGroup
from PyQt5.QtWidgets import QToolButton, QWidget, QAction
from PyQt5.QtGui import QIcon, QMouseEvent, QPaintEvent, QPainter, QColor, QPixmap, QBrush, QImage
import typing
import paths
from customWidget.ripple_animation import RippleAnimation


class IconButton(QToolButton):
    
    def __init__(self, parent: QWidget | None = ..., size: QSize = QSize(25, 25)) -> None:
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        #self.test_img = QIcon(paths.IMAGE_DIR + '/Link_Icon.png')
        self.setFixedSize(size)
        self.pixmap = QPixmap(paths.IMAGE_DIR + '/Link_Icon.png').scaled(size, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatioByExpanding, transformMode=Qt.TransformationMode.SmoothTransformation)
        self.alpha = 0
        self.hover_pixmap = self.pixmap
        self.result_pixmap = self.pixmap

    def set_pixmap_hover_color(self, color: QColor):
        tmp = self.pixmap.toImage()

        for y in range(tmp.height()):
            for x in range(tmp.width()):
                if tmp.pixelColor(x, y).alpha() == 0:
                    continue
                color.setAlpha(tmp.pixelColor(x, y).alpha())
                tmp.setPixelColor(x, y, color)
        
        self.hover_pixmap = QPixmap.fromImage(tmp)

    def enterEvent(self, a0: QEvent | None) -> None:
        super().enterEvent(a0)
        self.alpha = 200
        if self.pixmap == self.hover_pixmap:
            return
        self.result_pixmap = self.hover_pixmap

    def leaveEvent(self, a0: QEvent | None) -> None:
        super().leaveEvent(a0)
        self.alpha = 0
        if self.pixmap == self.hover_pixmap:
            return
        self.result_pixmap = self.pixmap

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        super().mousePressEvent(a0)
        self.ripple = RippleAnimation(self, round(max(self.width(), self.height()) * 1.5))
        self.ripple.start_ripple_effect(a0.x(), a0.y())

    def setIconSize(self, size: QSize) -> None:
        #super().setIconSize(size)
        self.pixmap = self.pixmap.scaled(size.width(), size.height(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatioByExpanding, transformMode=Qt.TransformationMode.SmoothTransformation)

    def setPixmap(self, url):
        self.pixmap = QPixmap(url).scaled(self.width(), self.height(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatioByExpanding, transformMode=Qt.TransformationMode.SmoothTransformation)
        self.result_pixmap = self.hover_pixmap = self.pixmap

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.HighQualityAntialiasing)
        painter.setBackgroundMode(Qt.BGMode.TransparentMode)
        brush = QBrush(QColor(230, 230, 230, self.alpha))
        painter.setBrush(brush)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 5, 5)
        painter.drawPixmap(self.result_pixmap.rect(), self.result_pixmap)
        