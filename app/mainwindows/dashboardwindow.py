""" Dashboard screen for VIMAAN """
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QSizePolicy, QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QTableView, QPushButton, QLabel, QComboBox
from PyQt5.QtGui import QFont, QPainter, QFontMetrics
from PyQt5.QtCore import QSize, Qt, QAbstractTableModel
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
		return QSize(self.sizeHint().width(), self.sizeHint().height()+20)


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


# A custom 'Table Model' to display data from pandas dataframe
class DataFrameModel(QAbstractTableModel):

	# reimplement constructor (implement constructor of super-class)
	def __init__(self, data, parent=None):
		super().__init__(parent)
		self._data = data

	# implement all methods of the 'Abstract Table Model' to create concrete class
	def rowCount(self, parent=None):
		return self._data.shape[0]

	def columnCount(self, parent=None):
		return self._data.shape[1]

	def data(self, index, role=Qt.DisplayRole):

		if index.isValid() and role == Qt.DisplayRole:
			print(index.row(), index.column())
			if not pd.isnull(self._data.iloc[index.row(), index.column()]):
				return str(self._data.iloc[index.row(), index.column()])

			else:
				return ''

		return None

	def headerData(self, section, orientation, role):

		if role == Qt.DisplayRole:
			if orientation == Qt.Horizontal:
				return self._data.columns[section]

			if orientation == Qt.Vertical:
				return self._data.index[section]

		return None


# Customise the QMainWindow widget to create VIMAAN dashboard
class DashboardWindow(QMainWindow):

	def __init__(self):
		# initialise the QMainWindow
		super().__init__()
		self.initUI()

	def initUI(self):

		# create and display the 'Menu' widgets
		menu_pane = QVBoxLayout()

		import_data_btn = MenuButton('Import Data')
		preprocess_data_btn = MenuButton('Preprocess Data')
		populate_iata_btn = MenuButton('Populate IATAs')

		preprocess_data_btn.setEnabled(False)
		populate_iata_btn.setEnabled(False)

		menu_pane.addWidget(import_data_btn)
		menu_pane.addWidget(preprocess_data_btn)
		menu_pane.addWidget(populate_iata_btn)

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

		# create and display 'input filename' widgets
		input_file_pane = QHBoxLayout()

		input_file_label = QLabel('Input Filename: ')
		input_file_label_font = QFont("Verdana, Helvetica", 10, QFont.Bold)
		input_file_label.setFont(input_file_label_font)

		input_filename_label = ResizeableLabel('')
		input_filename_label.setStyleSheet("border: 1px inset grey;")

		input_file_pane.addWidget(input_file_label)
		input_file_pane.addWidget(input_filename_label)

		# create and display input column's group box
		input_columns_pane = QGroupBox('Input Columns')

		# create and display input column's mapping group box
		input_columns_box = QGridLayout()

		cityname_label = QLabel('City Name: ')
		statename_label = QLabel('State Name: ')
		countryname_label = QLabel('Country Name: ')

		mapped_cityname_label = QLabel()
		mapped_statename_label = QLabel()
		mapped_countryname_label = QLabel()

		input_columns_box.addWidget(cityname_label, 0, 0)
		input_columns_box.addWidget(mapped_cityname_label, 0, 1)
		input_columns_box.addWidget(statename_label, 1, 0)
		input_columns_box.addWidget(mapped_statename_label, 1, 1)
		input_columns_box.addWidget(countryname_label, 2, 0)
		input_columns_box.addWidget(mapped_countryname_label, 2, 1)

		input_columns_pane.setLayout(input_columns_box)

		# create and display output column's mapping group box
		output_columns_pane = QGroupBox('Output Columns')

		# create and display input column's mapping group box
		output_columns_box = QHBoxLayout()

		iata_label = QLabel('Nearest Airport IATA: ')
		mapped_iata_label = QLabel()

		output_columns_box.addWidget(iata_label)
		output_columns_box.addWidget(mapped_iata_label)

		output_columns_pane.setLayout(output_columns_box)

		# Set font for the columns mapping labels
		column_label_font = QFont("Times", 11, QFont.Bold)

		cityname_label.setFont(column_label_font)
		statename_label.setFont(column_label_font)
		countryname_label.setFont(column_label_font)
		iata_label.setFont(column_label_font)

		# create and display input column's mapping outer pane
		input_columns_outer_pane = QVBoxLayout()

		input_columns_outer_pane.addStretch(1)
		input_columns_outer_pane.addWidget(input_columns_pane)
		input_columns_outer_pane.addStretch(1)

		# create and display output column's mapping outer pane
		output_columns_outer_pane = QVBoxLayout()

		output_columns_outer_pane.addStretch(1)
		output_columns_outer_pane.addWidget(output_columns_pane)
		output_columns_outer_pane.addStretch(1)

		# create and display columns mapping pane
		columns_mapping_pane = QHBoxLayout()

		columns_mapping_pane.addStretch(1)
		columns_mapping_pane.addLayout(input_columns_outer_pane)
		columns_mapping_pane.addStretch(1)
		columns_mapping_pane.addLayout(output_columns_outer_pane)
		columns_mapping_pane.addStretch(1)

		# create and display the 'imported data details' layout
		import_details_box = QVBoxLayout()

		import_details_box.addLayout(input_file_pane)
		import_details_box.addLayout(columns_mapping_pane)

		# create and display the 'imported data details' widget
		import_details_pane = QWidget()
		import_details_pane.setLayout(import_details_box)

		import_details_pane.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

		# create and display the 'imported data panel' widgets
		imported_data_table = QTableView()

		imported_data_panel = QVBoxLayout()

		imported_data_panel.addWidget(import_details_pane)
		imported_data_panel.addWidget(imported_data_table)

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

# Test the 'First Steps with VIMAAN' widget
if __name__ == '__main__':

	# create and display the application's "First Steps" widget
	application = QApplication(sys.argv)

	window = DashboardWindow()
	window.show()

	sys.exit(application.exec())