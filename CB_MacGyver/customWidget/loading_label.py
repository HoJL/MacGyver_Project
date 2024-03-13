
from PyQt5 import QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QLabel, QWidget
import paths

class Loading_Label(QLabel):
    
    loading_icon = paths.IMAGE_DIR + '/loading_spin.gif'

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        palette = QtGui.QPalette(self.palette())
        palette.setColor(palette.ColorRole.Background, Qt.GlobalColor.transparent)
        self.setPalette(palette)
        self.setFixedSize(QSize(35, 35))
        self.loading = QtGui.QMovie(self.loading_icon)
        self.loading.setScaledSize(QSize(35, 35))
        self.setMovie(self.loading)
        self.hide()


    def start(self):
        self.show()
        self.loading.start()

    def stop(self):
        self.hide()
        #self.loading.stop()