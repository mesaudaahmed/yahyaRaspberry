from PyQt5.QtWidgets import (QApplication, QMainWindow,QMessageBox,QDialog)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
import sys
from main_window_ui import Ui_MainWindow
from insert_window_ui import Ui_insertWindow
import sqlite3
from functions import *
import time
#the main window class 
class main_window(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(main_window,self).__init__()
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
        """" get curent page and last page 
        whene user hit the next button this function shows the next GuiRowCount database"""
        adder=0
        adder = 1 if self.get_dataRows()/self.get_GuiRowCount()-self.get_dataRows()//self.get_GuiRowCount()>0 else 0
        last_page=self.get_dataRows()//self.get_GuiRowCount()+adder
        if self.CurrentPages==0:
            # QMessageBox.warning(self, "Error Message","The passwords you entered do not match. Please try again.",QMessageBox.Close,QMessageBox.Close)
            QMessageBox.warning(self,"warning","you already in fisrt page",QMessageBox.Close,QMessageBox.Close)
        else:
            
            tablerow=0
            for index,row in enumerate(self.get_databaseRows()): 
                if index>=(self.CurrentPages-2)*self.get_GuiRowCount():
                    for i in range(self.get_columCount()):
                        self.tableWidget.setItem(tablerow,i,QtWidgets.QTableWidgetItem(str(row[i])))
                    tablerow +=1
            self.CurrentPages-=1
            print("prev page",self.CurrentPages,'/',last_page)

    def OnNextPage(self):
        adder=0
        adder = 1 if self.get_dataRows()/self.get_GuiRowCount()-self.get_dataRows()//self.get_GuiRowCount()>0 else 0
        last_page=self.get_dataRows()//self.get_GuiRowCount()+adder
        if self.CurrentPages==last_page:
            QMessageBox.warning(self,"warning","you already in last page",QMessageBox.Close,QMessageBox.Close)
        else:
            tablerow=0
            for index,row in enumerate(self.get_databaseRows()): 
                if index>=(self.CurrentPages+1)*self.get_GuiRowCount():
                    for i in range(self.get_columCount()):
                        self.tableWidget.setItem(tablerow,i,QtWidgets.QTableWidgetItem(str(row[i])))
                    tablerow +=1

            self.CurrentPages+=1
            print("next page",self.CurrentPages,'/',last_page)

    def addTagClicked(self):
        print(self.pushButton_6.text())
        addtagwindow=InsertWindow()
        addtagwindow.show()
        
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

#insert window class
class InsertWindow(QMainWindow,Ui_insertWindow):
    def __init__(self):
        super(InsertWindow,self).__init__()
        self.setupUi(self)
        self.device="esp00"
        self.tag="0000"
        self.ReloadTime=0
        self.eatState=0
        self.relayState=0
        self.R1Start=0
        self.R2Start=0
        self.R3Start=0
        self.R1End=0
        self.R2End=0
        self.R3End=0
        self.days=0
        
        self.pushButton.clicked.connect(lambda:self.insertDataButton())
    def insertDataButton(self):
        self.setValue()
        insertdata(self.device,self.tag,datetime.now(),self.ReloadTime,self.relayState,self.eatState,str(self.R1Start)+"#"+str(self.R1End),str(self.R2Start)+"#"+str(self.R2End),str(self.R3Start)+"#"+str(self.R3End),self.days)
    def setValue(self):
        self.device=self.lineEdit.text()
        self.tag=self.lineEdit_2.text()
        self.ReloadTime=self.lineEdit_3.text()
        self.eatState=self.checkBox.checkState()#either 2 or 0
        self.R1Start=self.spinBox.value()
        self.R2Start=self.spinBox_3.value()
        self.R3Start=self.spinBox_5.value()
        self.R1End=self.spinBox_2.value()
        self.R2End=self.spinBox_4.value()
        self.R3End=self.spinBox_6.value()
        self.days=self.spinBox_7.value()
if __name__ =="__main__":
    app=QApplication(sys.argv)
    win=main_window()
    win.show()
    sys.exit(app.exec())