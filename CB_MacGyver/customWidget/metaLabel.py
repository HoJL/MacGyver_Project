from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QAction
from PyQt5.QtGui import QPixmap, QIcon, QFont
from paths import MyIcon

class MetaLabel(QWidget):

    def __init__(self, parent: QWidget | None) -> None:
        super().__init__(parent)

        self.box_layout = QHBoxLayout()
        self.box_layout.setSpacing(1)
        self.box_layout.setContentsMargins(5, 0, 5, 0)
        self.setLayout(self.box_layout)
        self.time_pix_label, self.time_label = self.__init_label('00:00', MyIcon.TIME_ICON)
        self.size_pix_label, self.size_label = self.__init_label('140MB', MyIcon.DISK_ICON)
        self.setFixedWidth(self.time_label.width() + self.size_label.width() + self.time_pix_label.width() + self.size_pix_label.width() + 30)

    def setTimeText(self, text):
        self.time_label.setText(text)

    def setSizeText(self, text):
        self.size_label.setText(text)

    def __init_label(self, text, pixmap):
        pix_label = QLabel(self)
        self.box_layout.addWidget(pix_label)
        pix = QPixmap(pixmap).scaled(22, 22, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        pix_label.setPixmap(pix)
        pix_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pix_label.adjustSize()

        label = QLabel(self)
        self.box_layout.addWidget(label)
        label.setText(text)
        label.setStyleSheet("color: rgb(120, 120, 120)")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.adjustSize()

        return pix_label, label