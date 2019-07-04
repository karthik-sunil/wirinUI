#added matplotlib 
import sys
from PyQt5.QtWidgets import *
import serial 
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.animation as animation 
from functools import partial 
def start_read():
    print("start reading")

def stop_read():
    print("stop reading")

def plot_data():
    print("plot")

def display(a):
    case = a.text()
    print (case)
    if case == "Start":
        start_read()
    elif case == "Stop":
        stop_read()
    elif case == "Plot":
        plot_data()

def animate(i):
    pullData = open("eegdata.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    a.clear()
    a.plot(xList,yList)




app = QApplication(sys.argv)
window = QMainWindow()
wid = QWidget()
window.setCentralWidget(wid)




window.setGeometry(0, 0, 500, 500)
hmainBox = QHBoxLayout()
v_layout = QVBoxLayout()
toolbar = QToolBar()
window.addToolBar(toolbar)
comport = QToolButton()
comport.setText("COM")
menu = QMenu()
menu.addAction("COM1",)
menu.addAction("COM3",)
menu.triggered.connect()
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
figure = Figure()
canvas = FigureCanvas(figure)
canvas2 = FigureCanvas(figure)
#canvas3 = FigureCanvas(figure)
newQWidget = QWidget()
ax = figure.add_subplot(111)
canvas.draw()
canvas2.draw()
#canvas3.draw()

navtool = NavigationToolbar(canvas,newQWidget)


v_layout.addWidget(canvas)
newQWidget.setLayout(v_layout)
hmainBox.addWidget(newQWidget)
v_layout.addWidget(canvas2)
v_layoutRight = QVBoxLayout()
#v_layoutRight.addWidget(canvas3)
hmainBox.addLayout(v_layout)
hmainBox.addLayout(v_layoutRight)


window.setWindowTitle("Readings")
wid.setLayout(hmainBox)


window.show()
sys.exit(app.exec_())
