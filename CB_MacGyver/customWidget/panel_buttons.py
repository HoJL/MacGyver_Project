from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from customWidget.iconbutton import IconButton
from paths import MyIcon

class PanelButtons(QWidget):

    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)

        self.button_layout = QHBoxLayout()
        self.setLayout(self.button_layout)
        
        folder_img_url = MyIcon.FORDER_ICON
        file_del_url = MyIcon.DELETE_ICON
        list_del_url = MyIcon.REMOVE_ICON

        self.open_file_location_btn = self.__create_button(folder_img_url)
        self.open_file_location_btn.set_pixmap_hover_color(QColor(0, 0, 0))

        self.file_del_btn = self.__create_button(file_del_url)
        self.file_del_btn.set_pixmap_hover_color(QColor(255, 0, 0))
        
        self.list_del_btn = self.__create_button(list_del_url)
        self.list_del_btn.set_pixmap_hover_color(QColor(0, 0, 0))

        self.button_layout.addWidget(self.open_file_location_btn)
        self.button_layout.addWidget(self.file_del_btn)
        self.button_layout.addWidget(self.list_del_btn)
        
        spacing = 5
        margin = 5
        self.button_layout.setSpacing(spacing)
        self.button_layout.setContentsMargins(margin, 0, margin, 0)
        self.setFixedWidth(self.file_del_btn.width() * 3 + spacing * 3 + margin * 2)

    def __create_button(self, icon_url, size: QSize = QSize(20, 20)) -> IconButton:
        btn = IconButton(self)
        btn.setPixmap(icon_url)
        btn.setIconSize(size)
        return btn
        
    def addButtonAction(self, open_file_slot, file_del_slot, list_del_slot):
        self.open_file_location_btn.clicked.connect(open_file_slot)
        self.file_del_btn.clicked.connect(file_del_slot)
        self.list_del_btn.clicked.connect(list_del_slot)

    def add_open_file_btn_action(self, slot):
        self.open_file_location_btn.clicked.connect(slot)

    def add_file_del_btn_action(self, slot):
        self.file_del_btn.clicked.connect(slot)

    def add_list_del_btn_action(self, slot):
        self.list_del_btn.clicked.connect(slot)
    
