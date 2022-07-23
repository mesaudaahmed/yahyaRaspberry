from PyQt5.QtWidgets import (QApplication, QMainWindow,QMessageBox,QDialog)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import sys
from main_window_ui import Ui_MainWindow
import sqlite3
from functions import *
class window(QMainWindow,Ui_MainWindow):
    def __init__(self ,parent=None):
        super(window, self).__init__(parent)
        self.setupUi(self)
        self.CurrentPages=0
        self.load_data()
        self.pushButton_4.clicked.connect(lambda : self.OnPrevPage())#whene next page buttun clicked 
        self.pushButton_5.clicked.connect(lambda : self.OnNextPage())#whene previes page buttun clicked 
        self.pushButton_6.clicked.connect(lambda : self.addTagClicked())#whene we want to add tag data 
        self.pushButton_7.clicked.connect(lambda : self.deleteTagClicked())#delete an existing tag data
        self.pushButton_8.clicked.connect(lambda : self.editeTagClicked())#edite an existing tag data
        self.pushButton_9.clicked.connect(lambda : self.searchTagClicked())#search a tag data
        self.pushButton.clicked.connect(lambda : self.resetClicked())#resset all user interface data
        self.pushButton_3.clicked.connect(lambda : self.connectionClicked())#check the connection with esp device data 
        self.pushButton_10.clicked.connect(lambda : self.setupClicked())#send config data to 
    #load database table from esp to qtablewidget for 5 rows and n couloms
    #get how colums in qtablewidget
    def get_columCount(self):
        return self.tableWidget.columnCount()
    #get how meany row in qtablewidget
    def get_GuiRowCount(self):
        return self.tableWidget.rowCount()
    #get how meany rows in database
    def get_dataRows(self):
        return rowCounter()
    #return database rows
    def get_databaseRows(self):
        conn=sqlite3.connect("clientData.db")
        cursor=conn.cursor()
        query="SELECT * FROM EspData"
        return cursor.execute(query)
    def load_data(self):
        print(self.CurrentPages)
        tablerow=0
        for index,row in enumerate(self.get_databaseRows()):
            for i in range(self.get_columCount()):
                self.tableWidget.setItem(tablerow,i,QtWidgets.QTableWidgetItem(str(row[i])))
            tablerow +=1
        print(self.get_dataRows())

    def OnPrevPage(self):
        adder=0
        adder = 1 if self.get_dataRows()/self.get_GuiRowCount()-self.get_dataRows()//self.get_GuiRowCount()>0 else 0
        last_page=self.get_dataRows()//self.get_GuiRowCount()+adder
        if self.CurrentPages==0:
            # QMessageBox.warning(self, "Error Message","The passwords you entered do not match. Please try again.",QMessageBox.Close,QMessageBox.Close)
            QMessageBox.warning(self,"warning","you already in fisrt page",QMessageBox.Close,QMessageBox.Close)
        else:
            
            tablerow=0
            for index,row in enumerate(self.get_databaseRows()): 
                if index>=self.CurrentPages*self.get_GuiRowCount():
                    for i in range(self.get_columCount()):
                        self.tableWidget.setItem(tablerow,i,QtWidgets.QTableWidgetItem(str(row[i])))
                    tablerow +=1
            
            self.CurrentPages-=1
            print("prev page",self.CurrentPages)

    def OnNextPage(self):
        adder=0
        adder = 1 if self.get_dataRows()/self.get_GuiRowCount()-self.get_dataRows()//self.get_GuiRowCount()>0 else 0
        last_page=self.get_dataRows()//self.get_GuiRowCount()+adder
        if self.CurrentPages==last_page:
            QMessageBox.warning(self,"warning","you already in last page",QMessageBox.Close,QMessageBox.Close)
        else:
            tablerow=0
            for index,row in enumerate(self.get_databaseRows()): 
                if index>=self.CurrentPages*self.get_GuiRowCount():
                    for i in range(self.get_columCount()):
                        self.tableWidget.setItem(tablerow,i,QtWidgets.QTableWidgetItem(str(row[i])))
                    tablerow +=1

            self.CurrentPages+=1
            print("next page",self.CurrentPages)

    def addTagClicked(self):
        print(self.pushButton_6.text())
    def deleteTagClicked(self):
        print(self.pushButton_7.text())
    def editeTagClicked(self):
        print(self.pushButton_8.text())
    def searchTagClicked(self):
        print(self.pushButton_9.text())
    def resetClicked(self):
        print(self.pushButton.text())
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.spinBox.setValue(0)
        self.spinBox_2.setValue(0)
        self.spinBox_3.setValue(0)
        self.spinBox_4.setValue(0)
        self.spinBox_5.setValue(0)
        self.spinBox_6.setValue(0)
        self.load_data()
        self.CurrentPages=0
    def connectionClicked(self):
        print(self.pushButton_3.text())
    def setupClicked(self):
        print(self.pushButton_10.text())
if __name__ =="__main__":
    app=QApplication(sys.argv)
    win=window()
    win.show()
    sys.exit(app.exec())