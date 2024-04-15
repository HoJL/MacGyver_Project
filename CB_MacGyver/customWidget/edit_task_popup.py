from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QDialog
from PyQt5.QtGui import QPalette, QColor
from customWidget.custom_line_edit import CustomLineEdit

class EditTaskPopup(QDialog):

    RES_OK = 1
    RES_CANCEL = -1
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.WindowContextHelpButtonHint, False)
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
        self.setWindowTitle(self.tr('Edit task'))
        # self.setFixedSize(350, 350)
        self.setMinimumWidth(300)
        self.resize(400, 400)
        pal = QPalette()
        pal.setBrush(QPalette.ColorRole.Background, QColor(255, 255, 255))
        self.setPalette(pal)
        self.base_layout = QGridLayout()
        self.setLayout(self.base_layout)
        self.res = 0
        # self.base_layout.addWidget(QLabel(self.tr('Title')), 0, 0)
        # self.base_layout.addWidget(QLabel(self.tr('File')), 1, 0)
        # self.base_layout.addWidget(QLabel(self.tr('Forder')), 2, 0)
        # self.title_edit = CustomLineEdit(self)
        # self.file_edit = CustomLineEdit(self)
        # self.forder_edit = CustomLineEdit(self)
        # self.base_layout.addWidget(self.title_edit, 0, 1)
        # self.base_layout.addWidget(self.file_edit, 1, 1)
        # self.base_layout.addWidget(self.forder_edit, 2, 1)
        self.title_edit = self.add_label_and_edit('Ttile', 0)
        self.file_edit = self.add_label_and_edit('File', 1)
        self.forder_edit = self.add_label_and_edit('Forder', 2)

        self.base_layout.setRowStretch(3, 1)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch(4)
        self.ok_btn = QPushButton('OK', self)
        self.ok_btn.clicked.connect(self.__ok_slot)
        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(self.__cancel_slot)
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        self.base_layout.addLayout(btn_layout, 4, 0, 1, 0)

    def add_label_and_edit(self, title, row):
        self.base_layout.addWidget(QLabel(title), row, 0)
        edit = CustomLineEdit(self)
        self.base_layout.addWidget(edit, row, 1)
        return edit

    def set_data(self, title, file_name, forder):
        self.title_edit.setText(title)
        self.file_edit.setText(file_name)
        self.forder_edit.setText(forder)

    def __cancel_slot(self):
        self.res = self.RES_CANCEL
        self.close()

    def __ok_slot(self):
        self.res = self.RES_OK
        self.close()