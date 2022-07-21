from PyQt5.QtWidgets import (QApplication, QMainWindow,QMessageBox,QDialog)
from PyQt5.uic import loadUi
import sys
from main_window_ui import Ui_MainWindow
class window(QMainWindow,Ui_MainWindow):
    def __init__(self ,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        
if __name__ =="__main__":
    app=QApplication(sys.argv)
    win=window()
    win.show()
    sys.exit(app.exec())