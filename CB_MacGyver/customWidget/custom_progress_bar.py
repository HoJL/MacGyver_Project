from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QRectF, QSize, QTimer
from PyQt5.QtGui import QPaintEvent
from PyQt5.QtWidgets import QWidget, QLabel, QSizePolicy
from PyQt5.QtGui import QPainter, QColor
import threading
import typing
import paths
from myTimer import MyTimer

class CustomProgressBar(QWidget):

    is_postprocessing = False
    thread_lock = threading.Lock()
    def __init__(self, parent, total_value, segment=100, width=100, height=20, is_percent=True, background_color=QColor(255,255,255) ,chunk_color=QColor(0,149,255), text_color=QColor(0, 0, 0)) -> None:
        super().__init__(parent)
        self.segment = segment
        self.total_value = total_value
        self.cur_value = 0
        self.bar_width = width
        self.bar_height = height
        self.background_color = background_color
        self.chunk_color = chunk_color
        self.is_percent = is_percent
        self.text_color = text_color
        self.movie = QtGui.QMovie(paths.IMAGE_DIR + '/loading_spin.gif')
        self.movie.setScaledSize(QSize(30, 30))
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Ignored)
        self.la = QLabel(self)
        self.la.setFixedSize(30, 30)
        
        self.la.setMovie(self.movie)
        self.movie.start()
        self.la.hide()
        self.la.setStyleSheet('border: 0; background-color: rgba(0, 0, 0 ,0)')
        self.timer = MyTimer()
        self.timer.setInterval(1)
        #self.movie.frameChanged.connect(self.repaint)

    def setValue(self, value):
        self.cur_value = value
        self.update()

    def setTotal(self, value):
        self.total_value = value
        self.update()

    @typing.overload
    def setBarSize(self, w: int, h: int):
        self.bar_width = w
        self.bar_height = h

    @typing.overload
    def setBarSize(self, size: QtCore.QSize):
        self.setBarSize(size.width(), size.height())

    def setBarWidth(self, w: int):
        self.bar_width = w

    def setBarHeight(self, h: int):
        self.bar_height = h

    def update_progress(self):
        self.cur_value += 1
        self.update()

    def start(self):
        self.timer.start()
    
    def done(self):
        self.timer.stop()

    def download_done(self):
        self.cur_value = self.total_value
        self.update()

    def IsPostprocessing(self, b: bool):
        self.is_postprocessing = b
        if b is True:
            self.la.setGeometry(self.bar_width + 10 + 35 + 60, int(self.height()/2) - int(30 / 2), 30, 30)
            self.la.show()
        else:
            self.la.hide()
        self.update()

    def paintEvent(self, event: QPaintEvent | None) -> None:
        self.thread_lock.acquire()
        super().paintEvent(event)
        painter = QPainter(self)
        #painter.setBackground(QColor(255, 0, 0))
        painter.setRenderHint(QPainter.RenderHint.HighQualityAntialiasing)
        painter.fillRect(0, 0, self.width(), self.height(), QColor(255, 0, 0))
        bar_y = max(0, (int)((self.height() - self.bar_height) / 2))
        #background bar
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.background_color)
        painter.drawRect(0, bar_y, self.bar_width, self.bar_height)

        #chunk
        ratio = (self.cur_value / self.total_value)
        fill = ratio * self.bar_width
        painter.setBrush(self.chunk_color)
        rectF = QRectF(0, bar_y, fill, self.bar_height)
        painter.drawRect(rectF)

        #text
        painter.setPen(self.text_color)
        if self.is_percent: # 10%
            text = f'{int(ratio * 100)}%'
        else: #10/100
            text = f'{self.cur_value}/{self.total_value}'

        
        painter.drawText(self.bar_width + 10, bar_y + int(bar_y / 2), text)
        if self.is_postprocessing:
            painter.drawText(self.bar_width + 10 + 35, bar_y + int(bar_y / 2), '후 처리중...')
            
        
        self.thread_lock.release()