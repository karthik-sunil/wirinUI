from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.animation as anim 

from functools import partial 


from comms import *
from ecgAnimate import *
from ppgAnimate import *
from dataRead import *

def display(a):
    global running
    global t1
    global start
    case = a.text()
    print (case)
   
    
    if case == "Start":
        #start_read()
        if(comPorts.currentComPort == None):
            QMessageBox.warning(mainWindow, 'Error', "Choose COM Port", QMessageBox.Ok , QMessageBox.Ok)
        else:
            try:
                #s = serial.Serial(currentComPort)
                #s.close()

                start.setEnabled(False) 
                stop.setEnabled(True)
                eegAnimate._start()
                t1.start()
                
            except (OSError, comPorts.serial.SerialException):
                QMessageBox.warning(mainWindow, 'Error', "COM Port not available \n Choose another one", QMessageBox.Ok , QMessageBox.Ok)
            
            
    elif case == "Stop":
        stop.setEnabled(False)
        start.setEnabled(True)
        running = False
        
        dataRead.stop_read()

    elif case == "Plot":
        dataRead.plot_data()



def myExitHandler():
    dataRead.stop_read()

app = QApplication(sys.argv)
app.aboutToQuit.connect(myExitHandler)
mainWindow = QMainWindow()
mainWindow.setGeometry(50, 50, 500, 500)
mainWindow.setWindowTitle("Readings")

wid = QWidget()
mainWindow.setCentralWidget(wid)
hmainBox = QHBoxLayout()
wid.setLayout(hmainBox)




toolbar = QToolBar()
mainWindow.addToolBar(toolbar)



#Comports

comPorts = QToolButton()
toolbar.addWidget(comPorts)
comPorts.setText("COM")

#Comports list
menu = QMenu()
findComPorts(menu)
menu.triggered.connect(partial(setComPort, menu))
comPorts.setMenu(menu)
comPorts.setPopupMode(QToolButton.InstantPopup)


#Other toolbar buttons
start = QAction(QIcon(),"Start", mainWindow)
toolbar.addAction(start)
stop  = QAction(QIcon(),"Stop", mainWindow)
stop.setEnabled(False)
toolbar.addAction(stop)
plot  = QAction(QIcon(),"Plot", mainWindow)
toolbar.addAction(plot)
toolbar.actionTriggered[QAction].connect(display)


 
 

leftLayout = QVBoxLayout()
leftLayout.setContentsMargins(0,0,0,0)
leftLayout.setSpacing(0)
ECGFigure = Figure()
PPGFigure = Figure()
ECGCanvas = FigureCanvas(ECGFigure)
PPGCanvas = FigureCanvas(PPGFigure)

ecg = ECGFigure.add_subplot(111)
ecg.set_title("ECG")
ppg = PPGFigure.add_subplot(111)
ppg.set_title("PPG")
ECGCanvas.draw()
PPGCanvas.draw()
ecgAnimate = anim.FuncAnimation(ECGFigure, animateECG, interval=1000)
ecgAnimate.event_source.stop()

#canvas3.draw()
ecgWindow = QWidget()
ecgWindow.setContentsMargins(0,0,0,0)

ecgWindow.setAutoFillBackground(True)
ecgLayout = QVBoxLayout()
ecgLayout.setContentsMargins(0,0,0,0)
ecgLayout.setSpacing(0)
ecgWindow.setLayout(ecgLayout)
ppgWindow = QWidget()
ppgLayout = QVBoxLayout()
ppgLayout.setContentsMargins(0,0,0,0)
ppgLayout.setSpacing(0)
ppgWindow.setLayout(ppgLayout)

ecgToolbar = NavigationToolbar(ECGCanvas,wid)
ppgToolbar = NavigationToolbar(PPGCanvas,wid)

plotSplitter = QSplitter(Qt.Vertical)
ecgLayout.addWidget(ECGCanvas)
ecgLayout.addWidget(ecgToolbar)

leftLayout.addWidget(plotSplitter)
ppgLayout.addWidget(PPGCanvas)
ppgLayout.addWidget(ppgToolbar)
plotSplitter.addWidget(ecgWindow)
plotSplitter.addWidget(ppgWindow)
plotSplitter.setSizes([400,400])
plotSplitter.setStyleSheet("QSplitter::handle {   background: black;}")
plotSplitter.setHandleWidth(1)

leftWidget = QWidget()
leftWidget.setLayout(leftLayout)

horizontalSplitter = QSplitter(Qt.Horizontal)

rightWidget = QWidget()

rightSubLayout = QVBoxLayout()
rightWidget.setLayout(rightSubLayout)

title = QLabel()
gsr = QLabel()
heart_rate = QLabel()
title.setText("Readings:")
gsr.setText("GSR: {}".format(55))
heart_rate.setText("Heart Rate: {}".format(72))
title.setAlignment(Qt.AlignCenter)
gsr.setAlignment(Qt.AlignRight)
rightSubLayout.addWidget(title)
rightSubLayout.addWidget(gsr)
rightSubLayout.addWidget(heart_rate)

horizontalSplitter.addWidget(leftWidget)
horizontalSplitter.addWidget(rightWidget)
horizontalSplitter.setSizes([500,200])

horizontalSplitter.setStyleSheet("QSplitter::handle {   background: black;}")
horizontalSplitter.setHandleWidth(1)
hmainBox.addWidget(horizontalSplitter)

hmainBox.setSpacing(0)
hmainBox.setContentsMargins(0,0,0,0)

statusBar = QStatusBar()
mainWindow.setStatusBar(statusBar)
label = QLabel()
if currentComPort == None:
    label.setText("No COM Port Selected")
else:
    label.setText("Com Port : " + currentComPort)

statusBar.addPermanentWidget(label)