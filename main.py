# basic_window.py
# Import necessary modules
import sys
from PyQt5.QtWidgets import QApplication, QWidget,QLabel,QPushButton,QLineEdit
from PyQt5 import QtGui,QtCore,Qt
from PyQt5.QtGui import QFont
class EmptyWindow(QWidget):
    def __init__(self):
        super().__init__() # create default constructor for QWidget
        self.initializeUI("img/dkhan.jpg")
    def initializeUI(self,image):
        self.setGeometry(100, 100, 1080, 900)
        self.setWindowTitle("Bitzer")
        self.image0 = QtGui.QImage(image)
        self.redimage(self.width(), self.height())
        self.displayButton()
        self.text_field_1(300,80)
        self.text_field_2(300,180)
        self.text_field_3(300,280)
        self.text_field_4(320,450)
        self.show()
    def redimage(self, width=None, height=None):
        """redimensionne l'image selon les arguments donnés à l'appel
        """
        if width!=None and height==None:
            # on redimensionne selon la largeur mais on garde le ratio de l'image
            image = self.image0.scaledToWidth(width, QtCore.Qt.SmoothTransformation)
        elif width==None and height!=None:
            # on redimensionne selon la hauteur mais on garde le ratio de l'image
            image = self.image0.scaledToHeight(height, QtCore.Qt.SmoothTransformation)
        elif width!=None and height!=None:
            # on redimensionne selon la largeur et la hauteur, mais le ratio de l'image change
            image = self.image0.scaled(width, height, QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.SmoothTransformation)
        else:
            image = self.image0  # ici, on ne fait aucun redimensionnement
        palette = QtGui.QPalette()
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(image))
        self.setPalette(palette)
    @QtCore.pyqtSlot("QResizeEvent")
    def resizeEvent(self, event=None):
        """ Méthode exécutée à chaque redimensionnement """
        # redimensionne l'image de fond à la nouvelle taille
        self.redimage(event.size().width(), event.size().height())
    def displayButton(self):
        """detup the button widget """
        #####labele one 
        name_label=QLabel(self)
        name_label.setText("Set time for Relay 1")
        name_label.setFont(QFont('Arial',10,80,True))
        name_label.move(60,40)
        name_label.setStyleSheet('color:white')
        button=QPushButton("Relay 1", self)
        # button.setStyleSheet(
        #     "QPushButton" 
        # "{"
        #     "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 190, 11, 255), stop:1 rgba(251, 86, 7, 255));"
        #     "border-radius: 20px;"
        # "}"
        #     )
        #button.move(60,80) #arrange button
        button.setGeometry(60,80,200,50)
        button.clicked.connect(self.buttonClicked)
        #####labele 2
        name_label=QLabel(self)
        name_label.setText("Set time for Relay 2")
        name_label.setFont(QFont('Arial',10,80,True))
        name_label.move(60,140)
        name_label.setStyleSheet('color:white')
        button=QPushButton("Relay 2", self)
        # button.setStyleSheet(
        #     "QPushButton" 
        # "{"
        #     "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 190, 11, 255), stop:1 rgba(251, 86, 7, 255));"
        #     "border-radius: 20px;"
        # "}"
        #     )
        #button.move(60,80) #arrange button
        button.setGeometry(60,180,200,50)
        button.clicked.connect(self.buttonClicked)
        #####labele 3 
        name_label=QLabel(self)
        name_label.setText("Set time for Relay 3")
        name_label.setFont(QFont('Arial',10,80,True))
        name_label.move(60,240)
        name_label.setStyleSheet('color:white')
        button=QPushButton("Relay 3", self)
        # button.setStyleSheet(
        #     "QPushButton" 
        # "{"
        #     "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 190, 11, 255), stop:1 rgba(251, 86, 7, 255));"
        #     "border-radius: 20px;"
        # "}"
        #     )
        #button.move(60,80) #arrange button
        button.setGeometry(60,280,200,50)
        button.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        '''print message to the terminal and close all windows'''
        self.close()
    def text_field_1(self,xposition,yposition):
        """setup the Qline edit and the other widgets"""
        #create name labels
        #label for seting the start time
        start_label=QLabel("Start time :",self)
        start_label.setFont(QFont('Arial',10,80,True))
        start_label.move(xposition,yposition-40)
        start_label.setStyleSheet('color:white')
        #label for seting the end time
        end_label=QLabel("End time :",self)
        end_label.setFont(QFont('Arial',10,80,True))
        end_label.move(xposition+200,yposition-40)
        end_label.setStyleSheet('color:white')
        #create line text edit 
        self.start_entry_1=QLineEdit(self)
        self.start_entry_1.setGeometry(xposition,yposition,100,50)
        self.end_entry_1=QLineEdit(self)
        self.end_entry_1.setGeometry(xposition+200,yposition,100,50)

        self.clear_button=QPushButton('clear',self)
        self.clear_button.setGeometry(xposition+330,yposition,150,50)
        self.clear_button.clicked.connect(self.claerEntries_1)
        
    def text_field_2(self,xposition,yposition):
        """setup the Qline edit and the other widgets"""
        #create name labels
        #label for seting the start time
        start_label=QLabel("Start time :",self)
        start_label.setFont(QFont('Arial',10,80,True))
        start_label.move(xposition,yposition-40)
        start_label.setStyleSheet('color:white')
        #label for seting the end time
        end_label=QLabel("End time :",self)
        end_label.setFont(QFont('Arial',10,80,True))
        end_label.move(xposition+200,yposition-40)
        end_label.setStyleSheet('color:white')
        #create line text edit 
        self.start_entry_2=QLineEdit(self)
        self.start_entry_2.setGeometry(xposition,yposition,100,50)
        self.end_entry_2=QLineEdit(self)
        self.end_entry_2.setGeometry(xposition+200,yposition,100,50)

        self.clear_button=QPushButton('clear',self)
        self.clear_button.setGeometry(xposition+330,yposition,150,50)
        self.clear_button.clicked.connect(self.claerEntries_2)
        
    def text_field_3(self,xposition,yposition):
        """setup the Qline edit and the other widgets"""
        #create name labels
        #label for seting the start time
        start_label=QLabel("Start time :",self)
        start_label.setFont(QFont('Arial',10,80,True))
        start_label.move(xposition,yposition-40)
        start_label.setStyleSheet('color:white')
        #label for seting the end time
        end_label=QLabel("End time :",self)
        end_label.setFont(QFont('Arial',10,80,True))
        end_label.move(xposition+200,yposition-40)
        end_label.setStyleSheet('color:white')
        #create line text edit 
        self.start_entry_3=QLineEdit(self)
        self.start_entry_3.setGeometry(xposition,yposition,100,50)
        self.end_entry_3=QLineEdit(self)
        self.end_entry_3.setGeometry(xposition+200,yposition,100,50)

        self.clear_button=QPushButton('clear',self)
        self.clear_button.setGeometry(xposition+330,yposition,150,50)
        self.clear_button.clicked.connect(self.claerEntries_3)
        
    def text_field_4(self,xposition,yposition):
        """setup the Qline edit and the other widgets"""
        #create name labels
        #label for seting the start time
        mqtt_label=QLabel("espxx/ :",self)
        mqtt_label.setFont(QFont('Arial',10,80,True))
        mqtt_label.move(xposition,yposition-40)
        mqtt_label.setStyleSheet('color:white')
        #create line text edit 
        self.mqtt_entry_4=QLineEdit(self)
        self.mqtt_entry_4.setGeometry(xposition,yposition,100,50)

        self.mqtt_connect_button=QPushButton('mqtt_connect',self)
        self.mqtt_connect_button.setGeometry(xposition+330,yposition,180,50)
        self.mqtt_connect_button.setFont(QFont('Arial',10,80,True))
        self.mqtt_connect_button.clicked.connect(self.claerEntries_4)
        # self.mqtt_connect_button.setStyleSheet(
        #     "QPushButton" 
        # "{"
        #     "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(23, 174, 109, 0.89), stop:1 rgba(23, 174, 109, 0.89));"
        #     "border-radius: 20px;"
        # "}"
        #     )
    
    def claerEntries_1(self):
        sender=self.sender()
        if sender.text()=='clear':
            self.end_entry_1.clear()
            self.start_entry_1.clear()
    def claerEntries_2(self):
        sender=self.sender()
        if sender.text()=='clear':
            self.end_entry_2.clear()
            self.start_entry_2.clear()
    def claerEntries_3(self):
        sender=self.sender()
        if sender.text()=='clear':
            self.end_entry_3.clear()
            self.start_entry_3.clear()
    def claerEntries_4(self):
        sender=self.sender()
        if sender.text()=='mqtt_connect':
            self.mqtt_entry_4.clear()

# Run program
stylesheet =""""
color: white;
	background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(255, 190, 11, 255), stop:1 rgba(251, 86, 7, 255));
	border-radius: 20px;
}
"""
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmptyWindow()
    sys.exit(app.exec_())