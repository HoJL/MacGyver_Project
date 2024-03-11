from PyQt5.QtGui import QPaintEngine, QPaintEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QTextOption, QFontMetrics, QTextCursor
from PyQt5.QtCore import Qt, QRectF

class MyLabel(QLabel):

    def __init__(self, parent):
        super().__init__(parent)
        self.cnt = 0
        self.txt = ""
        self.mt = QFontMetrics(self.font())
        self.txt_flags = Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        self.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

    def setText(self, a0: str | None) -> None:
        self.txt = a0

    def paintEvent(self, a0: QPaintEvent | None):
        super().paintEvent(a0)
        print(self.cnt)
        self.cnt += 1
        painter = QPainter()
        painter.begin(self)
        # print(self.cnt)
        # self.cnt += 1
        # #rt = QRectF(0, 0, 100, 40)
        # # print(mt.boundingRect())
        elided = self.mt.elidedText(self.txt, Qt.TextElideMode.ElideRight, self.width() - 10)
        painter.drawText(self.rect(), self.txt_flags, elided)
        painter.end()