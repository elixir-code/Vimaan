from PyQt5.QtCore import Qt, QAbstractTableModel
import pandas as pd

# A custom 'Table Model' to display data from pandas dataframe
class DataFrameModel(QAbstractTableModel):

	# reimplement constructor (implement constructor of super-class)
	def __init__(self, data=None, parent=None):
		super().__init__(parent)
		if data is None:
			data = pd.DataFrame()
		self._data = data

	# implement all methods of the 'Abstract Table Model' to create concrete class
	def rowCount(self, parent=None):
		return self._data.shape[0]

	def columnCount(self, parent=None):
		return self._data.shape[1]

	def data(self, index, role=Qt.DisplayRole):

		if index.isValid() and role == Qt.DisplayRole:
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
				return str(self._data.index[section])
		return None

	# reset the entire data in a model
	def resetData(self, data):

		if data is None:
			data = pd.DataFrame()

		self.beginResetModel()
		self._data = data
		self.endResetModel()