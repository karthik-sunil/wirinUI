import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
def start_read():
    print("start reading")

def stop_read():
    print("stop reading")

def plot_data():
    print("haha")
def display(a):
    case = a.text()
    if case == "Start":
        start_read()
    elif case == "Stop":
        stop_read()
    elif case == "Plot":
        plot_data()




app = QApplication(sys.argv)

window = QMainWindow()
window.setGeometry(0, 0, 500, 500)
toolbar = QToolBar()
window.addToolBar(toolbar)
comport = QToolButton()
comport.setText("COM")
menu = QMenu()
menu.addAction("Port 1", )
menu.addAction("Port 2", )
comport.setMenu(menu)
comport.setPopupMode(QToolButton.InstantPopup)
toolbar.addWidget(comport)
start = QAction(QIcon(),"Start", window)
toolbar.addAction(start)
stop  = QAction(QIcon(),"Stop", window)
toolbar.addAction(stop)
plot  = QAction(QIcon(),"Plot", window)
toolbar.addAction(plot)
toolbar.actionTriggered[QAction].connect(display)
window.setWindowTitle("Readings")
window.show()
sys.exit(app.exec_())

