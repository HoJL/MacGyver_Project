from PyQt5.QtCore import QEvent, Qt, QSize, QRect, QRectF, pyqtSignal
from PyQt5.QtGui import QMouseEvent, QPaintEvent, QPainter, QColor, QPixmap, QImage, QBrush, QWindow, QPainterPath, QIcon
from PyQt5.QtWidgets import QLabel, QSplashScreen, QWidget, QToolTip, QAction, QPushButton, QFrame
from customWidget.loading_label import Loading_Label
import type

class ThumbnailLabel(QLabel):

    zoom_signal = pyqtSignal(int)
    zoom_move_signal = pyqtSignal()
    click_signal = pyqtSignal()
    pix = None
    __gap = 5
    thumb_base: QPixmap = None
    
    def __init__(self, size: QSize, pixmapUrl: str, parent, state = type.State.Normal):
        super().__init__(parent)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
                QLabel{
                        background-color: rgba(222, 222, 222, 0);
                        border-width: 0px;
                        border-radius: 10px;
                }
        """)
        self.pix = pixmapUrl
        self.thumbsize = size 
        self.isEnter = False
        self.mouseX = 0
        self.mouseY = 0
        self.setMouseTracking(True)
        self.state = state
        self.root = self
        while True:
            if self.root.parent() is None:
                break
            self.root = self.root.parent()

        self.overlayX = int(self.thumbsize.width() * 1.5)
        self.overlayY = int(self.thumbsize.height() * 1.5)
        self.loading = Loading_Label(self)
        self.loading.move(int(self.thumbsize.width()/2 - self.loading.width()/2), int(self.thumbsize.height()/2 - self.loading.height()/2))

        self.splash = QLabel(self, Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SplashScreen)
        #self.splash.setStyleSheet('background-color: rgba(222, 222, 222, 0); border-width: 0px;')
        self.splash.setWindowOpacity(0)
        self.splash.hide()
        self.zoom_signal.connect(self.zoom_slot)
        self.zoom_move_signal.connect(self.zoom_move_slot)
        QWidget(self.root).setWindowState(Qt.WindowState.WindowActive)
        self.set_thumb_pixmap(pixmapUrl)
        
    def rounded_image(self):
        image = QPixmap(self.pix)
        return self.rounded_image_by_pixmap(image)
    
    def rounded_image_by_pixmap(self, pixmap: QPixmap):
        image = pixmap.scaled(self.overlayX, self.overlayY, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatioByExpanding, transformMode=Qt.TransformationMode.SmoothTransformation)
        out_img = QPixmap(image.width(), image.height())
        out_img.fill(Qt.GlobalColor.transparent)
        painter = QPainter(out_img)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.HighQualityAntialiasing | QPainter.RenderHint.SmoothPixmapTransform, True)
        brush = QBrush(image)
        painter.setBrush(brush)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.fillRect(0, 0, image.width(), image.height(), QColor(255, 255, 255, 0))
        painter.drawRoundedRect(0, 0, image.width(), image.height(), 8, 8)
        painter.end()
        return out_img

    def __del__(self):
        self.splash = None

    def set_thumb_pixmap(self, pixUrl):
        if self.state == type.State.Error:
            return
        if pixUrl is None:
            self.setLoading(True)
            return
        
        self.setLoading(False)
        self.thumb_base = QPixmap(pixUrl).scaled(self.thumbsize, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        self.thumb_small = QPixmap(pixUrl).scaled(self.thumbsize.width() - 5, self.thumbsize.height() - 5, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        self.big_pix = QPixmap(pixUrl).scaled(self.overlayX, self.overlayY, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatioByExpanding, transformMode=Qt.TransformationMode.SmoothTransformation)
        #self.big_pix = QPixmap(self.pix).scaled(self.overlayX, self.overlayY, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        self.pix = pixUrl
        pix = self.rounded_image()
        self.splash.setPixmap(pix)
        self.splash.setMask(pix.mask())
        self.splash.setFixedSize(self.big_pix.width(), self.big_pix.height())
        self.update()

    def set_thumb_pixmap_by_load(self, pixmap: QPixmap):
        if pixmap is None:
            return
        
        self.thumb_base = pixmap.scaled(self.thumbsize, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        self.thumb_small = pixmap.scaled(self.thumbsize.width() - 5, self.thumbsize.height() - 5, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        self.big_pix = pixmap
        pix = self.rounded_image_by_pixmap(pixmap)
        self.splash.setPixmap(pix)
        self.splash.setMask(pix.mask())
        self.splash.setFixedSize(self.big_pix.width(), self.big_pix.height())
        self.update()

    def setLoading(self, b: bool):
        if b is True:
            self.loading.start()
        else:
            self.loading.stop()

    def enterEvent(self, a0: QEvent | None) -> None:
        self.isEnter = True
        self.zoom_signal.emit(1)
        self.update()

    def leaveEvent(self, a0: QEvent | None) -> None:
        self.isEnter = False
        self.zoom_signal.emit(0)
        self.update()
        
    def mouseMoveEvent(self, ev: QMouseEvent | None) -> None:
        self.mouseX = ev.globalX()
        self.mouseY = ev.globalY()
        self.zoom_move_signal.emit()

    def mousePressEvent(self, ev: QMouseEvent | None) -> None:
        self.click_signal.emit()

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        super().paintEvent(a0)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.HighQualityAntialiasing)
        painter.setBrush(QColor(222, 222, 222))
        painter.setPen(Qt.PenStyle.NoPen)

        left = top = 0
        width = self.thumbsize.width()
        height = self.thumbsize.height()

        if self.thumb_base is None or self.state is type.State.Error:
            left = self.__gap
            top = self.__gap
            width -= self.__gap * 2
            height -= self.__gap * 2
            rect = QRect(left, top, width, height)
            painter.drawRoundedRect(rect, 5, 5)
        
        else:
            pix_left = 0
            pix_top = int((self.thumbsize.height() - self.thumb_base.height())/2)
            pix_width = self.thumbsize.width()
            pix_height = self.thumb_base.height()
            thumb = self.thumb_base

            if self.isEnter is False:
                left = self.__gap
                top = self.__gap
                width -= self.__gap * 2
                height -= self.__gap * 2

                pix_left = self.__gap
                pix_width -= self.__gap * 2
                pix_height = self.thumb_small.height()
                pix_top = int((self.thumbsize.height() - self.thumb_small.height())/2)
                thumb = self.thumb_small

            rect = QRect(left, top, width, height)
            painter.drawRoundedRect(rect, 5, 5)

            rect = QRect(pix_left, pix_top, pix_width, pix_height)
            painter.drawPixmap(rect, thumb)

    def zoom_move_slot(self):
        self.splash.move(self.mouseX + 20, self.mouseY + 20)

    def zoom_slot(self, opacity):
        if self.state == type.State.Error:
            return
        if self.loading.isVisible() is True:
            return        
        if self.splash.isVisible() is False:
            self.show_splash()

        self.splash.setWindowOpacity(opacity)

    def show_splash(self):
        self.splash.show()
        QWidget(self.root).setWindowState(Qt.WindowState.WindowActive)
