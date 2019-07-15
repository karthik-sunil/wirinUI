import sys
import csvwriter 
from PyQt5.QtWidgets import *
import serial 
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import matplotlib.animation as anim 
from functools import partial 
import glob 
import threading
import wirinECGx
import pandas as pd
import numpy as np
import random
import time


from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.widgets.RemoteGraphicsView

from csvwriter import *
import datetime
import pyOpenBCI
from multiprocessing import Process, Queue
from pyOpenBCI import OpenBCICyton

titleFont = QtGui.QFont("Times", 14, QtGui.QFont.Bold) 
textFont = QtGui.QFont("Times", 12)


openBCIStream = []

buttonAction = "None"
board = None
q = Queue()

running = False
currentComPort = None
baudRate = 9600
graphInterval = 10
buffer = []
ecgBuffer = []
ecgBufy = []
ecgBufx = []
    
data = []
ix = 0

y1 = []
y2 = []
y3 = []
y4 = []
y5 = []
y6 = []
y7 = []
y8 = []
xss = []
data = []

bx = 0

BCIplt = plt.figure()
bciSub = BCIplt.add_subplot(1,1,1)


def annotator(button):
    global buttonAction
    if button.isChecked():
        buttonAction = button.text()

def print_raw(sample):
    global openBCIStream
    openBCIStream =  (sample.channels_data)
    #print("From print_Raw: ", end= "")
    #print(openBCIStream)
    
    q.put(openBCIStream)



   


def start_read():
    global running
    global buffer
    global buttonAction
    global board 
    global ecgBuffer
    global ecgBufx
    global ecgBufy
    ser = serial.Serial(currentComPort, baudRate)
    running = True
    
    result = pd.read_csv(r"E:\\Coding\\Wirin\\wirinUI\\data_1.csv", header=None)
    
    count = 0

    try:
        board = OpenBCICyton(port=None, daisy=False)
    except:
        print("Couldnt find OpenBCI")

    '''
    if(running):
        boardThread = threading.Thread(target=board.start_stream, args=(print_raw,))
        boardThread.daemon = True
        boardThread.start()
    '''
    
    while(running):
        '''
        data = ser.readline()
        data = data.decode().strip()
        '''
        #data = ",".join(map(str,l1[count]))
        ecgBufy.append(result[1][count]) 
        ecgBufx.append(count)
        count += 1
        #print(count)
        systime = datetime.datetime.now().isoformat()
        #data = data + c 
        #inp = filewriter(data,"newFile",buttonAction,systime)
        

        
        ecgBufy = ecgBufy[-4000:]
        ecgBufx = ecgBufx[-4000:]
         
        if(count % 4000 == 0):
            ecgBuffer = wirinECGx.f(ecgBufx, ecgBufy, 500.0)
            #print(ecgBuffer)
      
    

t1 = threading.Thread(target=start_read, args=()) 
t1.daemon = True
def findComPorts(menu):
    print("COM port detected")
    menu = menu
    menu.clear()
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
    for port in ports:
        
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
            
        except (OSError, serial.SerialException):
            pass
    
     
    
    if len(result) == 0:
        action = menu.addAction("NO PORTS")
        action.setEnabled(False)
    for r in result:
        r = menu.addAction(r)
  
  

def setComPort(menu,a):
    global currentComPort
    currentComPort = a.text()
    label.setText("Com Port : " + currentComPort)
    findComPorts(menu)

def display(a):
    global running
    global t1
    global start

    case = a.text()
    print(currentComPort)
    if case == "Start":
        print("START")
        if(currentComPort == None):
            QMessageBox.warning(mainWindow, 'Error', "Choose COM Port", QMessageBox.Ok , QMessageBox.Ok)
        
        else:
        
            try:
        
                s = serial.Serial(currentComPort)
                s.close()

                start.setEnabled(False) 
                stop.setEnabled(True)
        
        
              
        
        
                t1.start()
                
            except (OSError, serial.SerialException):
                QMessageBox.warning(mainWindow, 'Error', "COM Port not available \n Choose another one", QMessageBox.Ok , QMessageBox.Ok)
            
            
    elif case == "Stop":
        
        stop.setEnabled(False)
        start.setEnabled(True)
        
        stop_read()

    elif case == "Plot":
        plot_data()
    elif case == "OpenBCI Plot":
        startBciProcess()        

    

def stop_read():
    global t1
    global board
    global running
    running = False
    if(board != None):
        board.stop_stream()
    print("Stop")
    #ser.close()
    if(t1.isAlive()):
        print("Stop")
        t1.join()
        
        t1 = threading.Thread(target=start_read, args=()) 
    print("Stop")

def plot_data():
    print("plot")


def updateGraph():
    print("Update Graph")

#This function handles top menu bar press

""" def animateECG(i):
    global buffer
    #print("Inside animate")
    #pullData = open("eegdata.txt","r").read()
    #dataList = pullData.split('\n')
    
    x = (pd.read_csv(r"data_1.csv",header=None)[1][:4000]).tolist()
    m = wirinECGx.f(data,500.0)
     for eachLine in dataList:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y)) 
    ecg.clear()
    if(len(m[2])):
        ecg.plot(m[1],m[2]) """


def animatePPG(i):
    #print("Inside animate")fwiri
    # pullData = open("eegdata.txt","r").read()
    # dataList = pullData.split('\n')
    # xList = []
    # yList = []
    # for eachLine in dataList:
    #     if len(eachLine)>1:
    #         x,y = eachLine.split(',')
    #         xList.append(int(x))
    #         yList.append(int(y))
    # ppg.clear()
    # ppg.plot(xList,yList)
    pass


def animateBCI(q,i):
    openBCIStream = []
    global ix
    global bx
    uVolts_per_count = (4500000)/24/(2**23-1)
    #print(type(q))
    
    for i in range(250):    
        if(not q.empty()):
            openBCIStream = q.get()
            
            
            try:
                #print("From animate =>", end="")
                #print(openBCIStream)
                y1.append(openBCIStream[0]*uVolts_per_count)
                # y2.append(openBCIStream[1]*uVolts_per_count)
                # y3.append(openBCIStream[2]*uVolts_per_count)
                # y4.append(openBCIStream[3]*uVolts_per_count)
                # y5.append(openBCIStream[4]*uVolts_per_count)
                # y6.append(openBCIStream[5]*uVolts_per_count)
                # y7.append(openBCIStream[6]*uVolts_per_count)
                # y8.append(openBCIStream[7]*uVolts_per_count) 
                xss.append(ix)
                ix += 1
                xs = xss[-50:]
            except:
                pass

        bciSub.clear()
        bciSub.plot(xs, y1[-50:])
        # bciSub.plot(xs, y2[-50:])
        # bciSub.plot(xs, y3[-50:])
        # bciSub.plot(xs, y4[-50:])
        # bciSub.plot(xs, y5[-50:])
        # bciSub.plot(xs, y6[-50:])
        # bciSub.plot(xs, y7[-50:])
        # bciSub.plot(xs, y8[-50:]) 
        


def startBciProcess():
    
    p = Process(target=bciPlotFunc, args=(q,))
    p.start()
    

def update():
    global ecgBuffer
    global q
    global heartRate
    q.put(random.randint(1,5))
     
    
    try:
      #print(ecgBuffer[4])
      ecgPlot.clear()
      heartRate.setText("Heart Rate: {}".format(ecgBuffer[0]))
      ecgPlot.plot(ecgBuffer[2],ecgBuffer[3] ,pen=None, symbol='o')
      ecgPlot.plot(ecgBuffer[5])

    except:
        pass




def bciPlotFunc(q):
    app2 = QtGui.QApplication([])
    
    win2 = pg.GraphicsWindow(title="Basic plotting examples")
    win2.resize(1000,600)
    win2.setWindowTitle('Open BCI plot')
    p2 = win2.addPlot(title="OpenBCI Feed")
    curve = p2.plot(pen='y',)

    def updateInProc(curve):
        updateInProc.y.append(q.get())
        updateInProc.x.append(updateInProc.i)
        updateInProc.i += 1
        updateInProc.y = updateInProc.y[-100:]
        updateInProc.x = updateInProc.x[-100:]

        curve.setData(updateInProc.x,updateInProc.y)
        
    
    
    updateInProc.i = 0
    updateInProc.y = []
    updateInProc.x = []
    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: updateInProc(curve))
    timer.start(50)

    QtGui.QApplication.instance().exec_()

def myExitHandler():
    board.disconnect()
    stop_read()
    
    
if __name__ == '__main__':    
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(myExitHandler)
    mainWindow = QMainWindow()
    mainWindow.setGeometry(50, 50, 1200, 800)
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
    bciPlot  = QAction(QIcon(),"OpenBCI Plot", mainWindow)
    toolbar.addAction(bciPlot)
    toolbar.actionTriggered[QAction].connect(display)
    
    
    #Create the left layout
    leftLayout = QVBoxLayout()
    leftLayout.setContentsMargins(0,0,0,0)
    leftLayout.setSpacing(0)
    plotSplitter = QSplitter(Qt.Vertical)
    plotSplitter.setSizes([400,400,400])
    plotSplitter.setStyleSheet("QSplitter::handle { background: black; }")
    plotSplitter.setHandleWidth(2)
    leftLayout.addWidget(plotSplitter)
    leftWidget = QWidget()
    leftWidget.setLayout(leftLayout)

    
    #Set chart configurations
    pg.setConfigOptions(antialias=False)
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
    
    #ECG Chart
    ecgPlot = pg.PlotWidget(title="ECG")
    ecgPlot.enableAutoRange(enable=True)
    plotSplitter.addWidget(ecgPlot)

    #PPG Chart
    ppgPlot = pg.PlotWidget(title="PPG")
    plotSplitter.addWidget(ppgPlot)
    
    #GSR Chart    
    gsrPlot = pg.PlotWidget(title="GSR")
    plotSplitter.addWidget(gsrPlot)

   

    
    
    horizontalSplitter = QSplitter(Qt.Horizontal)

    #
    rightWidget = QWidget()

    rightLayout = QVBoxLayout()
    rightWidget.setLayout(rightLayout)

    annotate = QFormLayout()
    annotLabel = QLabel("Annotate")
    
    annotLabel.setFont(titleFont)
    annotate.addWidget(annotLabel)
    
    btn1 = QRadioButton("Heavy Traffic", rightWidget)
    
    btn2 = QRadioButton("Moderate Traffic", rightWidget)
    btn3 = QRadioButton("Sparse Traffic", rightWidget)
    #btn4 = QRadioButton("something", rightWidget)
    #btn5 = QRadioButton("something else", rightWidget)
    
    btns = [btn1,btn2,btn3]
    
    
    for btn in btns:
        btn.setFont(textFont)
        annotate.addWidget(btn)

    rightLayout.addLayout(annotate)

    btn1.toggled.connect(lambda:annotator(btn1))
    btn2.toggled.connect(lambda:annotator(btn2))
    btn3.toggled.connect(lambda:annotator(btn3))    
    
    title = QLabel("Readings:")
    title.setFont(titleFont)
    title.setAlignment(Qt.AlignCenter)
    
    rightForm = QFormLayout()
    rightLayout.addLayout(rightForm)
    
    rightForm.addWidget(title)
    gsr = QLabel()
    gsr.setText("GSR: {}".format(55))
    gsr.setAlignment(Qt.AlignCenter)
    rightForm.addWidget(gsr)
    
    heartRate = QLabel()
    heartRate.setText("Heart Rate: __")
    heartRate.setAlignment(Qt.AlignCenter)
    rightForm.addWidget(heartRate)
    
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


    timer1 = QTimer()
    timer1.timeout.connect(update)
    timer1.start(300)
    menu.aboutToShow.connect(partial(findComPorts,menu))
    


    mainWindow.show()

    sys.exit(app.exec_())

