""" Dashboard screen for VIMAAN """
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSizePolicy, QDesktopWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QTableView, QPushButton, QLabel, QComboBox
from PyQt5.QtGui import QFont, QPainter, QFontMetrics
from PyQt5.QtCore import QSize, Qt, pyqtSignal

import sys

import pandas as pd

about_vimaan = """<p>
Project <strong>VIMAAN</strong> is a highly specific enterprise <b>web-mining</b> project undertaken to tag places around the world to their <b>nearest airports</b>.
</p>

<p>
The project <i>source code</i> can be found on <a href='https://github.com/elixir-code'>github</a> and is licensed under the <b>BSD 3-Clause license</b>.
</p>
"""

# A custom 'menu button' class
class MenuButton(QPushButton):

	def __init__(self, *args, **kargs):
		
		# initialise the QPushButton
		super().__init__(*args, **kargs)

		menu_button_font = QFont("TypeWriter", 13)
		self.setFont(menu_button_font)

		self.setStyleSheet("QPushButton {padding-top: 25px; padding-bottom:25px; padding-left:100px; padding-right:100px;}")


	def minimumSizeHint(self):
		return QSize(self.sizeHint().width(), self.sizeHint().height()+10)


# A custom 'resizable label' class (that trucates text with elipsis ...)
class ResizeableLabel(QLabel):

	# reimplement constructor (implement constructor of super-class)
	def __init__(self, *args, **kargs):
		super().__init__(*args, **kargs)
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
		# self.setMaximumWidth(700)

	# set default size of label at start
	def sizeHint(self):
		return QSize(285, QLabel().sizeHint().height())

	# set minimum size hint to allow horizontal resizability
	def minimumSizeHint(self):
		return QSize(0, 23)

	# callback for paint event
	def paintEvent(self, event):
		painter = QPainter(self)

		metrics = QFontMetrics(self.font())
		elided  = metrics.elidedText(self.text(), Qt.ElideRight, self.width())

		painter.drawText(self.rect(), self.alignment(), elided)

	def setText(self, text):
		super().setText(text)
		self.setToolTip(text)


# Customise the QMainWindow widget to create VIMAAN dashboard
class DashboardWindow(QMainWindow):

	# define the custom signals for use by controller
	select_chromedriver_menu_pressed = pyqtSignal()
	import_data_menu_pressed = pyqtSignal()
	preprocess_data_menu_pressed = pyqtSignal()

	def __init__(self):
		# initialise the QMainWindow
		super().__init__()
		self.initUI()

	def initUI(self):

		# create and display the 'Menu' widgets
		menu_pane = QVBoxLayout()

		select_chromedriver_btn = MenuButton('Select ChromeDriver')
		self.import_data_btn = MenuButton('Import Data')
		self.preprocess_data_btn = MenuButton('Preprocess Data')
		self.populate_iata_btn = MenuButton('Populate IATAs')

		self.import_data_btn.setEnabled(False)
		self.preprocess_data_btn.setEnabled(False)
		self.populate_iata_btn.setEnabled(False)

		menu_pane.addWidget(select_chromedriver_btn)
		menu_pane.addWidget(self.import_data_btn)
		menu_pane.addWidget(self.preprocess_data_btn)
		menu_pane.addWidget(self.populate_iata_btn)

		# connect the custom controller signals to menu button's pressed event
		select_chromedriver_btn.pressed.connect(self.select_chromedriver_menu_pressed)
		self.import_data_btn.pressed.connect(self.import_data_menu_pressed)
		self.preprocess_data_btn.pressed.connect(self.preprocess_data_menu_pressed)

		# create and display 'About VIMAAN' widgets
		about_vimaan_pane = QGroupBox('About VIMAAN')
		
		about_vimaan_box = QVBoxLayout()
		
		about_vimaan_label = QLabel(about_vimaan)
		
		about_vimaan_label.setWordWrap(True)
		about_vimaan_label.setOpenExternalLinks(True)
		about_vimaan_box.addWidget(about_vimaan_label)

		about_vimaan_pane.setLayout(about_vimaan_box)
		
		# create and display left panel contents
		left_panel = QVBoxLayout()
		left_panel.addStretch(1)
		left_panel.addLayout(menu_pane)
		left_panel.addStretch(5)
		left_panel.addWidget(about_vimaan_pane)
		left_panel.addStretch(1)

		# create and display 'chromedriver' widgets
		chromedriver_pane = QHBoxLayout()

		chromedriver_label = QLabel('Chrome Driver:  ')
		chromedriver_label_font = QFont("Verdana, Helvetica", 10, QFont.Bold)
		chromedriver_label.setFont(chromedriver_label_font)

		self.chromedriver_path_label = ResizeableLabel('')
		self.chromedriver_path_label.setStyleSheet("border: 1px inset grey;")

		chromedriver_pane.addWidget(chromedriver_label)
		chromedriver_pane.addWidget(self.chromedriver_path_label)

		# create and display 'input filename' widgets
		input_file_pane = QHBoxLayout()

		input_file_label = QLabel('Input Filename: ')
		input_file_label_font = QFont("Verdana, Helvetica", 10, QFont.Bold)
		input_file_label.setFont(input_file_label_font)

		self.input_filename_label = ResizeableLabel('')
		self.input_filename_label.setStyleSheet("border: 1px inset grey;")

		input_file_pane.addWidget(input_file_label)
		input_file_pane.addWidget(self.input_filename_label)

		# create and display input field's group box
		input_fields_pane = QGroupBox('Input fields')

		# create and display input field's mapping group box
		input_fields_box = QGridLayout()

		cityname_label = QLabel('City Name: ')
		statename_label = QLabel('State Name: ')
		countryname_label = QLabel('Country Name: ')

		self.mapped_cityname_label = QLabel()
		self.mapped_statename_label = QLabel()
		self.mapped_countryname_label = QLabel()

		input_fields_box.addWidget(cityname_label, 0, 0)
		input_fields_box.addWidget(self.mapped_cityname_label, 0, 1)
		input_fields_box.addWidget(statename_label, 1, 0)
		input_fields_box.addWidget(self.mapped_statename_label, 1, 1)
		input_fields_box.addWidget(countryname_label, 2, 0)
		input_fields_box.addWidget(self.mapped_countryname_label, 2, 1)

		input_fields_pane.setLayout(input_fields_box)

		# create and display output field's mapping group box
		output_fields_pane = QGroupBox('Output fields')

		# create and display input field's mapping group box
		output_fields_box = QHBoxLayout()

		iata_label = QLabel('Nearest Airport IATA: ')
		self.mapped_iata_label = QLabel()

		output_fields_box.addWidget(iata_label)
		output_fields_box.addWidget(self.mapped_iata_label)

		output_fields_pane.setLayout(output_fields_box)

		# Set font for the fields mapping labels
		field_label_font = QFont("Times", 11, QFont.Bold)

		cityname_label.setFont(field_label_font)
		statename_label.setFont(field_label_font)
		countryname_label.setFont(field_label_font)
		iata_label.setFont(field_label_font)

		# create and display input field's mapping outer pane
		input_fields_outer_pane = QVBoxLayout()

		input_fields_outer_pane.addStretch(1)
		input_fields_outer_pane.addWidget(input_fields_pane)
		input_fields_outer_pane.addStretch(1)

		# create and display output field's mapping outer pane
		output_fields_outer_pane = QVBoxLayout()

		output_fields_outer_pane.addStretch(1)
		output_fields_outer_pane.addWidget(output_fields_pane)
		output_fields_outer_pane.addStretch(1)

		# create and display fields mapping pane
		fields_mapping_pane = QHBoxLayout()

		fields_mapping_pane.addStretch(1)
		fields_mapping_pane.addLayout(input_fields_outer_pane)
		fields_mapping_pane.addStretch(1)
		fields_mapping_pane.addLayout(output_fields_outer_pane)
		fields_mapping_pane.addStretch(1)

		# create and display the 'imported data details' layout
		import_details_box = QVBoxLayout()

		import_details_box.addLayout(chromedriver_pane)
		import_details_box.addLayout(input_file_pane)
		import_details_box.addLayout(fields_mapping_pane)

		# create and display the 'imported data details' widget
		import_details_pane = QWidget()
		import_details_pane.setLayout(import_details_box)

		import_details_pane.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

		# create and display the 'imported data panel' widgets
		self.imported_data_table = QTableView()

		imported_data_panel = QVBoxLayout()

		imported_data_panel.addWidget(import_details_pane)
		imported_data_panel.addWidget(self.imported_data_table)

		# create and display the 'dashboard' widgets
		dashboard_main_pane = QHBoxLayout()

		dashboard_main_pane.addSpacing(20)
		dashboard_main_pane.addLayout(left_panel)
		dashboard_main_pane.addSpacing(30)
		dashboard_main_pane.addLayout(imported_data_panel)
		dashboard_main_pane.addSpacing(20)

		# Create and display contents of main window
		dashboard_main_widget = QWidget()
		self.setCentralWidget(dashboard_main_widget)

		dashboard_main_widget.setLayout(dashboard_main_pane)

		# set the attributes of the first steps widget
		self.setWindowTitle('Project VIMAAN - Dashboard')
		self.resize(QDesktopWidget().availableGeometry().size())

	# set the imported data details in the dashboard
	def setImportedDataDetails(self, filename, cityname_field, statename_field, countryname_field, iata_field):

		self.input_filename_label.setText(filename)
		self.mapped_cityname_label.setText(cityname_field)
		self.mapped_statename_label.setText(statename_field)
		self.mapped_countryname_label.setText(countryname_field)
		self.mapped_iata_label.setText(iata_field)

	def setChromeDriverPath(self, chromedriver_path):
		self.chromedriver_path_label.setText(chromedriver_path)

	# set the table data model
	def setDataModel(self, data_model):
		self.imported_data_table.setModel(data_model)

	# enable the import data buttons
	def enableImportData(self):
		self.import_data_btn.setEnabled(True)

	# enable the preprocess data button
	def enablePreprocessData(self):
		self.preprocess_data_btn.setEnabled(True)

	# enable the populate iata's button
	def enablePopulateIATAs(self):
		self.populate_iata_btn.setEnabled(True)

# Test the 'First Steps with VIMAAN' widget
if __name__ == '__main__':

	# create and display the application's "First Steps" widget
	application = QApplication(sys.argv)

	window = DashboardWindow()
	window.show()

	sys.exit(application.exec())