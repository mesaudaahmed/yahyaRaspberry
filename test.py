# Welcome to PyShine
# This is part 12 of the PyQt5 learning series
# Start and Stop Qthreads
# Source code available: www.pyshine.com
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5 import uic
import sys, time

class PyShine_THREADS_APP(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.resize(888, 200)
		self.thread={}
		self.start_worker_1()
		time.sleep(3)
		self.stop_worker_1()
	def start_worker_1(self):
		self.thread[1] = ThreadClass(index=1)
		self.thread[1].start()
		self.thread[1].any_signal.connect(self.my_function)

		
	def stop_worker_1(self):
		self.thread[1].stop()
		del self.thread[1]
	def my_function(self,counter):
		cnt=counter
		index = self.sender().index
		if index==1:
			print(cnt) 

class ThreadClass(QtCore.QThread):
	
	any_signal = QtCore.pyqtSignal(int)
	def __init__(self,index):
		super().__init__()
		self.index=index
		self.is_running = True
		print(self.index)
	def run(self):
		print('Starting thread...',self.index)
		cnt=0
		while (True):
			cnt+=1
			if cnt==99: cnt=0
			time.sleep(0.01)
			self.any_signal.emit(cnt) 
	def stop(self):
		self.is_running = False
		print('Stopping thread...',self.index)
		self.terminate()



app = QtWidgets.QApplication(sys.argv)
mainWindow = PyShine_THREADS_APP()
mainWindow.show()
sys.exit(app.exec_())