from PyQt5.QtGui import QMouseEvent, QPaintEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QWidget
#from .rippleEffect import IconButton
import customWidget.iconbutton
from customWidget.custom_line_edit import CustomLineEdit
from paths import MyIcon
import type
from type import DownloadInfo

class CustomIconEdit(CustomLineEdit):
    cur_url = None
    cur_type = None

    def __init__(self, parent) -> None:
        super(CustomIconEdit, self).__init__(parent)
        
        self.setFixedHeight(32)
        self.__buttonInit()
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(QStyle.PixelMetric.PM_DefaultFrameWidth)
        font = self.font()
        font.setPixelSize(15)
        self.setFont(font)
        self.setPlaceholderText(self.tr('Enter URL'))
        self.setStyleSheet(self.styleSheet() + """
            QLineEdit#CustomEdit {
                padding-left: %dpx;
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
        self.cur_url = url.strip()
        self.cur_type = None
        for key, value in type.type_list.items():
            if self.cur_url.find(key) > 0 :
                self.button.setPixmap(type.icon_list[value])
                self.cur_type = value
                return
        
        for key, value in type.ext_list.items():
            if self.cur_url.endswith(key):
                self.button.setPixmap(type.icon_list[value])
                self.cur_type = value
                return
        
        self.button.setPixmap(MyIcon.LINK_ICON)
    
    def getCurrentTypeAndUrl(self) -> DownloadInfo:
        di = DownloadInfo(url=self.cur_url, type=self.cur_type)
        if self.cur_type == None:
            di.state = type.State.Error
        
        self.setText('')
        return di
    
    def __buttonInit(self):
        '''버튼 초기화 함수
        '''
        frameWidth = self.style().pixelMetric(QStyle.PixelMetric.PM_DefaultFrameWidth)
        buttonHeight = (self.height() - frameWidth * 2 * 2 - 4)
        self.button = customWidget.iconbutton.IconButton(self, QSize(buttonHeight, buttonHeight))
        self.button.setToolTip(self.tr('Paste'))
        self.button.clicked.connect(self.__pressClick)

    def __pressClick(self):
       self.setText(QApplication.clipboard().text())
    

