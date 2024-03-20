from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton
from customWidget.iconbutton import IconButton
import paths

class PanelButtons(QWidget):

    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)

        self.button_layout = QHBoxLayout()
        self.setLayout(self.button_layout)
        
        folder_img_url = paths.IMAGE_DIR + '/folder_icon.png'
        file_del_url = paths.IMAGE_DIR + '/trash_icon.png'
        list_del_url = paths.IMAGE_DIR + '/delete_icon.png'

        self.open_file_location_btn = self.__create_button(folder_img_url)
        self.open_file_location_btn.set_pixmap_hover_color(QColor(0, 0, 0))

        self.file_del_btn = self.__create_button(file_del_url)
        self.file_del_btn.set_pixmap_hover_color(QColor(255, 0, 0))
        
        self.list_del_btn = self.__create_button(list_del_url)
        self.list_del_btn.set_pixmap_hover_color(QColor(0, 0, 0))

        self.button_layout.addWidget(self.open_file_location_btn)
        self.button_layout.addWidget(self.file_del_btn)
        self.button_layout.addWidget(self.list_del_btn)
        self.button_layout.setSpacing(5)

        self.setFixedWidth(self.file_del_btn.width() * 3 +20)

    def __create_button(self, icon_url) -> IconButton:
        btn = IconButton(self)
        btn.setPixmap(icon_url)
        return btn
        