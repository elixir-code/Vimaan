# import libraries necessary for GUI creation
from PyQt5.QtWidgets import QApplication, QDialog, QTableView, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
import sys

class DataViewerDialog(QDialog):
	
	def __init__(self, *args, **kargs):
		
		super().__init__(*args, **kargs)
		self.setWindowModality(Qt.WindowModal)
		
		self.initUI()

	# customise the QDialog UI
	def initUI(self):

		self.data_table = QTableView()

		# create and display status and close button pane
		status_close_pane = QHBoxLayout()

		self.status_label = QLabel()
		close_btn = QPushButton('Close')
		close_btn.pressed.connect(self.close)

		status_close_pane.addWidget(self.status_label)
		status_close_pane.addStretch(100)
		status_close_pane.addWidget(close_btn)
		status_close_pane.addStretch(1)

		# create and display 'data viewer' layout
		data_viewer_pane = QVBoxLayout()
		data_viewer_pane.addWidget(self.data_table)
		data_viewer_pane.addLayout(status_close_pane)

		self.setLayout(data_viewer_pane)

	# show preparing data wait status message
	def showPreparingDataStatus(self):

		self.status_label.setText('Preparing Data. Please wait ...')
		self.status_label.setStyleSheet("color: brown; font: bold;")

	# set data in the data viewer dialog
	def setDataModel(self, data_model):

		self.data_table.setModel(data_model)

		self.status_label.setText('Showing <b>{}</b> Records'.format(data_model.rowCount()))
		self.status_label.setStyleSheet("")

# Test the 'Data Viewer' dialog
if __name__ == '__main__':

	# create and the display the application's "Data Viewer" dialog
	application = QApplication(sys.argv)

	window = DataViewerDialog()
	window.show()

	sys.exit(application.exec_())