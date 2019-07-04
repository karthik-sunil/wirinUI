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
import threading
running = False
currentComPort = None

def start_read():
    global running

    


    print("start reading")
    running = True
    while(running):
        print(running)
t1 = threading.Thread(target=start_read, args=()) 
def stop_read():
    print
    running = False
    if(t1.isAlive()):
        t1.join()

def plot_data():
    print("plot")

def display(a):
    global running
    global t1
    case = a.text()
    print (case)
   
        
    if case == "Start":
        #start_read()
        if(currentComPort == None):
            QMessageBox.warning(mainWindow, 'Error', "Choose COM Port", QMessageBox.Ok , QMessageBox.Ok)
        else:
            try:
                s = serial.Serial(currentComPort)
                s.close()
                t1.start()
                
            except (OSError, serial.SerialException):
                QMessageBox.warning(mainWindow, 'Error', "COM Port not available \n Choose another one", QMessageBox.Ok , QMessageBox.Ok)
            
            
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


def findComPorts(menu):
    menu = menu
    menu.clear()
    print("Hello")
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    print(ports)
    #print(menu)
    for port in ports:
        
        try:
            s = serial.Serial(port)
            s.close()
            #print(type(port))
            result.append(port)
            
        except (OSError, serial.SerialException):
            pass
     
    
    #result = ["COM1","COM2"]
    if len(result) == 0:
        action = menu.addAction("NO PORTS")
        action.setEnabled(False)
    for r in result:
        r = menu.addAction(r)
    #menu.triggered.disconnect()
    #menu.triggered.connect(partial(setComPort, menu))

def setComPort(menu,a):
    print(a.text())
    currentComPort = a.text()
    print(currentComPort)
    findComPorts(menu)
   
def myExitHandler():
    stop_read()

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

mainWindow.show()
sys.exit(app.exec_())

