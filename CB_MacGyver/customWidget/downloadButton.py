from PyQt5.QtCore import QEvent, QObject
from PyQt5.QtGui import QMouseEvent, QPaintEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget
#from .rippleEffect import IconButton
import customWidget.iconbutton
from paths import MyIcon

class DownloadButton(customWidget.iconbutton.IconButton):

    isIn = False
    isInMenu = False
    isPress = False
    btnW = 96
    btnH = 32
    menuX = 75
    menuY = 0
    menuW = 20
    menuH = 32
    _radius = 5
    baseColor = QColor(184, 20, 20)
    hilightColor = QColor(160, 20, 20)
    pixmapDown :QPixmap
    pixmapArrow :QPixmap

    def __init__(self, edit, parent = None, ) -> None:
        super().__init__(parent, QSize(self.btnW, self.btnH))
        # menu = QMenu()
        # temp = QAction('추가중', self)
        # menu.addAction(temp)
        # menu.addSeparator()
        # self.setMenu(menu)
        #self.setIcon(QIcon('Download_Icon.png'))
        self.setAutoRaise(True)
        self.setFixedHeight(self.btnH)
        self.setFixedWidth(self.btnW)
        self.setMouseTracking(True)
        self.pixmapDown = QPixmap(MyIcon.DOWNLOAD_ICON)
        self.pixmapArrow = QPixmap(MyIcon.MENU_ARROW_ICON)
        self.pixmapDown = self.pixmapDown.scaled(20, 18, Qt.AspectRatioMode.KeepAspectRatio)
        #self.installEventFilter(self)
        #self.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        #self.baseColor = "rgb(184, 20, 20)"
        #self.pressedColor = "rgb(160, 20, 20)"
        #self.clicked.connect(self.__pressClick)
        self.setObjectName('DownloadBtn')
        self.setStyleSheet("""
            QToolButton#DownloadBtn {
                padding: 0px;
                border-width: 0px;
            }
            QToolButton:menu-button#DownloadBtn {
                width: 20px;
                height: 32px;
            }
            """)
        self.edit = edit

    def paintEvent(self, a0: QPaintEvent | None) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.RenderHint.HighQualityAntialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        if not self.isPress:
            painter.setBrush(self.baseColor)
        else: painter.setBrush(self.hilightColor)
        painter.drawRoundedRect(0,0, self.btnW, self.btnH, self._radius, self._radius)
        painter.drawPixmap(QPointF((self.btnW - self.pixmapDown.width())/2, (self.btnH - self.pixmapDown.height())/2), self.pixmapDown)

        if not self.isIn: return
        if not self.isInMenu:
            painter.setBrush(self.baseColor)
        else : painter.setBrush(self.hilightColor)
        if not self.isPress:
            painter.setBrush(self.baseColor)
        else: painter.setBrush(self.hilightColor)
        painter.drawRoundedRect(self.menuX, self.menuY, self.menuW, self.menuH, self._radius, self._radius)
        pen = QPen(Qt.GlobalColor.white, 1, Qt.PenStyle.SolidLine)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawLine(self.menuX, self.menuY + 5, self.menuX, self.menuH - 5)

        w = self.pixmapArrow.width()
        h = self.pixmapArrow.height()
        painter.drawPixmap(QPointF(self.menuX + (self.menuW - w)/2, (self.menuH - h)/2), self.pixmapArrow)
        painter.end()

    def leaveEvent(self, a0: QEvent | None) -> None:
        super().leaveEvent(a0)
        self.setGraphicsEffect(None)
        self.isIn = False
        self.isInMenu = False
        self.isPress =  False
        self.update()
    
    def enterEvent(self, a0: QEvent | None) -> None:
        super().enterEvent(a0)
        #self.isIn = True
        effect = QGraphicsDropShadowEffect(self)
        #이펙트의 반경이 눈에보이는것보다 조금 더 큰 공간을 차지함
        #그래서 현재기준으로 반경이 8이넘어가면 1번째 항목의 QLabel위젯은 이펙트발생시에 계속해서 repaint됨
        #지금과 같은 상황은 아니지만 구글검색시에 QLabel의 paintEvent가 많이 호출되서 문제를 겪고있다는 질문이 다수 존재함.
        #이는 QLabel의 paint메커니즘 때문이라 QLabel을 사용하는거면 어쩔 수 없다고 함.
        effect.setBlurRadius(8)
        effect.setColor(QColor(184, 20, 20))
        effect.setOffset(0)
        self.setGraphicsEffect(effect)
        self.update()
    
    # def mouseMoveEvent(self, e: QMouseEvent | None) -> None:
    #     #super().mouseMoveEvent(e)
    #     x = e.x()
    #     y = e.y()
    #     if (0 <= x < self.width() and 0 <= y < self.height()):
    #         if (self.menuX <= x < self.menuX + self.menuW and self.menuY <= y < self.menuY + self.menuH):
    #             self.isInMenu = True
    #         else: 
    #             self.isInMenu = False
    #         self.update()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        super().mousePressEvent(e)
        if e.buttons() & Qt.MouseButton.LeftButton:
            self.isPress = True
            if self.isInMenu is True:
                   self.showMenu()

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        super().mouseReleaseEvent(e)
        self.isPress = False
        self.update()

    # def eventFilter(self, object: QObject | None, event: QEvent | None) -> bool:
    #     if event.type() == QEvent.Type.HoverEnter:
    #         effect = QGraphicsDropShadowEffect()
    #         effect.setBlurRadius(20)
    #         effect.setColor(QColor(184, 20, 20))
    #         effect.setOffset(0)
    #         self.setGraphicsEffect(effect)
    #         return True
    #     elif event.type() == QEvent.Type.HoverLeave:
    #         self.setGraphicsEffect(None)
    #         return True
    #     return False
    

    # def __pressClick(self):
    #    self.setText(QApplication.clipboard().text())