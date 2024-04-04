from PyQt5.QtCore import Qt, QMargins
from PyQt5.QtWidgets import QMenu, QAction, QProxyStyle, QStyle, QStyleOption, QWidget
from PyQt5.QtGui import QIcon

from paths import MyIcon


class MyStyle(QProxyStyle):
    def pixelMetric(self, metric: QStyle.PixelMetric, option: QStyleOption | None = ..., widget: QWidget | None = ...) -> int:
        return 20

class MyMenu(QMenu):
    
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint | 
                            Qt.WindowType.NoDropShadowWindowHint)

        self.setStyle(MyStyle())
        self.setContentsMargins(4, 4, 4, 4)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setObjectName('MyMenu')
        self.setStyleSheet("""
                QMenu#MyMenu {
                    background-color: rgb(255, 255, 255);
                    margin: 2px;
                    font-size: 14px;
                    border: 0.5px solid rgb(222,222,222);
                    border-radius: 4px;
                }
                QMenu::item#MyMenu {
                    spacing: 0px;
                    height: 30px;
                    width: 200px;
                }
                QMenu::item:selected#MyMenu {
                    background-color: rgb(180, 200, 200);
                    border-radius: 4px;
                }
        """)

        self.adjustSize()
