import sys
from PyQt5.QtGui import QCloseEvent, QPaintEvent
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from translator import Translator
from customWidget import *
import paths
from paths import MyIcon
import downloading
import save_load
import threading
#기본적으로 png이미지를 불러올때 pyqt ICC 프로파일에 맞지않는 경우가 많음
#color 즉 sRGB 프로파일 문제일 확률이 높음
#해결방법: 포토샵에서 웹용으로 저장을 선택하여 png-8을 선택하고 저장하면 해결
#기본적으로 그냥저장하면 RGB프로파일이아닌 CMYK프로파일을 기본적으로 사용하기때문에 RGB를 기본으로 사용하는 웹용으로 저장하는것
#test m3u8 https://cph-p2p-msl.akamaized.net/hls/live/2000341/test/master.m3u8
class MainWindow(QMainWindow):

    WIN_W = 540
    WIN_H = 600
    sig = pyqtSignal()
    def __init__(self, app: QApplication) -> None:
        super().__init__()
        self.initUI(app)

    def initUI(self, app: QApplication):
        self.resize(self.WIN_W, self.WIN_H)
        self.setMinimumSize(450, 400)
        self.MoveWinCenter()
        self.setWindowTitle("MacGyver_CB")
        self.setWindowIcon(QIcon(MyIcon.WIN_ICON))

        self.exitAction = QAction(QIcon(MyIcon.EXIT_ICON), 'Exit', self)
        self.exitAction.setShortcut('Alt+F4')
        self.exitAction.triggered.connect(app.closeAllWindows)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        self.tasks = menubar.addMenu('Tasks')
        self.tasks.addAction(self.exitAction)
        self.tray_opt_action = QAction(self.tr('Minimize to tray on close'), self)
        self.tray_opt_action.setCheckable(True)

        option_menu = menubar.addMenu(self.tr('Option'))
        option_menu.addAction(self.tray_opt_action)
        mainGrid = QGridLayout()
        downloadGrid = QGridLayout()
        self.edit = CustomIconEdit(self)
        bt = DownloadButton(self.edit, self)
        downloadGrid.addWidget(self.edit, 0, 0)
        downloadGrid.addWidget(bt, 0, 1)
        downloadGrid.setContentsMargins(6, 6, 6, 6)
        downloadGrid.setHorizontalSpacing(6)
        bt.clicked.connect(self.download)

        self.contentGrid = QGridLayout()
        self.content = QWidget(self)
        self.content.setObjectName('Content')
        self.content.setStyleSheet('#Content{background-color: rgb(255, 255, 255);}')

        scroll_area = QScrollArea()
        scroll_area.setObjectName('Scroll_Area')
        scroll_area.setStyleSheet('#Scroll_Area{border: 0px;}')
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        rt = self.content.geometry()
        scroll_area.setGeometry(rt)
        scroll_area.setWidgetResizable(True)

        self.ly = QVBoxLayout()
        self.ly.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.ly.setSpacing(0)
        self.ly.setContentsMargins(0, 0, 0, 0)

        self.listView = QListWidget(self)
        self.listView.setObjectName('ListView')
        self.listView.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.listView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.listView.setStyleSheet("""
        #     QListWidget::item:hover{
        #         background-color: rgb(192, 0, 0);        
        #     }
        #     QListWidget::item:selected:hover{ 
        #         background-color: rgb(192, 0, 0); 
        #     }
        #     QListWidget::item:selected:active{ 
        #         background-color: rgb(192, 0, 0); 
        #     }                 
        #     """)
        self.ly.addWidget(self.listView)
        self.content.setLayout(self.ly)

        scroll_area.setWidget(self.content)
        self.contentGrid.addWidget(scroll_area, 0, 0, 1, 0)

        self.status = QWidget(self)
        self.status.setObjectName('Status')
        self.status.setStyleSheet('#Status{background-color: rgb(222, 222, 222);}')
        self.status.setFixedHeight(64)
        status_layout = QGridLayout()
        status_layout.addWidget(self.status, 0, 0, 1, 0)
        #self.contentGrid.addWidget(self.status, 1, 0, 1, 0)

        mainGrid.addLayout(downloadGrid, 0, 0, 1, 0)
        mainGrid.addLayout(self.contentGrid, 1, 0, 1, 0)
        mainGrid.addLayout(status_layout,2, 0, 1, 0)
        mainGrid.setContentsMargins(0, 0, 0, 0)
        mainGrid.setVerticalSpacing(2)
        widget = QWidget()
        widget.setLayout(mainGrid)
        self.setCentralWidget(widget)
        self.sig.connect(self.start_download)
        self.show()

        self.tray = QSystemTrayIcon(QIcon(MyIcon.WIN_ICON), self)
        self.tray.show()
        self.tray.activated.connect(self.__tray_activated)
        tray_menu = QMenu()
        self.tray_exitAction = QAction(QIcon(MyIcon.EXIT_ICON), self.tr('Exit'), self)
        self.tray_exitAction.triggered.connect(self.tray_close)
        tray_menu.addAction(self.tray_exitAction)
        self.retranslateUi()
        self.tray.setContextMenu(tray_menu)
        save_load.load(self.listView)

    def MoveWinCenter(self):
        '''창을 모니터 중앙으로 위치하게 하는 함수
        '''
        fg = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

    def retranslateUi(self):
        '''언어팩에 따른 UI언어번역
        '''
        self.exitAction.setText(self.tr('Exit'))
        self.exitAction.setStatusTip(self.tr('Exit'))
        self.tasks.setTitle(self.tr('Tasks'))

    def download(self):
        self.sig.emit()

    def start_download(self):

        di = self.edit.getCurrentTypeAndUrl()
        if di.url is None or di.url == '':
            print('Url을 입력해 주세요')
            return

        down = downloading.Downloading(di, self.listView)
        down.start()

    def closeEvent(self, a0: QCloseEvent | None) -> None:
        if self.isHidden() is False:
            if self.tray_opt_action.isChecked():
                a0.ignore()
                self.hide()
                return
        save_load.save(self.listView)
    
    def tray_close(self):
        save_load.save(self.listView)
        QApplication.quit()
    
    def __tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show()

import ctypes
import os

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # myappid = u'mycompany.myproduct.subproduct.version' # arbitrary string
    # ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    ic = MyIcon.WIN_ICON
    app_icon = QIcon()
    app_icon.addFile(ic, QSize(16,16))
    app_icon.addFile(ic, QSize(24,24))
    app_icon.addFile(ic, QSize(32,32))
    app_icon.addFile(ic, QSize(48,48))
    app_icon.addFile(ic, QSize(256,256))
    app.setWindowIcon(app_icon)
    # app.setStyle(QStyleFactory.create('fusion'))
    trPath = paths.BASE_DIR + '/qt5_ko_kr.qm'
    trr = Translator(app, trPath)
    fontDB = QFontDatabase()
    fontDB.addApplicationFont('D:/MacGyver_Project/CB_MacGyver/font/HakgyoansimBareondotumB.ttf')
    app.setFont(QFont('학교안심 바른돋움 B', 11))
    main = MainWindow(app)

    sys.exit(app.exec_())