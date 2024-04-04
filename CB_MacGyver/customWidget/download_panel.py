from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QSize, QTimer, QFile
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QColor, QIcon, QPixmap, QFontMetrics, QKeySequence
import threading

from PyQt5.QtWidgets import QStyle, QStyleOption, QWidget
from customWidget.custom_progress_bar import CustomProgressBar
from customWidget.thumbnail_label import ThumbnailLabel
import os
import paths
import webbrowser
import type
from type import DownloadInfo
from functools import partial
from customWidget.myLabel import MyLabel
from customWidget.panel_buttons import PanelButtons
from enum import Enum
from customWidget.myMenu import MyMenu
from customWidget.iconbutton import IconButton
from paths import MyIcon
class Download_Panel(QWidget):
    
    _height = 80
    _gap = 10
    _lock = threading.Lock()
    item_index = -1
    _file_path: str = None
    _forder_dir: str = None

    def __init__(self, parent, info: DownloadInfo) -> None:

        super().__init__(parent)
        self._layout = QBoxLayout(QBoxLayout.Direction.LeftToRight)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.list_view: QListWidget = parent
        self.setFixedHeight(self._height)
        self.setLayout(self._layout)
        self.info = info
        self.setObjectName('Panel')

        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.back_color = QColor(255, 255, 255)
        front_color = QColor(100, 100, 200)
        self.error_color = QColor(233, 59, 59)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.update_state_color()

        self._init_menu()
        self._init_panel_widget()

    def _init_menu(self):
        self.my_menu = MyMenu(self)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.customContextMenuSlot)
        open_action = QAction(QIcon(MyIcon.FORDER_ICON), self.tr('Forder Open'), self)
        open_action.triggered.connect(self.__open_forder)
        del_action = QAction(QIcon(MyIcon.DELETE_ICON), self.tr('Delete File'), self)
        del_action.triggered.connect(self.__delete_file)
        remove_action = QAction(QIcon(MyIcon.REMOVE_ICON), self.tr('Remove from list'), self)
        remove_action.triggered.connect(self.__delete_list)
        self.my_menu.addActions([open_action, del_action, remove_action])
        self.my_menu.addSeparator()

    def customContextMenuSlot(self, pos):
        self.my_menu.popup(QtGui.QCursor.pos())

    def _init_panel_widget(self):
        #=========================================
        #∥       ∥ title
        #∥ thumb ∥ -------------------------------
        #∥       ∥ typeIcon / progressBar
        #=========================================

        #Thmbnail
        thumbnail_frame_size = QtCore.QSize((int)(self._height * 1.5), (self._height))
        self.pix = QPixmap('D:/CB_MacGyver/CB_MacGyver/1.png').scaled(thumbnail_frame_size, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio, transformMode=Qt.TransformationMode.SmoothTransformation)
        self.thumbnail = ThumbnailLabel(thumbnail_frame_size, None, self, self.info.state)
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
        self.title = MyLabel(self)
        self.title.setObjectName('Title')
        self.title.setFixedHeight((int)(self._height/2))
        self.title.setStyleSheet('#Title{border: 0; background-color: rgba(255, 0, 255, 0);}')
        self._top_layout.addWidget(self.title)

        #Panel Button
        self.pbt = PanelButtons(self)
        self._top_layout.addWidget(self.pbt)
        self.pbt.hide()
        self.pbt.add_list_del_btn_action(self.__delete_list)
        self.pbt.add_file_del_btn_action(self.__delete_file)
        self.pbt.add_open_file_btn_action(self.__open_forder)

        self._bottom_layout = QHBoxLayout()
        self._bottom_layout.setSpacing(1)
        self._bottom_layout.setContentsMargins(0, 0, 0, 0)
        self._work_layout.addLayout(self._bottom_layout)

        #Type Icon
        self.type_icon = QPushButton(self)
        # icon = type.icon_list[self.info.type]
        icon_size = QSize(25, 25)
        self.type_icon.setObjectName('Type_Icon')
        self.type_icon.setFixedSize(icon_size)
        self.type_icon.setIconSize(icon_size)
        self.type_icon.setStyleSheet('#Type_Icon{border: 0; background-color: rgba(255, 255, 255, 0);}')
        self.type_icon.setCursor(Qt.CursorShape.PointingHandCursor)
        self._bottom_layout.addWidget(self.type_icon)

        #Progress bar
        self.progress = CustomProgressBar(self, 100, height=5, background_color=QColor(222, 222, 222))
        self.progress.setBarWidth(100)
        self._bottom_layout.addWidget(self.progress)

        #Time
        self.time_widget = QLabel(self)
        self.time_widget.setObjectName('Time')
        self.time_widget.setStyleSheet('#Time{border: 0; background-color: rgba(255, 255, 255, 0);}')
        self.time_str = '00:00'
        self.time_widget.setText(self.time_str)
        self.time = 0
        self.progress.timer.timeout.connect(self._timer)
        self.time_widget.setContentsMargins(5, 0, 5, 0)
        self._bottom_layout.addWidget(self.time_widget)

        #temp space
        self.empty = QLabel(self)
        self.empty.setObjectName('Empty')
        self.empty.hide()
        self.empty.setStyleSheet('#Empty{border: 0; background-color: rgba(255, 255, 255, 0);}')
        self._bottom_layout.addWidget(self.empty)

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
       
        self.setStyleSheet("""
                QWidget#Panel{
                    background-color: rgba(%s);
                    border-width: 0.5px;
                    border-style: solid;
                    border-color: rgb(240, 240, 240);
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
            self.type_icon.released.connect(self.__open_web)
            self.thumbnail.setLoading(True)
            self.title.setText(self.info.name)
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
    
    def __delete_list(self):
        text = self.tr('Are you sure you want to delete this task from the list?')
        if self.__pop_message_box(self.tr('Delete List'), text) is False:
            return
        self.__del_widget()

    def __delete_file(self):
        text = self.tr('Are you sure you want to delete this file?')
        if self.__pop_message_box(self.tr('Delete File'), text) is False:
            return
        self.__del_file()
        self.__del_widget()

    def __pop_message_box(self, title, text:str = ''):
        qm = QMessageBox(self)
        qm.setTextFormat(Qt.TextFormat.RichText)
        qm.setIcon(QMessageBox.Icon.Warning)
        qm.setWindowTitle(title)
        qm.setText(text + '<br><br>' + '<font color="red">%s</font>'% self.title.txt)
        yes_btn = qm.addButton(self.tr('&Yes'), QMessageBox.ButtonRole.YesRole)
        yes_btn.setShortcut(QKeySequence(Qt.Key.Key_Y))
        no_btn = qm.addButton(self.tr('&No'), QMessageBox.ButtonRole.NoRole)
        no_btn.setShortcut(QKeySequence(Qt.Key.Key_N))
        qm.setDefaultButton(yes_btn)
        
        reply = qm.exec_()

        if reply == 0:
            return True
        else:
            return False
        # ret = qm.warning(self, title, text + '<br><br>' + '<font color="red">%s</font>'% self.title.txt, buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, defaultButton=QMessageBox.StandardButton.Yes)
        ret = QMessageBox.warning(self, title, text, buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, defaultButton=QMessageBox.StandardButton.Yes)
        
        # if ret == QMessageBox.StandardButton.Yes:
        #     return True
        # else:
        #     return False
        # qm = QMessageBox(self)
        # qm.setWindowTitle(title)
        # qm.addButton(self.tr('Yes'), QMessageBox.ButtonRole.YesRole)
        # qm.addButton(self.tr('No'), QMessageBox.ButtonRole.NoRole)
        
        # reply = qm.exec_()

        # if reply == 0:
        #     return True
        # else:
        #     return False

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
    
    def __open_web(self):
        webbrowser.open_new(self.info.url)
        #os.system("start chrome %s"%self.info.url)

    def set_item(self, item):
        self.item = item

