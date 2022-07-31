from turtle import color
from PyQt5.QtWidgets import (QWidget ,QApplication, QMainWindow,QMessageBox,QDialog,QLabel)
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.uic import loadUi
import sys
from classes.main_window_ui import Ui_MainWindow
from classes.insert_window_ui import Ui_insertWindow
from classes.delete_window_ui import Ui_deleteWindow
from classes.setting_dialog__ui import Ui_Dialog
import sqlite3
from functions.database import *
from functions.mqtt import *
#the main window class 
class main_window(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(main_window,self).__init__(parent)
        self.setupUi(self)
        self.CurrentPages=0
        self.action_Stop.setDisabled(True)
        self.thread={}
        
        #get the mqtt parametres
        self.mqtt_username = getSetting("setting")["mqtt_username"]
        self.mqtt_password = getSetting("setting")["mqtt_password"]
        self.mqtt_topic = getSetting("setting")["mqtt_topic"]
        self.mqtt_broker_ip = getSetting("setting")["mqtt_broker_ip"]   
        self.mqtt_port = getSetting("setting")["mqtt_port"]
        self.thread[1] = ThreadClass(index=1,
                                     mqtt_username=self.mqtt_username,
                                     mqtt_password=self.mqtt_password,
                                     mqtt_topic=self.mqtt_topic,
                                     mqtt_broker_ip=self.mqtt_broker_ip,
                                     mqtt_port=self.mqtt_port
                                     )
        #load the data on qtable widget   
        self.load_data()
        #creat buttons clicked event
        self.pushButton_4.clicked.connect(lambda : self.OnPrevPage())#whene next page buttun clicked 
        self.pushButton_5.clicked.connect(lambda : self.OnNextPage())#whene previes page buttun clicked 
        self.pushButton_6.clicked.connect(lambda : self.addTagClicked())#whene we want to add tag data 
        self.pushButton_7.clicked.connect(lambda : self.deleteTagClicked())#delete an existing tag data
        self.pushButton_8.clicked.connect(lambda : self.editeTagClicked())#edite an existing tag data
        self.pushButton_9.clicked.connect(lambda : self.searchTagClicked())#search a tag data
        self.pushButton.clicked.connect(lambda : self.resetClicked())#resset all user interface data
        self.pushButton_3.clicked.connect(lambda : self.connectionClicked())#check the connection with esp device data 
        self.pushButton_10.clicked.connect(lambda : self.setupClicked())#send config data to 
        """the follwing event is for actions events"""
        self.action_Start.triggered.connect(lambda : self.startAction())
        self.action_Stop.triggered.connect(lambda : self.stopAction())
        self.action_Setting.triggered.connect(lambda : self.settingAction())
        self.action_Exit.triggered.connect(lambda : self.exitAction())
        self.action_About.triggered.connect(lambda : self.aboutAction())
        """the fllowing events are for sending ON OFF action
        to a specifice esp device"""
        self.pushButton_2.clicked.connect(lambda:self.r1ON())#activate relay 1
        self.pushButton_11.clicked.connect(lambda:self.r1OFF())#deactivate relay 1
        self.pushButton_12.clicked.connect(lambda:self.r2ON())#activate relay 2
        self.pushButton_13.clicked.connect(lambda:self.r2OFF())#deactivate relay 2
        self.pushButton_14.clicked.connect(lambda:self.r3ON())#activate relay 3
        self.pushButton_15.clicked.connect(lambda:self.r3OFF())#deactivate relay 3
        self.pushButton_16.clicked.connect(lambda:self.allON())#deactivate relay 3
        self.pushButton_17.clicked.connect(lambda:self.allOFF())#deactivate relay 3
    def startAction(self):
        self.thread[1].start()
        # self.thread[1].any_signal.connect(self.my_function)
        self.action_Stop.setDisabled(False)
        self.action_Start.setDisabled(True)
    def stopAction(self):
        self.thread[1].stop() 
        self.thread[1].quit()     
        self.thread[1].wait()
        self.action_Stop.setDisabled(True)
        self.action_Start.setDisabled(False)
    def settingAction(self):
        settingwindow=SettingDialog()
        settingwindow.show()
    def exitAction(self):
        self.close()
    def aboutAction(self):
        QMessageBox.about(self,"about","<font size = 8> smart farmer gardien for eating cycles for sheeps </font> ")
    def checkDeviceName(self,devicename):
        if devicename=="" or devicename[0:3]!="esp" or len(devicename)!=5:
            QMessageBox.warning(self,"Warning","<font size = 8> your device name is incorrect </font> ")
            return False
        else:
            try:
                int(devicename[3:5])
            except:
                QMessageBox.warning(self,"Warning","<font size = 8> your device number is incorrect </font> ")
                return False
    #activate relay 1
    def r1ON(self):
        if self.checkDeviceName(self.lineEdit_3.text()) ==False:
            return False
        else:
            loading=Loading()
            loading.show()
            # Set the username and password for the MQTT client
            client.username_pw_set(self.mqtt_username, self.mqtt_password)
            client.connect(self.mqtt_broker_ip, int(self.mqtt_port))
            # client.subscribe(self.lineEdit_3.text()+"/R1")
            topic=self.lineEdit_3.text()+"/R1"
            client.publish(topic,"1")
            print("send on relay 1")
            loading.close()
    #deactivate relay 1
    def r1OFF(self):
        if self.checkDeviceName(self.lineEdit_3.text()) ==False:
            return False
        else:
            loading=Loading()
            loading.show()
            # Set the username and password for the MQTT client
            client.username_pw_set(self.mqtt_username, self.mqtt_password)
            client.connect(self.mqtt_broker_ip, int(self.mqtt_port))
            # client.subscribe(self.lineEdit_3.text()+"/R1")
            topic=self.lineEdit_3.text()+"/R1"
            client.publish(topic,"0")
            print("send off relay 1")
            loading.close()
    #activate relay 2
    def r2ON(self):
        if self.checkDeviceName(self.lineEdit_3.text()) ==False:
            return False
        else:
            loading=Loading()
            loading.show()
            # Set the username and password for the MQTT client
            client.username_pw_set(self.mqtt_username, self.mqtt_password)
            client.connect(self.mqtt_broker_ip, int(self.mqtt_port))
            # client.subscribe(self.lineEdit_3.text()+"/R1")
            topic=self.lineEdit_3.text()+"/R2"
            client.publish(topic,"1")
            print("send on relay 2")
            loading.close()
    #deactivate relay 2
    def r2OFF(self):

        if self.checkDeviceName(self.lineEdit_3.text()) ==False:
            return False
        else:
            loading=Loading()
            loading.show()
            # Set the username and password for the MQTT client
            client.username_pw_set(self.mqtt_username, self.mqtt_password)
            client.connect(self.mqtt_broker_ip, int(self.mqtt_port))
            # client.subscribe(self.lineEdit_3.text()+"/R1")
            topic=self.lineEdit_3.text()+"/R2"
            client.publish(topic,"0")
            print("send off relay 2")
            loading.close()
    #activate relay 3
    def r3ON(self):
        if self.checkDeviceName(self.lineEdit_3.text()) ==False:
            return False
        else:
            loading=Loading()
            loading.show()
            # Set the username and password for the MQTT client
            client.username_pw_set(self.mqtt_username, self.mqtt_password)
            client.connect(self.mqtt_broker_ip, int(self.mqtt_port))
            # client.subscribe(self.lineEdit_3.text()+"/R1")
            topic=self.lineEdit_3.text()+"/R3"
            client.publish(topic,"1")
            print("send on relay 3")
            loading.close()
    #deactivate relay 3
    def r3OFF(self):
        if self.checkDeviceName(self.lineEdit_3.text()) ==False:
            return False
        else:
            loading=Loading()
            loading.show()
            # Set the username and password for the MQTT client
            client.username_pw_set(self.mqtt_username, self.mqtt_password)
            client.connect(self.mqtt_broker_ip, int(self.mqtt_port))
            # client.subscribe(self.lineEdit_3.text()+"/R1")
            topic=self.lineEdit_3.text()+"/R3"
            client.publish(topic,"0")
            print("send off relay 3")
            loading.close()
    def allON(self):
        if self.checkDeviceName(self.lineEdit_3.text()) ==False:
            return False
        else:
            loading=Loading()
            loading.show()
            # Set the username and password for the MQTT client
            client.username_pw_set(self.mqtt_username, self.mqtt_password)
            client.connect(self.mqtt_broker_ip, int(self.mqtt_port))
            # client.subscribe(self.lineEdit_3.text()+"/R1")
            topic=self.lineEdit_3.text()+"/ALL"
            client.publish(topic,"1")
            print("send off relays")
            loading.close()
    def allOFF(self):
        if self.checkDeviceName(self.lineEdit_3.text()) ==False:
            return False
        else:
            loading=Loading()
            loading.show()
            # Set the username and password for the MQTT client
            client.username_pw_set(self.mqtt_username, self.mqtt_password)
            client.connect(self.mqtt_broker_ip, int(self.mqtt_port))
            # client.subscribe(self.lineEdit_3.text()+"/R1")
            topic=self.lineEdit_3.text()+"/ALL"
            client.publish(topic,"0")
            print("send off relays")
            loading.close()
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
            # if tablerow<5:
            #     for row in range(tablerow,self.get_GuiRowCount()): 
            #         for i in range(self.get_columCount()):
            #             self.tableWidget.setItem(tablerow,i,QtWidgets.QTableWidgetItem(""))
            self.CurrentPages+=1
            print("next page",self.CurrentPages,'/',last_page)

    def addTagClicked(self):
        print(self.pushButton_6.text())
        addtagwindow=InsertWindow()
        addtagwindow.show()
        
    def deleteTagClicked(self):
        print(self.pushButton_7.text())
        deletetag=DeleteWindow()
        deletetag.show()
    def editeTagClicked(self):
        print(self.pushButton_8.text())
        self.edit=SearchEditeWindow()
        self.edit.show()
    def searchTagClicked(self):
        print(self.pushButton_9.text())
        self.lineEdit.text()
        qm = QMessageBox
        if searchTag(self.lineEdit.text())[0] ==True:
            tag=searchTag(self.lineEdit.text())
            data=tag[1]
            listdata=data[0]
            print(self.get_GuiRowCount())
            for i in range(self.get_columCount()):
                self.tableWidget.setItem(0,i,QtWidgets.QTableWidgetItem(str(listdata[i])))
            for row in range(1,5):
                for i in range(self.get_columCount()):
                    self.tableWidget.setItem(row,i,QtWidgets.QTableWidgetItem(""))

        else :
            qm.warning(self,'info',"<font size = 8>Tag id "+self.lineEdit.text()+" not exist </font>")
  
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
        if self.checkDeviceName(self.lineEdit_2.text()) ==False:
            return False
        else:
            loading=Loading()
            loading.show()
            # Set the username and password for the MQTT client
            client.username_pw_set(self.mqtt_username, self.mqtt_password)
            client.connect(self.mqtt_broker_ip, int(self.mqtt_port))
            # client.subscribe(self.lineEdit_3.text()+"/R1")
            topic=self.lineEdit_2.text()+"/connection"
            client.publish(topic,"1")
            loading.close()
    def setupClicked(self):
        print(self.pushButton_10.text())

        payload=str(self.spinBox.value())+"#"+str(self.spinBox_2.value())+"#"+str(self.spinBox_5.value())+"#"+str(self.spinBox_6.value())+"#"+str(self.spinBox_3.value())+"#"+str(self.spinBox_4.value())
        print(payload)
        if self.checkDeviceName(self.lineEdit_2.text()) ==False:
            return False
        else:
            # Set the username and password for the MQTT client
            client.username_pw_set(self.mqtt_username, self.mqtt_password)
            client.connect(self.mqtt_broker_ip, int(self.mqtt_port))
            # client.subscribe(self.lineEdit_3.text()+"/R1")
            topic=self.lineEdit_2.text()+"/Relays"
            client.publish(topic,payload)

#insert window class
class InsertWindow(QMainWindow,Ui_insertWindow):
    def __init__(self,parent=None):
        super(InsertWindow,self).__init__(parent)
        self.setupUi(self)
        # self.setWindowFlags(
        # QtCore.Qt.Window |
        # QtCore.Qt.CustomizeWindowHint |
        # QtCore.Qt.WindowTitleHint |
        # QtCore.Qt.WindowCloseButtonHint |
        # QtCore.Qt.WindowStaysOnTopHint|
        # QtCore.Qt.FramelessWindowHint
        # )
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.device=None
        self.tag=None
        self.ReloadTime=None
        self.eatState=None
        self.relayState=1
        self.R1Start=None
        self.R2Start=None
        self.R3Start=None
        self.R1End=None
        self.R2End=None
        self.R3End=None
        self.days=None
        
        self.pushButton.clicked.connect(lambda:self.insertDataButton())
    def insertDataButton(self):
        self.setValue()
        #insertion condutions for all data seted bu the user
        qm = QMessageBox  
        #check if device name have esp in the first three characters
        if  self.device[0:3] !="esp"  or len(self.device)!=5:
            print('bad device')
            qm.warning(self,'Warning',"<font size = 8> Your device name is incorrect </font> ")
            return False
        #check if tag id is already in data
        elif searchTag(str(self.tag))[0]==True:
            print('tag is in our data')
            qm.warning(self,'Warning',"<font size = 8>Tag id "+self.tag+" already exist </font>")
            return False
        #check if tag id is already in data
        elif self.tag=='':
            qm.warning(self,'Warning',"<font size = 8> please input atleast one tag </font>")
            return False
        #check if reload time is seted correctly
        elif self.ReloadTime=='':
            qm.warning(self,'Warning',"<font size = 8> please input the reload time </font>")
            return False
        #check if R1 start time is smaller than R1 END
        # elif self.R1Start>self.R1End:
        #     print('bad timing for R1')
        #     qm.warning(self,'Warning',"<font size = 8>R1 start can't be bigger than R1 end </font>")
        #     return False
        # elif self.R2Start>self.R2End:
        #     print('bad timing for R2')
        #     qm.warning(self,'Warning',"<font size = 8>R2 start can't be bigger than R2 end </font>")
        #     return False
        # elif self.R3Start>self.R3End:
        #     print('bad timing for R3')
        #     qm.warning(self,'Warning',"<font size = 8>R3 start can't be bigger than R3 end </font>")
            
        #     return False
        else: 
            insertdata(self.device,self.tag,datetime.now(),self.ReloadTime,self.relayState,self.eatState,str(self.R1Start)+"#"+str(self.R1End),str(self.R2Start)+"#"+str(self.R2End),str(self.R3Start)+"#"+str(self.R3End),self.days)
            qm.information(self,'Congratulation',"<font size = 8>data inserted successfully</font>")
            self.close()
            # qm.close()
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
#delete window class
class DeleteWindow(QMainWindow,Ui_deleteWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.pushButton.clicked.connect(lambda: self.confirmDelete())
        self.pushButton_2.clicked.connect(lambda: self.cancelDelete())
    def confirmDelete(self):
        qm = QMessageBox
        
        if searchTag(self.lineEdit.text())[0] ==True:
            ret = qm.question(self,'Confirmation', "Are you sure to delete the Tag"+str(self.lineEdit.text()), qm.Yes | qm.No)
            if ret==qm.Yes:
                deleteTag(self.lineEdit.text())
                qm.information(self,'info',"Tag is deleted")
                self.close()
            else:
                qm.warning(self,'info',"<font size = 8>Nothing Change</font>")
                self.close()
        else :
            qm.warning(self,'info',"<font size = 8>Tag id "+self.lineEdit.text()+" not exist </font>")
  
            # qm.information(self,'info',"Nothing Changed")
    def cancelDelete(self):
                self.close()
#search window class
class SearchEditeWindow(QMainWindow,Ui_deleteWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.lineEdit.text()
        self.pushButton.clicked.connect(lambda: self.confirm())
        self.pushButton_2.clicked.connect(lambda: self.cancel())
    def confirm(self):
        self.texttag=self.lineEdit.text()
        state=(searchTag(self.texttag))[0]
        qm = QMessageBox
        if  state is True:
                data=(searchTag(self.texttag))[1]
                data=data[0]
                qm.information(self,'info',"Tag is found it")
                self.close()
                win=EditWindow()
                win.tag=self.lineEdit.text()
                win.showData(self.lineEdit.text())
                win.show()
                # self.close()
        else:
            qm.information(self,'info',"No Tag named "+self.texttag+" registred")
            data=(searchTag(self.texttag))[1]
    def cancel(self):
                self.close()
#edite window class 
class EditWindow(QMainWindow,Ui_insertWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self) 
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.device=None
        self.tag=None
        self.saveTime=None
        self.ReloadTime=None
        self.eatState=None
        self.relayState=None
        self.R1Start=None
        self.R2Start=None
        self.R3Start=None
        self.R1End=None
        self.R2End=None
        self.R3End=None
        self.days=None
        self.pushButton.clicked.connect(lambda:self.update())
    def showData(self,tagid):
        self.tag=tagid
        self.dic=getData("EspData",self.tag)
        # sqlitequery="SELECT * FROM EspData WHERE tag =?"
        # cursor.execute(sqlitequery,(str(self.tag),))
        # data=cursor.fetchall()[0]
        # self.device=data[1]
        # self.tag=data[2]
        # self.saveTime=data[3]
        # self.ReloadTime=data[4]
        # self.eatState=data[5]
        # self.relayState=data[6]
        # self.R1Start=data[7].split("#")[0]
        # self.R2Start=data[8].split("#")[0]
        # self.R3Start=data[9].split("#")[0]
        # self.R1End=data[7].split("#")[1]
        # self.R2End=data[8].split("#")[1]
        # self.R3End=data[9].split("#")[1]
        # self.days=data[10]
        self.lineEdit.setText(str(self.dic["device"]))
        self.lineEdit_2.setText(str(self.dic["tag"]))
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_3.setText(str(self.dic["ReloadTime"]))
        #r1 start and end
        self.spinBox.setValue(int(self.dic["R1time"].split("#")[0]))
        self.spinBox_2.setValue(int(self.dic["R1time"].split("#")[1]))
        #r2 start and end
        self.spinBox_3.setValue(int(self.dic["R2time"].split("#")[0]))
        self.spinBox_4.setValue(int(self.dic["R2time"].split("#")[1]))
        #r3 start and end
        self.spinBox_5.setValue(int(self.dic["R3time"].split("#")[0]))
        self.spinBox_6.setValue(int(self.dic["R3time"].split("#")[1]))
        #days
        self.spinBox_7.setValue(int(self.dic["Days"]))
        #ccheckBox
        self.x=True if self.dic["EatState"]=="1" else False
        print(self.x)
        self.checkBox.setChecked(self.x)
    def setData(self):
        self.device=self.lineEdit.text()
        self.tag=self.lineEdit_2.text()
        self.relayState="0"
        self.ReloadTime=self.lineEdit_3.text()
        if self.checkBox.isChecked():
            self.eatState="1"
        else:
            self.eatState="0"
        self.R1Start=self.spinBox.value()
        self.R2Start=self.spinBox_3.value()
        self.R3Start=self.spinBox_5.value()
        self.R1End=self.spinBox_2.value()
        self.R2End=self.spinBox_4.value()
        self.R3End=self.spinBox_6.value()
        self.days=self.spinBox_7.value()
    def update(self):
        self.setData()
        if updatedata(self.device,self.tag,datetime.now(),self.ReloadTime,self.relayState,self.eatState,str(self.R1Start)+"#"+str(self.R1End),str(self.R2Start)+"#"+str(self.R2End),str(self.R3Start)+"#"+str(self.R3End),self.days) is True:
            QMessageBox.information(self,'congratulation',"<font size = 8>Data inserted succussfuly</font>")
            self.close()
        else:
            QMessageBox.information(self,'bad setup',"<font size = 8>Bad data insertion</font>")
    def insertDataButton(self):
            self.close()
# setting dialog class
class SettingDialog(QDialog,Ui_Dialog):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.pushButton.clicked.connect(lambda : self.setSetting())
        self.lineEdit.setText(getSetting("setting")["mqtt_username"])
        self.lineEdit_2.setText(getSetting("setting")["mqtt_port"])
        self.lineEdit_3.setText(getSetting("setting")["mqtt_password"])
        self.lineEdit_5.setText(getSetting("setting")["mqtt_topic"])
        self.lineEdit_7.setText(getSetting("setting")["mqtt_broker_ip"])
        # Relay 1 timer
        self.spinBox_2.setValue(int((getSetting("setting")["R1time"]).split("#")[0]))
        self.spinBox_3.setValue(int((getSetting("setting")["R1time"]).split("#")[1]))
        # Relay 2 timer
        self.spinBox_4.setValue(int((getSetting("setting")["R2time"]).split("#")[0]))
        self.spinBox_5.setValue(int((getSetting("setting")["R2time"]).split("#")[1]))
        # Relay 3 timer
        self.spinBox_6.setValue(int((getSetting("setting")["R3time"]).split("#")[0]))
        self.spinBox_12.setValue(int((getSetting("setting")["R3time"]).split("#")[1]))
    def setSetting(self):
        updateSetting("mqtt_username",self.lineEdit.text())
        updateSetting("mqtt_password",self.lineEdit_3.text())
        updateSetting("mqtt_topic",self.lineEdit_5.text())
        updateSetting("mqtt_broker_ip", self.lineEdit_7.text())
        updateSetting("mqtt_port",self.lineEdit_2.text())
        updateSetting("R1time",str(self.spinBox_2.value())+"#"+str(self.spinBox_3.value()))
        updateSetting("R2time",str(self.spinBox_4.value())+"#"+str(self.spinBox_5.value()))
        updateSetting("R3time",str(self.spinBox_6.value())+"#"+str(self.spinBox_12.value()))
class Loading(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowFlags(
        QtCore.Qt.WindowStaysOnTopHint| QtCore.Qt.CustomizeWindowHint
        )
        self.setObjectName( "FTwindow" ) 
        self.setFixedSize( 200, 200) 
        self.centralwidget = QWidget(self) 
        self.centralwidget.setObjectName( "main-widget" ) 
        # Label Create 
        self.label = QLabel( self.centralwidget) 
        self.label.setObjectName( "lb1" ) 

        self.setCentralWidget( self.centralwidget) 
        # Loading the GIF 
        self.movie = QMovie( "UI\\../resources/icons/Loading2.gif" ) 
        self.label.setMovie( self.movie) 
        self.startAnimation() 
        
        # Start Animation 
    def startAnimation( self ): 
        self.movie.start() 
    # Stop Animation(According to need) 
    def stopAnimation( self ): 
        self.movie.stop() 
class ThreadClass(QtCore.QThread):
    any_signal = QtCore.pyqtSignal(int)
    def __init__(self,index,mqtt_username,mqtt_password,mqtt_topic,mqtt_broker_ip,mqtt_port):
        super().__init__()
        self.index=index
        self.is_running = True
        self.mq=mqtt_esp(mqtt_username,mqtt_password,mqtt_topic,mqtt_broker_ip,int(mqtt_port))
    def run(self):
        print('Starting thread...',self.index)
        #my code
        self.any_signal.emit(1)
        self.mq.instance()
        self.mq.run_mqtt()


    def stop(self):
        self.is_running = False
        print('Stopping thread...',self.index)
        self.mq.mqstop()
        self.any_signal.emit(0)
        self.terminate()
        
