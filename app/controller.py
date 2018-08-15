# import necessary widgets and windows
from dialogs.firststepsdialog import FirstStepsDialog
from mainwindows.dashboardwindow import DashboardWindow
from dialogs.importdatadialog import ImportDataDialog
from dialogs.preprocessdatadialog import PreprocessDataDialog

from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtCore import Qt, QAbstractTableModel, QDir
import sys

# import necessary models
from models.dataframemodel import DataFrameModel

# Create a Application Controller class
class ControlledApplication(QApplication):
	
	def __init__(self, *args, **kargs):
		super().__init__(*args, **kargs)
		self._active_dialog = None

		# chrome driver location
		self.chromedriver_path = None

		# imported data and mapping details
		self.filename = None

		self.cityname_field = None
		self.statename_field = None
		self.countryname_field = None

		self.iata_field = None

		# create the data models for use by controller
		self.data_model = DataFrameModel()

	# initialise main window and start main event loop
	def startApplication(self):

		# create the dashboard window
		self.dashboard_window = DashboardWindow()
		self.dashboard_window.setDataModel(self.data_model)

		self.dashboard_window.select_chromedriver_menu_pressed.connect(self.selectChromeDriver)
		self.dashboard_window.import_data_menu_pressed.connect(self.showImportDataDialog)
		self.dashboard_window.preprocess_data_menu_pressed.connect(self.showPreprocessDataDialog)

		# create and display the first steps widget
		first_steps_widget = FirstStepsDialog(parent = self.dashboard_window)
		first_steps_widget.dialog_closed_signal.connect(self.dashboard_window.show)
		first_steps_widget.show()

		self.exec()

	# select the chrome driver executable file
	def selectChromeDriver(self):

		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog

		filename, _ = QFileDialog.getOpenFileName(self.dashboard_window, "Choose ChromeDriver", "chromedriver", "executable (application/x-executable)", options=options)
		
		if filename:
			self.chromedriver_path = filename
			self.dashboard_window.setChromeDriverPath(filename)

			self.dashboard_window.enableImportData()

	# show the import data dialog
	def showImportDataDialog(self):

		import_data_dialog = ImportDataDialog(parent=self.dashboard_window)
		import_data_dialog.data_import_finish_signal.connect(self.dataImported)

		self._active_dialog = import_data_dialog
		import_data_dialog.show()

	# slot to handle imported data details (imported using import data dialog)
	def dataImported(self, filename, cityname_field, statename_field, countryname_field, iata_field, data):

		self._active_dialog = None

		self.filename = filename

		self.cityname_field = cityname_field
		self.statename_field = statename_field
		self.countryname_field = countryname_field

		self.iata_field = iata_field
		
		self.dashboard_window.setImportedDataDetails(filename, cityname_field, statename_field, countryname_field, iata_field)
		self.data_model.resetData(data)

		self.dashboard_window.enablePreprocessData()
		self.dashboard_window.enablePopulateIATAs()

	def showPreprocessDataDialog(self):
		
		preprocess_data_dialog = PreprocessDataDialog(parent=self.dashboard_window, data=self.data_model._data, fields=[self.cityname_field, self.statename_field, self.countryname_field])

		self._active_dialog = preprocess_data_dialog
		preprocess_data_dialog.show()

# Test the application
if __name__ == '__main__':
	
	controller = ControlledApplication(sys.argv)
	controller.startApplication()