from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.pushButton1 = QPushButton("Button 1", self.centralwidget)
        self.pushButton1.setGeometry(50,80,100,50)
        self.pushButton2 = QPushButton("Button 2", self.centralwidget)
        self.pushButton2.setGeometry(150,80,100,50)
        self.pushButton3 = QPushButton("Button 3", self.centralwidget)
        self.pushButton3.setGeometry(250,80,100,50)

        lay = QHBoxLayout(self.centralwidget)
        lay.addWidget(self.pushButton1)
        lay.addWidget(self.pushButton2)
        lay.addWidget(self.pushButton3)

stylesheet = """
    MainWindow {
        background-image: url("jake.png"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
"""


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)     # <---
    window = MainWindow()
    window.resize(640, 640)
    window.show()
    sys.exit(app.exec_())