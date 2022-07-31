from classes.window import *
if __name__ =="__main__":
    app=QApplication(sys.argv)
    win=main_window()
    win.show()
    sys.exit(app.exec())