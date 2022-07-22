from PyQt5.QtWidgets import (QApplication, QMainWindow,QMessageBox,QDialog)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import sys
from main_window_ui import Ui_MainWindow
import sqlite3
class window(QMainWindow,Ui_MainWindow):
    def __init__(self ,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.load_data()
    def load_data(self):
        conn=sqlite3.connect("clientData.db")
        cursor=conn.cursor()
        query="SELECT * FROM EspData"
        tablerow=0
        for row in cursor.execute(query):
            for i in range(10):
                self.tableWidget.setItem(tablerow,i,QtWidgets.QTableWidgetItem(str(row[i])))
            tablerow +=1
if __name__ =="__main__":
    app=QApplication(sys.argv)
    win=window()
    win.show()
    sys.exit(app.exec())