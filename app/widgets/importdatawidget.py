""" 'Import Data' screen """

# import neccessary libraries for gui creation
from PyQt5.QtWidgets import QApplication, QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QFileDialog, QGroupBox, QComboBox, QMessageBox
from PyQt5.QtGui import QFont, QPainter, QFontMetrics, QStandardItemModel, QStandardItem
from PyQt5.QtCore import QSize, Qt
import sys

# import libraries importing and manipulating data
import pandas as pd
from xlrd.biffh import XLRDError

# A custom 'resizable label' class (that trucates text with elipsis ...)
class ResizeableLabel(QLabel):

	# reimplement constructor (implement constructor of super-class)
	def __init__(self, *args, **kargs):
		super().__init__(*args, **kargs)
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		# self.setMaximumWidth(700)

	# set default size of label at start
	def sizeHint(self):
		return QSize(285, QLabel().sizeHint().height())

	# set minimum size hint to allow horizontal resizability
	def minimumSizeHint(self):
		return QSize(0, QLabel().minimumSizeHint().height())

	# callback for paint event
	def paintEvent(self, event):
		painter = QPainter(self)

		metrics = QFontMetrics(self.font())
		elided  = metrics.elidedText(self.text(), Qt.ElideRight, self.width())

		painter.drawText(self.rect(), self.alignment(), elided)

	def setText(self, text):
		super().setText(text)
		self.setToolTip(text)

# A custom combobox to display column names
class DataColumnsComboBox(QComboBox):

	# reimplement constructor (implement constructor of super-class)
	def __init__(self, parent=None):
		super().__init__(parent)

	def sizeHint(self):
		return QSize(150, QComboBox().sizeHint().height())


# Import data widget class
class ImportDataWidget(QWidget):

	def __init__(self):

		# initialise the QWidget
		super().__init__()

		self.initUI()

	def initUI(self):

		# create and display widgets to 'choose input file'
		input_file_pane = QHBoxLayout()

		input_file_choose_label = QLabel('Choose your input file (.xlsx, .xls)')
		input_file_label_font  = QFont("Verdana, Helvetica", 10, QFont.Bold)
		input_file_choose_label.setFont(input_file_label_font)

		self.input_filename_label = ResizeableLabel('')
		self.input_filename_label.setStyleSheet("border: 1px inset grey;")

		input_file_choose_btn = QPushButton('Choose')
		input_file_choose_btn.pressed.connect(self.chooseInputFile)

		input_file_pane.addWidget(input_file_choose_label)
		input_file_pane.addWidget(self.input_filename_label)
		input_file_pane.addWidget(input_file_choose_btn)

		# create and display input column's group box
		map_input_columns_pane = QGroupBox('Input Columns')

		# create and display input column's mapping group box
		map_input_columns_box = QGridLayout()

		map_cityname_col_label = QLabel('City Name')
		map_statename_col_label = QLabel('State Name')
		map_countryname_col_label = QLabel('Country Name')

		map_cityname_col_combobox = DataColumnsComboBox()
		map_statename_col_combobox = DataColumnsComboBox()
		map_countryname_col_combobox = DataColumnsComboBox()

		map_input_columns_box.addWidget(map_cityname_col_label, 0, 0)
		map_input_columns_box.addWidget(map_cityname_col_combobox, 0, 1)
		map_input_columns_box.addWidget(map_statename_col_label, 1, 0)
		map_input_columns_box.addWidget(map_statename_col_combobox, 1, 1)
		map_input_columns_box.addWidget(map_countryname_col_label, 2, 0)
		map_input_columns_box.addWidget(map_countryname_col_combobox, 2, 1)

		map_input_columns_pane.setLayout(map_input_columns_box)
		# map_input_columns_pane.hide()

		# create and display output column's mapping group box
		map_output_columns_pane = QGroupBox('Output Columns')

		# create and display input column's mapping group box
		map_output_columns_box = QHBoxLayout()

		map_iata_col_label = QLabel('Nearest Airport IATA')
		map_iata_col_combobox = DataColumnsComboBox()

		map_output_columns_box.addWidget(map_iata_col_label)
		map_output_columns_box.addWidget(map_iata_col_combobox)

		map_output_columns_pane.setLayout(map_output_columns_box)
		# map_output_columns_pane.hide()

		# create and display input column's mapping outer pane
		map_input_columns_outer_pane = QVBoxLayout()

		map_input_columns_outer_pane.addStretch(1)
		map_input_columns_outer_pane.addWidget(map_input_columns_pane)
		map_input_columns_outer_pane.addStretch(1)

		# create and display output column's mapping outer pane
		map_output_columns_outer_pane = QVBoxLayout()

		map_output_columns_outer_pane.addStretch(1)
		map_output_columns_outer_pane.addWidget(map_output_columns_pane)
		map_output_columns_outer_pane.addStretch(1)

		# create and display columns mapping pane
		map_columns_pane = QHBoxLayout()
		map_columns_pane.addStretch(1)
		map_columns_pane.addLayout(map_input_columns_outer_pane)
		map_columns_pane.addStretch(1)
		map_columns_pane.addLayout(map_output_columns_outer_pane)
		map_columns_pane.addStretch(1)

		# Create the next button box
		finish_button_pane = QHBoxLayout()
		finish_button = QPushButton('Finish')

		finish_button_pane.addStretch(30)
		finish_button_pane.addWidget(finish_button)
		finish_button_pane.addStretch(1)

		finish_button.setEnabled(False)
		# Create and display the import data components
		main_pane = QVBoxLayout()

		main_pane.addStretch(1)
		main_pane.addLayout(input_file_pane)
		main_pane.addStretch(1)
		main_pane.addLayout(map_columns_pane)
		main_pane.addStretch(1)
		main_pane.addLayout(finish_button_pane)

		self.setLayout(main_pane)

		# set the attributes of the 'import data' widget
		self.setWindowTitle('Import Data')


	# Choose input file by popping up a OPEN FILE DIALOG
	def chooseInputFile(self):

		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		filename, _ = QFileDialog.getOpenFileName(self,"Choose Input File", "", "Excel Spreadsheet (*.xlsx *.xls);;All Files (*)", options=options)		


# Test the 'First Steps with VIMAAN' widget
if __name__ == '__main__':

	# create and display the application's "First Steps" widget
	application = QApplication(sys.argv)

	window = ImportDataWidget()
	window.show()

	sys.exit(application.exec_())