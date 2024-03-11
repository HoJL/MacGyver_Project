from PyQt5.QtCore import QTranslator, QCoreApplication
from PyQt5.QtWidgets import QApplication

class Translator:
    def __init__(self, app: QApplication, file: str = None) -> None:
        self._tr = QTranslator()
        self._app = app
        self.changeLanguage(file)
        
    
    def changeLanguage(self, file: str) -> None:
        if (file == None): return None
        tr = QTranslator()
        if (tr.load(file) == False): return None
        self._app.removeTranslator(self._tr)
        self._app.installTranslator(tr)
        self._tr = tr