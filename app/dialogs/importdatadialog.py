""" 'Import Data' screen """

# import neccessary libraries for gui creation
from PyQt5.QtWidgets import QApplication, QDialog, QSizePolicy, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton, QFileDialog, QGroupBox, QComboBox, QMessageBox
from PyQt5.QtGui import QFont, QPainter, QFontMetrics, QStandardItemModel, QStandardItem
from PyQt5.QtCore import QSize, Qt, pyqtSignal
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

# A custom combobox to display field names
class DataFieldsComboBox(QComboBox):

	# reimplement constructor (implement constructor of super-class)
	def __init__(self, parent=None):
		super().__init__(parent)

	def sizeHint(self):
		return QSize(150, QComboBox().sizeHint().height())


# Import data dialog class
class ImportDataDialog(QDialog):

	# define the custom signals for use by controller
	data_import_finish_signal = pyqtSignal(str, str, str, str, str, pd.DataFrame)

	def __init__(self, *args, **kargs):

		# initialise the QDialog
		super().__init__(*args, **kargs)
		self.setWindowModality(Qt.WindowModal)

		# Details of imported input file and fields mapping
		self.filename = None

		self.cityname_field = None
		self.statename_field = None
		self.countryname_field = None

		self.iata_field = None

		# imported data and fields mapping combo boxes model
		self._data = None
		self._data_fields_model = QStandardItemModel()

		# Customise the QDialog UI
		self.initUI()

	def initUI(self):

		# create and display dialog to 'choose input file'
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

		# create and display input field's group box
		map_input_fields_pane = QGroupBox('Input Fields')

		# create and display input field's mapping group box
		map_input_fields_box = QGridLayout()

		map_cityname_field_label = QLabel('City Name')
		map_statename_field_label = QLabel('State Name')
		map_countryname_field_label = QLabel('Country Name')

		map_cityname_field_combobox = DataFieldsComboBox()
		map_statename_field_combobox = DataFieldsComboBox()
		map_countryname_field_combobox = DataFieldsComboBox()

		# set Models for the fields mapping combobox
		map_cityname_field_combobox.setModel(self._data_fields_model)
		map_statename_field_combobox.setModel(self._data_fields_model)
		map_countryname_field_combobox.setModel(self._data_fields_model)

		map_cityname_field_combobox.currentIndexChanged.connect(self.citynameFieldChanged)
		map_statename_field_combobox.currentIndexChanged.connect(self.statenameFieldChanged)
		map_countryname_field_combobox.currentIndexChanged.connect(self.countrynameFieldChanged)		

		map_input_fields_box.addWidget(map_cityname_field_label, 0, 0)
		map_input_fields_box.addWidget(map_cityname_field_combobox, 0, 1)
		map_input_fields_box.addWidget(map_statename_field_label, 1, 0)
		map_input_fields_box.addWidget(map_statename_field_combobox, 1, 1)
		map_input_fields_box.addWidget(map_countryname_field_label, 2, 0)
		map_input_fields_box.addWidget(map_countryname_field_combobox, 2, 1)

		map_input_fields_pane.setLayout(map_input_fields_box)
		# map_input_fields_pane.hide()

		# create and display output field's mapping group box
		map_output_fields_pane = QGroupBox('Output Fields')

		# create and display input field's mapping group box
		map_output_fields_box = QHBoxLayout()

		map_iata_field_label = QLabel('Nearest Airport IATA')
		map_iata_field_combobox = DataFieldsComboBox()

		map_iata_field_combobox.setModel(self._data_fields_model)

		map_iata_field_combobox.currentIndexChanged.connect(self.iataFieldChanged)

		map_output_fields_box.addWidget(map_iata_field_label)
		map_output_fields_box.addWidget(map_iata_field_combobox)

		map_output_fields_pane.setLayout(map_output_fields_box)
		# map_output_fields_pane.hide()

		# create and display input field's mapping outer pane
		map_input_fields_outer_pane = QVBoxLayout()

		map_input_fields_outer_pane.addStretch(1)
		map_input_fields_outer_pane.addWidget(map_input_fields_pane)
		map_input_fields_outer_pane.addStretch(1)

		# create and display output field's mapping outer pane
		map_output_fields_outer_pane = QVBoxLayout()

		map_output_fields_outer_pane.addStretch(1)
		map_output_fields_outer_pane.addWidget(map_output_fields_pane)
		map_output_fields_outer_pane.addStretch(1)

		# create and display fields mapping pane
		map_fields_pane = QHBoxLayout()
		map_fields_pane.addStretch(1)
		map_fields_pane.addLayout(map_input_fields_outer_pane)
		map_fields_pane.addStretch(1)
		map_fields_pane.addLayout(map_output_fields_outer_pane)
		map_fields_pane.addStretch(1)

		# Create the finish button box
		finish_button_pane = QHBoxLayout()
		
		self.wait_message_label = QLabel('Reading data from file. Please wait ...')
		self.wait_message_label.setStyleSheet("color: brown; font: bold;")

		self.finish_button = QPushButton('Finish')
		self.finish_button.pressed.connect(self.finishPressed)

		finish_button_pane.addWidget(self.wait_message_label)
		finish_button_pane.addStretch(100)
		finish_button_pane.addWidget(self.finish_button)
		finish_button_pane.addStretch(1)

		self.wait_message_label.hide()
		self.finish_button.setEnabled(False)

		# Create and display the import data components
		main_pane = QVBoxLayout()

		main_pane.addStretch(1)
		main_pane.addLayout(input_file_pane)
		main_pane.addStretch(1)
		main_pane.addLayout(map_fields_pane)
		main_pane.addStretch(1)
		main_pane.addLayout(finish_button_pane)

		self.setLayout(main_pane)

		# set the attributes of the 'import data' dialog
		self.setWindowTitle('Import Data')


	# Choose input file by popping up a OPEN FILE DIALOG
	def chooseInputFile(self):

		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		filename, _ = QFileDialog.getOpenFileName(self,"Choose Input File", "", "Excel Spreadsheet (*.xlsx *.xls);;All Files (*)", options=options)

		if filename:

			# Clear the input filename attribute
			self.filename = None
			self.input_filename_label.setText(self.filename)

			# clear the fiels mappings
			self.cityname_field = None
			self.statename_field = None
			self.countryname_field = None
			self.iata_field = None
			self._data_fields_model.clear()

			self.wait_message_label.show()
			self.repaint()


			try:
				self._data = pd.read_excel(filename)
				self._data.index += 2

			except XLRDError as error:
				error_message_dialog = QMessageBox(QMessageBox.Critical, " ", "<b>File Type Not Supported:</b> {}".format(error), buttons = QMessageBox.Ok, parent = self)
				error_message_dialog.show()

			except Exception as error:
				error_message_dialog = QMessageBox(QMessageBox.Critical, " ", "<b>Encountered an error in opening and parsing file.</b> {}".format(error), buttons = QMessageBox.Ok, parent = self)
				error_message_dialog.show()

			else:

				self.filename = filename
				self.input_filename_label.setText(self.filename)
				
				combobox_placeholder_item = QStandardItem('Please select ...')
				combobox_placeholder_item.setEnabled(False)

				self._data_fields_model.appendRow(combobox_placeholder_item)

				for field in self._data.columns:
					item = QStandardItem(field)
					self._data_fields_model.appendRow(item)

			self.wait_message_label.hide()

	# slot to handle change of cityname field mapping
	def citynameFieldChanged(self, current_index):
		
		if current_index <= 0:
			self.cityname_field = None
		else:
			self.cityname_field = self._data_fields_model.item(current_index).text()
		
		if self.cityname_field and self.statename_field and self.countryname_field and self.iata_field:
			self.finish_button.setEnabled(True)
		else:
			self.finish_button.setEnabled(False)

	# slot to handle change of statname field mapping
	def statenameFieldChanged(self, current_index):
		
		if current_index <= 0:
			self.statename_field = None
		else:
			self.statename_field = self._data_fields_model.item(current_index).text()

		if self.cityname_field and self.statename_field and self.countryname_field and self.iata_field:
			self.finish_button.setEnabled(True)
		else:
			self.finish_button.setEnabled(False)

	# slot to handle change of countryname field mapping
	def countrynameFieldChanged(self, current_index):
		
		if current_index <= 0:
			self.countryname_field = None
		else:
			self.countryname_field = self._data_fields_model.item(current_index).text()

		if self.cityname_field and self.statename_field and self.countryname_field and self.iata_field:
			self.finish_button.setEnabled(True)
		else:
			self.finish_button.setEnabled(False)

	# slot to handle change of iata field mapping
	def iataFieldChanged(self, current_index):
		
		if current_index <= 0:
			self.iata_field = None
		else:
			self.iata_field = self._data_fields_model.item(current_index).text()
		
		if self.cityname_field and self.statename_field and self.countryname_field and self.iata_field:
			self.finish_button.setEnabled(True)
		else:
			self.finish_button.setEnabled(False)

	def finishPressed(self):

		self.data_import_finish_signal.emit(self.filename, self.cityname_field, self.statename_field, self.countryname_field, self.iata_field, self._data)
		self.close()

# Test the 'Import Data' dialog
if __name__ == '__main__':

	# create and display the application's "First Steps" dialog
	application = QApplication(sys.argv)

	window = ImportDataDialog()
	window.show()

	sys.exit(application.exec_())