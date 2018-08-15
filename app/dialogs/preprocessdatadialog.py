# import necessary libraries for gui creation
from PyQt5.QtWidgets import QApplication, QDialog, QGroupBox, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCheckBox
from PyQt5.QtCore import Qt
import sys

# import data processing libraries
import pandas as pd

# import gui dialogs
from dialogs.dataviewerdialog import DataViewerDialog 

# import necessary models
from models.dataframemodel import DataFrameModel

missing_data_note = """Note: Records with missing city, state or country names have been implicitly removed."""

class MissingDataNoteLabel(QLabel):

	def __init__(self, *args, **kargs):
		super().__init__(*args, **kargs)
		self.setStyleSheet("color: brown; font: bold;")
		self.setWordWrap(True)

	def minimumSizeHint(self):
		return self.sizeHint()

class PreprocessDataDialog(QDialog):

	def __init__(self, *args, **kargs):

		self.data = kargs.pop('data', None)

		if self.data is None:
			self.data = pd.DataFrame()

		# consider a subset of fields for preprocessing
		self.fields = kargs.pop('fields', None)
		
		if self.fields is not None:

			invalid_fields = [field for field in self.fields if field not in self.data]
			if invalid_fields:
				print("ERROR: Invalid field(s) '{}' specified for data".format(*invalid_fields))
				sys.exit(1)

		# initialise the QDialog
		super().__init__(*args, **kargs)
		self.setWindowModality(Qt.WindowModal)

		# customise the QDialog UI
		self.initUI()

	def initUI(self):

		# create and diplay missing data records group box
		missing_data_pane = QGroupBox('Missing Data Records')
		missing_data_box = QVBoxLayout()

		missing_data_label = MissingDataNoteLabel(missing_data_note)

		missing_data_view_box = QHBoxLayout()
		missing_data_view_btn = QPushButton('View Records')
		missing_data_view_btn.pressed.connect(self.viewMissingDataRecords)

		missing_data_view_box.addStretch(50)
		missing_data_view_box.addWidget(missing_data_view_btn)
		missing_data_view_box.addStretch(1)

		missing_data_box.addStretch(1)
		missing_data_box.addWidget(missing_data_label)
		missing_data_box.addStretch(1)
		missing_data_box.addLayout(missing_data_view_box)
		missing_data_box.addStretch(1)

		missing_data_pane.setLayout(missing_data_box)

		# create and display duplicate records group box
		duplicate_records_pane = QGroupBox('Duplicate Records')
		duplicate_records_box = QVBoxLayout()

		duplicate_records_checkbox = QCheckBox('Remove records with duplicate city, state and country names.')

		duplicate_data_view_box = QHBoxLayout()
		duplicate_data_view_btn = QPushButton('View Records')
		duplicate_data_view_btn.pressed.connect(self.viewDuplicateRecords)

		duplicate_data_view_box.addStretch(50)
		duplicate_data_view_box.addWidget(duplicate_data_view_btn)
		duplicate_data_view_box.addStretch(1)

		duplicate_records_box.addStretch(1)
		duplicate_records_box.addWidget(duplicate_records_checkbox)
		duplicate_records_box.addStretch(1)
		duplicate_records_box.addLayout(duplicate_data_view_box)
		duplicate_records_box.addStretch(1)

		duplicate_records_pane.setLayout(duplicate_records_box)

		# create and display the finish button pane
		finish_button_pane = QHBoxLayout()

		finish_button = QPushButton('Finish')

		finish_button_pane.addStretch(100)
		finish_button_pane.addWidget(finish_button)
		finish_button_pane.addStretch(1)

		# create and display 'preprocess dialog' layout
		preprocess_data_pane = QVBoxLayout()

		preprocess_data_pane.addStretch(1)
		preprocess_data_pane.addWidget(missing_data_pane)
		preprocess_data_pane.addStretch(1)
		preprocess_data_pane.addWidget(duplicate_records_pane)
		preprocess_data_pane.addSpacing(20)
		preprocess_data_pane.addStretch(1)
		preprocess_data_pane.addLayout(finish_button_pane)
		preprocess_data_pane.addStretch(1)

		self.setLayout(preprocess_data_pane)

		# set the attributes of the 'preprocess data' dialog
		self.setWindowTitle('Preprocess Data')

	# view missing data records
	def viewMissingDataRecords(self):
		
		missing_data_viewer_dialog = DataViewerDialog(parent=self)
		missing_data_viewer_dialog.setWindowTitle('Missing Data Records')
		missing_data_viewer_dialog.showPreparingDataStatus()
		missing_data_viewer_dialog.show()

		# extract records with missing fields
		missing_data_records = self.data[self.fields][self.data[self.fields].isna().any(axis=1)]
		missing_data_model = DataFrameModel(missing_data_records)
		missing_data_viewer_dialog.setDataModel(missing_data_model)
		missing_data_viewer_dialog.resize(self.sizeHint())

	# view duplicate data records
	def viewDuplicateRecords(self):
		
		duplicate_data_viewer_dialog = DataViewerDialog(parent=self)
		duplicate_data_viewer_dialog.setWindowTitle('Duplicate Data Records')
		duplicate_data_viewer_dialog.showPreparingDataStatus()
		duplicate_data_viewer_dialog.show()

# Test the 'Preprocess Data' dialog
if __name__ == '__main__':

	# create and the display the application's "Preprocess Data" dialog
	application = QApplication(sys.argv)

	window = PreprocessDataDialog()
	window.show()

	sys.exit(application.exec_())