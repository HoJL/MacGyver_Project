from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QSize, QTimer, QFile
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon, QPixmap, QFontMetrics
import threading
from customWidget.custom_progress_bar import CustomProgressBar
from customWidget.thumbnail_label import ThumbnailLabel
import os
import paths
import webbrowser
import type
from type import DownloadInfo
from functools import partial
from myTimer import MyTimer
from customWidget.myLabel import MyLabel
from customWidget.panel_buttons import PanelButtons
class Download_Panel():
    
    _height = 80
    _gap = 10
    loading_icon = paths.IMAGE_DIR + '/loading_spin.gif'
    _lock = threading.Lock()
    item_index = -1
    _file_path: str = None
    _forder_dir: str = None
    def __init__(self, parent, info: DownloadInfo) -> None:

        #super().__init__(parent)
        self._layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.list_view: QListWidget = parent
     
        self.info = info
        self.base = QWidget(parent)
        self.base.setLayout(self._layout)
        self.base.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.base.enterEvent = self.enterEvent
        self.base.leaveEvent = self.leaveEvent
        self.back_color = QColor(255, 255, 255)
        front_color = QColor(100, 100, 200)
        self.error_color = QColor(233, 59, 59)
        #error_color = QColor(255, 0, 0)
        self.update_state_color()
       
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
        self.thumbnail.click_signal.connect(self.__file_open)
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
        self.title.setStyleSheet('border: 0; background-color: rgba(255, 0, 255, 0);')
        self._top_layout.addWidget(self.title)
        
        #Panel Button
        self.pbt = PanelButtons(self.base)
        self._top_layout.addWidget(self.pbt)
        self.pbt.hide()
        self.pbt.add_list_del_btn_action(self.__del_widget)
        self.pbt.add_file_del_btn_action(self.__del_all)
        self.pbt.add_open_file_btn_action(self.__open_forder)
     
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
        self.time_widget.setStyleSheet('border: 0; background-color: rgba(255, 255, 255, 0);')
        self.time_str = '00:00'
        self.time_widget.setText(self.time_str)
        self.time = 0
        self.progress.timer.connect(self._timer)
        self.time_widget.setContentsMargins(5, 0, 5, 0)
        self._bottom_layout.addWidget(self.time_widget)
        # self.time_widget.hide()

        #temp space
        self.empty = QLabel(self.base)
        self.empty.setObjectName('empty')
        self.empty.hide()
        self.empty.setStyleSheet('border: 0; background-color: rgba(255, 255, 255, 0);')
        self._bottom_layout.addWidget(self.empty)
        #self.update_state()
    
    def enterEvent(self, e: QtCore.QEvent | None) -> None:
        self.pbt.show()

    def leaveEvent(self, e: QtCore.QEvent | None) -> None:
        self.pbt.hide()

    def setTitle(self, title: str):
       self.title.setText(title)
       self.title.update()
    
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
                
            txt = prefix + ' \n' + postfix
            self.title.setText(txt)
            self.thumbnail.setLoading(False)
            self.thumbnail.state = type.State.Error
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

    def __del_widget(self):
        idx = self.list_view.indexFromItem(self.item).row()
        item = self.list_view.takeItem(idx)

        del item

    def __del_file(self):
        if self.info.file_path is None:
            return
        try:
            QFile.moveToTrash(self.info.file_path)
        except:
            pass

    def __del_all(self):
        self.__del_file()
        self.__del_widget()

    def __open_forder(self):
        if self.info.dir is None:
            return
        try:
            os.startfile(self.info.dir)
        except:
            pass
    
    def __file_open(self):
        if self.info.file_path is None:
            return
        try:
            os.startfile(self.info.file_path)
        except:
            pass

    def set_item(self, item):
        self.item = item
        
        
