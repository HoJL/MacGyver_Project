from PyQt5.QtGui import QContextMenuEvent, QCursor
from PyQt5.QtWidgets import QLineEdit, QAction
from PyQt5.QtCore import Qt, QLocale, QCoreApplication
from customWidget.myMenu import MyMenu

class CustomLineEdit(QLineEdit):

    def __init__(self, parent):
       
        super(CustomLineEdit, self).__init__(parent)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.setObjectName('CustomEdit')
        self.setStyleSheet("""
            QLineEdit#CustomEdit {
                border-style: solid;
                border-width: 1px;
                border-color: rgb(200, 200, 200);
                border-radius: 4px;
            }
            QLineEdit:hover#CustomEdit {
                border-color: rgb(200, 0, 0);
            }
            QLineEdit:focus#CustomEdit {
                border-width: 1.5px;
                border-color: rgb(200, 0, 0);
            }
            """
        )
        ko = QLocale(QLocale.Language.Korean, QLocale.Country.SouthKorea)
        self.setLocale(ko)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__menu_popup_slot)
        translate = QCoreApplication.translate

        self.my_menu = MyMenu(self)
        self.undo_action = QAction(translate('CustomLineEdit', '&Undo'), self)
        self.redo_action = QAction(translate('CustomLineEdit', '&Redo'), self)
        self.cut_action = QAction(translate('CustomLineEdit', 'Cu&t'), self)
        self.copy_action = QAction(translate('CustomLineEdit', '&Copy'), self)
        self.paste_action = QAction(translate('CustomLineEdit', '&Paste'), self)
        self.delete_action = QAction(translate('CustomLineEdit', 'Delete'), self)
        self.select_all_action = QAction(translate('CustomLineEdit', 'Select All'), self)

        custom_action_list = [self.undo_action, self.redo_action, self.cut_action, self.copy_action, self.paste_action, self.delete_action, self.select_all_action]
        self.st_menu = self.createStandardContextMenu()

        action_list = self.st_menu.actions()
        cnt = 0
        for ac in action_list:
            if ac.isSeparator():
                continue
            custom_action_list[cnt].triggered.connect(ac.trigger)
            list_str = ac.text().split('\t')
            if len(list_str) == 2:
                custom_action_list[cnt].setShortcut(list_str[1])

            cnt += 1
            if cnt >= len(custom_action_list):
                break

        self.my_menu.addActions([self.undo_action, self.redo_action])
        self.my_menu.addSeparator()
        self.my_menu.addActions([self.cut_action, self.copy_action, self.paste_action, self.delete_action])
        self.my_menu.addSeparator()
        self.my_menu.addAction(self.select_all_action)
        self.my_menu.setStyleSheet(self.my_menu.styleSheet() + """
                QMenu::item#MyMenu {
                        width: 140px;
                    } 
        """)

    def __menu_popup_slot(self, pos):
        self.redo_action.setEnabled(self.isRedoAvailable())
        self.undo_action.setEnabled(self.isUndoAvailable())
        if self.selectedText() != '':
            self.cut_action.setEnabled(True)
            self.copy_action.setEnabled(True)
            self.delete_action.setEnabled(True)
        else:
            self.cut_action.setEnabled(False)
            self.copy_action.setEnabled(False)
            self.delete_action.setEnabled(False)
        
        if self.text() != '':
            self.select_all_action.setEnabled(True)
        else:
            self.select_all_action.setEnabled(False)

        self.my_menu.exec_(QCursor.pos())
