# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\UI\deleteWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_deleteWindow(object):
    def setupUi(self, deleteWindow):
        deleteWindow.setObjectName("deleteWindow")
        deleteWindow.resize(371, 133)
        self.centralwidget = QtWidgets.QWidget(deleteWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setInputMask("")
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        deleteWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(deleteWindow)
        self.statusbar.setObjectName("statusbar")
        deleteWindow.setStatusBar(self.statusbar)

        self.retranslateUi(deleteWindow)
        QtCore.QMetaObject.connectSlotsByName(deleteWindow)

    def retranslateUi(self, deleteWindow):
        _translate = QtCore.QCoreApplication.translate
        deleteWindow.setWindowTitle(_translate("deleteWindow", "Perform window"))
        self.lineEdit.setPlaceholderText(_translate("deleteWindow", "Tag ID "))
        self.pushButton.setText(_translate("deleteWindow", "Perform"))
        self.pushButton.setShortcut(_translate("deleteWindow", "Return"))
        self.pushButton_2.setText(_translate("deleteWindow", "Cancel"))
