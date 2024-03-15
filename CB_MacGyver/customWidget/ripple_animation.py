from PyQt5.QtCore import Qt, QVariantAnimation, QRect, QPoint, QSequentialAnimationGroup
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPaintEvent, QPainter, QColor

class RippleAnimation(QWidget):

    ripple_rect : QRect = QRect(0, 0, 0, 0)
    alpah = 120
    def __init__(self, parent, max_size):
        super().__init__(parent)
        self.animation = QVariantAnimation(parent=parent)
        self.start_rect = QRect(0, 0, 0, 0)
        self.animation.setStartValue(self.start_rect)
        self.end_rect = QRect(0, 0, max_size, max_size)
        self.animation.setEndValue(self.end_rect)
        self.animation.setDuration(200)
        self.animation.valueChanged.connect(self.ripple_size_ani)

        self.animation_alpha = QVariantAnimation(parent=parent)
        self.animation_alpha.setStartValue(120)
        self.animation_alpha.setEndValue(0)
        self.animation_alpha.setDuration(200)
        self.animation_alpha.valueChanged.connect(self.ripple_alpha_ani)

        self.ani_gruop = QSequentialAnimationGroup()
        self.ani_gruop.finished.connect(self.delete)
        self.show()

    def start_ripple_effect(self, x, y):
        self.start_rect = QRect(0, 0, 0, 0)
        self.start_rect.moveCenter(QPoint(x, y))
        self.animation.setStartValue(self.start_rect)
        self.end_rect.moveCenter(QPoint(x, y))
        self.animation.setEndValue(self.end_rect)
        
        self.ani_gruop.addAnimation(self.animation)
        self.ani_gruop.addAnimation(self.animation_alpha)
        self.ani_gruop.start()
        
    def ripple_size_ani(self, rt):
        self.ripple_rect = rt
        self.update()

    def ripple_alpha_ani(self, al):
        self.alpah = al
        self.update()

    def delete(self):
        self.deleteLater()

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        
        painter = QPainter(self)
        #painter.setBackgroundMode(Qt.BGMode.TransparentMode)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(100, 100, 100, self.alpah))
        #painter.fillRect(0,0,100, 100, QColor(255, 255, 0))
        painter.drawEllipse(self.ripple_rect)