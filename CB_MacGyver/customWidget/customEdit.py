from PyQt5.QtGui import QMouseEvent, QPaintEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget
from .rippleEffect import IconButton
import paths
import type
from type import DownloadInfo

class CustomLineEdit(QLineEdit):

    link_icon = paths.IMAGE_DIR + '/Link_Icon.png'
    cur_url = None
    cur_type = None

    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        
        self.setFixedHeight(32)
        self.__buttonInit()
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PixelMetric.PM_DefaultFrameWidth)
        font = self.font()
        font.setPixelSize(15)
        self.setFont(font)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setPlaceholderText(self.tr('Enter URL'))
        #self.setStyleSheet('QLineEdit {padding-left: %dpx;}' )
        self.setStyleSheet("""
            QLineEdit {
                padding-left: %dpx;
                border-style: solid;
                border-width: 1px;
                border-color: rgb(200, 200, 200);
                border-radius: 4px;
            }
            QLineEdit:hover {
                border-color: rgb(200, 0, 0);
            }
            QLineEdit:focus {
                border-width: 1.5px;
                border-color: rgb(200, 0, 0);
            }
            """ %(buttonSize.width() + frameWidth + 4)
        )
        self.setMinimumSize(max(self.minimumSizeHint().width(), buttonSize.width() + frameWidth*2 + 2),
                            max(self.minimumSizeHint().height(), buttonSize.height() + frameWidth*2 + 2))
        
        self.textChanged.connect(self.__display_type)
        
    def resizeEvent(self, event):
        frameWidth = self.style().pixelMetric(QStyle.PixelMetric.PM_DefaultFrameWidth)
        self.button.move(frameWidth * 4, frameWidth * 4)
        super().resizeEvent(event)

    def __display_type(self):
        url = self.text()
        self.cur_url = url
        self.cur_type = None
        for key, value in type.type_list.items():
            if url.find(key) > 0 :
                self.button.setIcon(QIcon(type.icon_list[value]))
                self.cur_type = value
                return
        
        for key, value in type.ext_list.items():
            if url.endswith(key):
                self.button.setIcon(QIcon(type.icon_list[value]))
                self.cur_type = value
                return
        
        self.button.setIcon(QIcon(self.link_icon))
    
    def getCurrentTypeAndUrl(self) -> DownloadInfo:
        di = DownloadInfo(self.cur_url, self.cur_type)
        if self.cur_type == None:
            di.state = type.State.Error
        
        self.setText('')
        return di
    
    def __buttonInit(self):
        '''버튼 초기화 함수
        '''
        self.button = IconButton(self)
        self.button.setIcon(QIcon(self.link_icon))
        self.button.setStyleSheet("""
            QToolButton {
                border: 0px;
                padding: 0px;
                border-radius: 3px;
            }
            QToolButton:hover {
                background-color: rgb(210, 210, 210);
            }
            
            """)
        self.button.clicked.connect(self.__pressClick)
        self.button.setCursor(Qt.CursorShape.PointingHandCursor)
        frameWidth = self.style().pixelMetric(QStyle.PixelMetric.PM_DefaultFrameWidth)
        buttonHeight = (self.height() - frameWidth * 2 * 2 - 4)
        self.button.setFixedHeight(buttonHeight)
        self.button.setIconSize(QSize(buttonHeight, buttonHeight))
        self.button.setToolTip(self.tr('Paste'))

    def __pressClick(self):
       self.setText(QApplication.clipboard().text())
    

