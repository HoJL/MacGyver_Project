from PyQt5.QtCore import QEvent, QSize, Qt, QVariantAnimation, QRect, QPoint, QSequentialAnimationGroup
from PyQt5.QtWidgets import QToolButton, QWidget, QAction
from PyQt5.QtGui import QIcon, QMouseEvent, QPaintEvent, QPainter, QColor, QPixmap, QBrush
import typing
import paths
from customWidget.ripple_animation import RippleAnimation


class IconButton(QToolButton):
    
    def __init__(self, parent: QWidget | None = ..., size: QSize = QSize(25, 25)) -> None:
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.test_img = QIcon(paths.IMAGE_DIR + '/Link_Icon.png')
        self.setFixedSize(size)
        self.pixmap = QPixmap(paths.IMAGE_DIR + '/Link_Icon.png').scaled(size, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatioByExpanding, transformMode=Qt.TransformationMode.SmoothTransformation)
        self.alpha = 0

    def enterEvent(self, a0: QEvent | None) -> None:
        super().enterEvent(a0)
        self.alpha = 255

    def leaveEvent(self, a0: QEvent | None) -> None:
        super().leaveEvent(a0)
        self.alpha = 0

    def mousePressEvent(self, a0: QMouseEvent | None) -> None:
        super().mousePressEvent(a0)
        self.ripple = RippleAnimation(self, round(max(self.width(), self.height()) * 1.5))
        self.ripple.start_ripple_effect(a0.x(), a0.y())

    def setIconSize(self, size: QSize) -> None:
        #super().setIconSize(size)
        self.pixmap = self.pixmap.scaled(size.width(), size.height(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatioByExpanding, transformMode=Qt.TransformationMode.SmoothTransformation)

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.HighQualityAntialiasing)
        painter.setBackgroundMode(Qt.BGMode.TransparentMode)
        brush = QBrush(QColor(210, 210, 210, self.alpha))
        painter.setBrush(brush)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 5, 5)
        painter.drawPixmap(self.pixmap.rect(), self.pixmap)