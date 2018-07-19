# import necessary widgets and windows
from widgets.firststepswidget import FirstStepsWidget
from mainwindows.dashboardwindow import DashboardWindow

# import necessary library components for GUI creation
from PyQt5.QtWidgets import QApplication
import sys

# Create the Application Controller
class AppController(QApplication):
	
	# initialise the AppController with necessary data
	def __init__(self, *args, **kargs):
		super().__init__(*args, **kargs)

	def startApp(self):

		# create and display the 'First Steps Widget'
		first_steps_widget = FirstStepsWidget()
		first_steps_widget.show()
		
		# create 'Vimaan Dashboard' and prepare to show when 'First Steps' is closed
		first_steps_widget.widget_closed_signal.connect(self.showDashboard)

	def showDashboard(self):
		print('Show Dashboard')

		dashboard_window = DashboardWindow()
		dashboard_window.show()

# Test the 'Application Contoller'
if __name__ == '__main__':

	application = QApplication(sys.argv)
	
	# create and display the 'First Steps Widget'
	first_steps_widget = FirstStepsWidget()
	first_steps_widget.show()
		
	# create 'Vimaan Dashboard' and prepare to show when 'First Steps' is closed
	# first_steps_widget.widget_closed_signal.connect(self.showDashboard)

	sys.exit(application.exec())
	