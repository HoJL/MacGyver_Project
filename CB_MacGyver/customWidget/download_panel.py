from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon, QPixmap, QFontMetrics
import threading
from customWidget.custom_progress_bar import CustomProgressBar
from customWidget.thumbnail_label import ThumbnailLabel
import paths
import webbrowser
import type
from type import DownloadInfo
from functools import partial
from myTimer import MyTimer
from customWidget.myLabel import MyLabel

class Download_Panel():
    
    _height = 80
    _gap = 10
    loading_icon = paths.IMAGE_DIR + '/loading_spin.gif'
    _lock = threading.Lock()
    def __init__(self, parent, info: DownloadInfo) -> None:
        self._layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.info = info
        self.base = QWidget(parent)
        self.base.setLayout(self._layout)
        self.base.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        self.back_color = QColor(255, 255, 255)
        front_color = QColor(100, 100, 200)
        self.error_color = QColor(233, 59, 59)
        #error_color = QColor(255, 0, 0)
        self.update_state_color()
        
        # if info.state is type.State.Error:
        #     self.back_color = self.error_color

        # al = 0.1
        # r = al * front_color.red() +(1 - al) * back_color.red()
        # g = al * front_color.green() +(1 - al) * back_color.green()
        # b = al * front_color.blue() +(1 - al) * back_color.blue()
        # a = al * al + (1 - al) * 1
        # hover_rgba = '{}, {}, {}, {}'.format(r, g, b, a)

        # rgb = '{}, {}, {}, {}'.format(self.back_color.red(), self.back_color.green(), self.back_color.blue(), 0.6)
       
        # self.base.setStyleSheet("""
        #         QWidget{
        #             background-color: rgba(%s);
        #             border-width: 0.5px;
        #             border-style: solid;
        #             border-color: rgb(240, 240, 240);
                                
        #         }         
        #         QWidget::hover{

        #         }
        # """% (rgb))
        self.base.setFixedHeight(self._height)
        
        #=========================================
        #∥       ∥ title
        #∥ thumb ∥ -------------------------------
        #∥       ∥ typeIcon / progressBar
        #=========================================

        #Thmbnail
        thumbnail_frame_size = QtCore.QSize((int)(self._height * 1.5), (self._height))
        self.pix = QPixmap('D:/CB_MacGyver/CB_MacGyver/1.png').scaled(thumbnail_frame_size, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        self.thumbnail = ThumbnailLabel(thumbnail_frame_size, None, self.base, self.info.state)
        self.thumbnail.setFixedSize(thumbnail_frame_size)
        self.thumbnail.setCursor(Qt.CursorShape.PointingHandCursor)
        self._layout.addWidget(self.thumbnail)

        self._work_layout = QVBoxLayout()
        self._work_layout.setSpacing(0)
        self._work_layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addLayout(self._work_layout)
        
        self._top_layout = QHBoxLayout()
        self._top_layout.setSpacing(0)
        self._top_layout.setContentsMargins(0, 0, 0, 0)
        self._work_layout.addLayout(self._top_layout)

        #Title
        #self.title = QLabel(self.base)
        self.title = MyLabel(self.base)
        self.title.setFixedHeight((int)(self._height/2))
        #self.title.setContentsMargins(0, 0, 0, 0)
        # if self.info.state is type.State.Error:
        #     postfix = self.info.url
        #     if postfix is None:
        #         postfix = ''
                
        #     txt = 'Unkown URL: ' + postfix
        #     self.title.setText(txt)
        
        #self.title.setWordWrap(True)
        #self.title.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Expanding)
        self.title.setStyleSheet('border: 0; background-color: rgba(255, 0, 255, 100);')
        self._top_layout.addWidget(self.title)

        # self.testL = QLabel(self.base)
        # self.testL.setText("1")
        # # #self.testL.setFixedWidth(100)
        # self._top_layout.addWidget(self.testL)        

        self._bottom_layout = QHBoxLayout()
        self._bottom_layout.setSpacing(1)
        self._bottom_layout.setContentsMargins(0, 0, 0, 0)
        self._work_layout.addLayout(self._bottom_layout)

        #Type Icon
        self.type_icon = QPushButton(self.base)
        # icon = type.icon_list[self.info.type]
        # self.type_icon.setIcon(QIcon(icon))
        icon_size = QSize(25, 25)
        self.type_icon.setFixedSize(icon_size)
        self.type_icon.setIconSize(icon_size)
        self.type_icon.setStyleSheet('border: 0; background-color: rgba(255, 255, 255, 0);')
        self.type_icon.setCursor(Qt.CursorShape.PointingHandCursor)
        # self.type_icon.released.connect(partial(webbrowser.open, self.info.url))
        self._bottom_layout.addWidget(self.type_icon)


        #Progress bar
        self.progress = CustomProgressBar(self.base, 100, height=5, background_color=QColor(222, 222, 222))
        self.progress.setBarWidth(100)
        self._bottom_layout.addWidget(self.progress)
        # self.progress.hide()

        #Time
        self.time_widget = QLabel(self.base)
        self.time_widget.setStyleSheet('border: 0; background-color: rgb(255, 255, 0);')
        self.time_str = '00:00'
        self.time_widget.setText(self.time_str)
        self.time = 0
        self.progress.timer.connect(self._timer)
        self.time_widget.setContentsMargins(5, 0, 5, 0)
        self._bottom_layout.addWidget(self.time_widget)
        # self.time_widget.hide()

        # if self.info is not None and self.info.state is not type.State.Error and self.info.type is not None:
        #     self.type_icon = QPushButton(self.base)
        #     icon = type.icon_list[self.info.type]
        #     self.type_icon.setIcon(QIcon(icon))
        #     icon_size = QSize(25, 25)
        #     self.type_icon.setFixedSize(icon_size)
        #     self.type_icon.setIconSize(icon_size)
        #     self.type_icon.setStyleSheet('border: 0; background-color: rgba(255, 255, 255, 0);')
        #     self.type_icon.setCursor(Qt.CursorShape.PointingHandCursor)
        #     self.type_icon.released.connect(partial(webbrowser.open, self.info.url))
        #     self._bottom_layout.addWidget(self.type_icon)

        #     self.progress = CustomProgressBar(self.base, 100, height=5, background_color=QColor(222, 222, 222))
        #     self.progress.setBarWidth(100)
        #     self._bottom_layout.addWidget(self.progress)

        #     self.time_widget = QLabel(self.base)
        #     self.time_widget.setStyleSheet('border: 0; background-color: rgb(255, 255, 0);')
        #     self.time_str = '00:00'
        #     self.time_widget.setText(self.time_str)
        #     self.time = 0
        #     self.progress.timer.connect(self._timer)
        #     self.time_widget.setContentsMargins(5, 0, 5, 0)
        #     self._bottom_layout.addWidget(self.time_widget)

        #temp space
        self.empty = QLabel(self.base)
        self.empty.setObjectName('empty')
        self.empty.hide()
        self.empty.setStyleSheet('border: 0; background-color: rgba(255, 255, 255, 0);')
        self._bottom_layout.addWidget(self.empty)
        #self.update_state()
           
    def setTitle(self, title: str):
       self.title.setText(title)
       pass
    
    def set_infomation(self):

        pass

    def update_state_color(self):
        back_color = self.back_color
        if self.info.state is type.State.Error:
            back_color = self.error_color

        rgb = '{}, {}, {}, {}'.format(back_color.red(), back_color.green(), back_color.blue(), 0.6)
       
        self.base.setStyleSheet("""
                QWidget{
                    background-color: rgba(%s);
                    border-width: 0.5px;
                    border-style: solid;
                    border-color: rgb(240, 240, 240);
                                
                }         
                QWidget::hover{

                }
        """% (rgb))

    def update_state(self):
        if self.info.state is type.State.Error:
            self.type_icon.hide()
            self.progress.hide()
            self.time_widget.hide()
            self.empty.show()
            postfix = self.info.url
            prefix = 'Unkown URL: '
            if self.info.type is not None:
                prefix = self.info.error_code
                
            txt = prefix
            self.title.setText(txt)
            #self.title.adjustSize()
            # rect = self._top_layout.contentsRect()
            # print(rect)
            # mt = QFontMetrics(self.title.font())
            # elided = mt.elidedText(txt, Qt.TextElideMode.ElideRight, self.title.width() - 10)
            # self.title.setText(elided)
            # self._top_layout.update()
            self.thumbnail.setLoading(False)
        else:
            self.type_icon.show()
            self.progress.show()
            self.time_widget.show()
            icon = type.icon_list[self.info.type]
            self.type_icon.setIcon(QIcon(icon))
            self.type_icon.released.connect(partial(webbrowser.open, self.info.url))
            self.thumbnail.setLoading(True)
            self.empty.hide()

        if self.info.state is type.State.Done:
            self.time_widget.hide()
            self.thumbnail.setLoading(False)
            

    def _timer(self):
        self.time += 1
        m, s = divmod(self.time, 60)
        self.time_str = '{:02d}:{:02d}'.format(m, s)
        if (m > 60):
            h, m = divmod(m, 60)
            self.time_str = '{:02d}:{:02d}:{:02d}'.format(h, m, s)
        
        self.time_widget.setText(self.time_str)
        #print(self.time_str)
        
