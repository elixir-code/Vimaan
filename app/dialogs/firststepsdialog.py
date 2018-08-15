""" 'First Steps with VIMAAN' instructions screen """

# import necessary libraries for gui creation
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal

import sys

first_steps_instructions = """
1. Download and update <b>Google Chrome Browser</b> to a latest version.<br>
2. Download the <b>Chrome Driver</b> supported for your browser version from <a href="http://chromedriver.chromium.org/">here</a>.
"""

class FirstStepsDialog(QDialog):

	# define the custom signals for use by controller
	dialog_closed_signal = pyqtSignal()

	def __init__(self, *args, **kargs):

		# initialise the QDialog
		super().__init__(*args, **kargs)
		self.setWindowModality(Qt.WindowModal)
		self.initUI()

	def initUI(self):

		# Create and display the 'FIRST STEPS WITH VIMAAN' title
		first_steps_title_box = QHBoxLayout()
		
		first_steps_label = QLabel('First Steps with VIMAAN')
		first_steps_title_font = QFont("Helvetica", 12, QFont.Bold)
		first_steps_label.setFont(first_steps_title_font)

		first_steps_title_box.addStretch(1)
		first_steps_title_box.addWidget(first_steps_label)
		first_steps_title_box.addStretch(10)

		# Create and display the first steps instruction
		first_steps_instrn_box = QHBoxLayout()

		first_steps_instrn_label = QLabel()
		
		first_steps_instrn_label.setText(first_steps_instructions)
		first_steps_instrn_label.setOpenExternalLinks(True)
		# first_steps_instrn_label.setWordWrap(True)

		first_steps_instrn_box.addStretch(1)
		first_steps_instrn_box.addWidget(first_steps_instrn_label)
		first_steps_instrn_box.addStretch(10)

		# Create and display the close button box
		first_steps_close_box = QHBoxLayout()
		first_steps_close_button = QPushButton('Close')
		first_steps_close_button.pressed.connect(self.close)

		first_steps_close_box.addStretch(50)
		first_steps_close_box.addWidget(first_steps_close_button)
		first_steps_close_box.addStretch(1)

		# Create and display the first steps page
		first_steps_main_box = QVBoxLayout()

		first_steps_main_box.addStretch(1)
		first_steps_main_box.addLayout(first_steps_title_box)
		first_steps_main_box.addStretch(1)
		first_steps_main_box.addLayout(first_steps_instrn_box)
		first_steps_main_box.addStretch(1)
		first_steps_main_box.addLayout(first_steps_close_box)
		first_steps_main_box.addStretch(1)

		self.setLayout(first_steps_main_box)

		# set the attributes of the first steps dialog
		self.setWindowTitle('First Steps with VIMAAN')

	def closeEvent(self, event):
		self.dialog_closed_signal.emit()

# Test the 'First Steps with VIMAAN' dialog
if __name__ == '__main__':

	# create and display the application's "First Steps" dialog
	application = QApplication(sys.argv)

	window = FirstStepsDialog()
	window.show()

	sys.exit(application.exec())