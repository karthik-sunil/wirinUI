#import essential performance optimization dependencies 
import sys, glob, time, random, threading, csv, datetime, traceback, serial
from functools import partial 
from multiprocessing import Process, Queue

#import GUI libraries 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

#import main libraries
import pandas as pd
import numpy as np
import pygame
from pyOpenBCI import OpenBCICyton
import pyOpenBCI

#import graphing libraries 
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.widgets.RemoteGraphicsView

#import custom modules
import csvwriter 
from csvwriter import *
import wirinECGx
import mySer

import os

#Variables to be tweaked 
baudRate = 115200
programPath = (os.path.dirname(os.path.abspath(__file__)))
graphInterval = 10
openBCIFile = "newFile2.csv"#.csv
arduinoFile = "newFile1.csv" #.csv
oddballFile = "write.csv"

#Fonts
titleFont = QtGui.QFont("Times", 14, QtGui.QFont.Bold) 
textFont = QtGui.QFont("Times", 12)

#global variable declarations 
openBCIStream = []
buttonAction = "None"
board = None
q = Queue()
running = False
currentComPort = None
buffer = []
ecgBuffer = []
ecgBufy = []
respBufy = []
ecgBufx = []
ppgBufy = []
ppgBufx = []
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

#data annotation handling 
def annotator(button):
    global buttonAction
    if button.isChecked():
        buttonAction = button.text()

#Multithreaded Function to read the OpenBCI stream
def print_raw(sample):
    import csvwriter
    global openBCIStream,buttonAction
    

    openBCIStream =  (sample.channels_data)
    
    systime = datetime.datetime.now().isoformat()
   
    inp = csvwriter.filewriterBCI(openBCIStream,openBCIFile,buttonAction,systime)
        
    q.put(openBCIStream)


#Thread 1 handling data read from Arduino
def start_read():
    global running, buffer, buttonAction, board, ecgBuffer, ecgBufx, ecgBufy, ppgBufy, respBufy
    
    ser = serial.Serial(currentComPort, baudRate)
    
    running = True
    
    #result = pd.read_csv(programPath + arduinoFile + ".csv", header=None)
    
    count = 0

    try:
        board = OpenBCICyton(port=None, daisy=False)
    except:
        print("Couldnt find OpenBCI")

    #Start board thread if board was found
    if(running and board):
        boardThread = threading.Thread(target=board.start_stream, args=(print_raw,))
        boardThread.daemon = True
        boardThread.start()
    
    
    while(running):
        
        data = ser.read()
        print(data)
        mySer.handle_data(int.from_bytes(data,"little"))
        try:
            ecgBufy.append(mySer.ECG[-1])
            ecgBufy = ecgBufy[-4000:]
            
            ppgBufy.append(mySer.PPG_Red[-1])
            ppgBufy = ppgBufy[-4000:]

            resp.append()

            
        except:
            pass
      
#module implementing the oddball paradigm experiment 
def oddball():
    global running
    pygame.init()
    win = pygame.display.set_mode((500, 500))
    precision = 50 # Dynamic variable
    beat_sl_no = 0
  
    with open(os.path.join(programPath,oddballFile), 'w+', newline = '') as writeFile:
        print(writeFile)
        writer = csv.writer(writeFile, delimiter = ',')
        
        rows = ["Experiment: Odd Ball Expt","Normal sound: 500 Hz",
                "Odd sound: 1000 Hz","Marker for normal sound: 5",
                "Marker for odd sound: 7","Marker for correct click: 1",
                "Marker for incorrect click: 0"," "]

        for row in rows:
            writer.writerow([row])

        #Table 
        rows = [["Sound","Response","Result"],
                ["5","Click","0"],
                ["5","No Click","1"],
                ["7","Click","1"],
                ["7","No click","0"],
                [" "],
                ["Sl No","Sound Present Time",
                    "Beat Type","Response Type",
                    "Key Press Time",
                    "Response Time"]]

        for row in rows:
            writer.writerow(row)     
       
        while(1 and running):
            
            beat_sl_no += 1
            row = []
            
            print('Delay 1 Start 2000')
            pygame.time.delay(2000)
            
            diff_4 = random.randint(1, precision) # Difference after 4 seconds
        
            beep_time = (int(2000*diff_4/precision))
            print('Delay 2 Start', beep_time)
            pygame.time.delay(beep_time)
            choose_sound = (random.randint(1, 10) <= 5)   # Generate 80% probability
            
            if(choose_sound == False):
                
                # "Odd Ball"
                beat_type = 7 
                pygame.mixer.music.load(os.path.join(programPath,"tones","500hz.wav"))
                pygame.mixer.music.play(0)        
                sound_present_time = datetime.datetime.now().time()
                
                # Store the time at which the beat occurs            
                start = time.time() 
                flag = True
                break_flag = False
                while(1):
                    event = pygame.event.get()
                    for e in event:
                        if e.type == 12:
                            pygame.quit()


                    mouse_status = (pygame.mouse.get_pressed())    # Check if LMB has been clicked
        
                    if(time.time() - start >= 2):   #  If the driver doesn't click a mouse button in 2 seconds
                        sound_response_time = datetime.datetime.now().time()
                        response_time = 2   
                        response_type = 0 # "Incorrect"
                        break
                    
                    if(mouse_status[0] == 1):             # If the driver clicks a mouse button, a correct repsonse has to be registered
                        response_time = time.time() - start
                        sound_response_time = datetime.datetime.now().time()
                        response_type = 1 # "Correct"
                        print("Correct")
                        flag = False
                        break
                    
                    if(mouse_status[2] == 1):   # Exit
                        break_flag = True
                        break
                    
                if(break_flag == True):
                    break
                    
                if(flag == True):
                    print("Missed the beep")
                    
            else:
                beat_type = 5 #"Normal"
                pygame.mixer.music.load(os.path.join(programPath,"tones","1000hz.wav"))
                pygame.mixer.music.play(0)        
                start = time.time()
                sound_present_time = datetime.datetime.now().isoformat()
                break_flag = False
                
                while(1):
                    
                    pygame.event.get()
                    mouse_status = (pygame.mouse.get_pressed())    
                
                    if(time.time() - start >= 2):
                        sound_response_time = datetime.datetime.now().isoformat()
                        response_time = 2
                        response_type = 1 # "Correct"
                        break
                    
                    if(mouse_status[0] == 1):   # If the driver clicks a mouse button, an incorrect repsonse has to be registered
                        response_time = time.time() - start
                        sound_response_time = datetime.datetime.now().isoformat()
                        response_type = 0 # "Incorrect"
                        print("Incorrect")
                        break
                    
                    if(mouse_status[2] == 1):   #Exit Wondow
                        break_flag = True
                        break
                    
                if(break_flag == True):
                    break
            time1 = []
            
            
            row.append(sound_present_time)
            row.append(beat_sl_no)
            row.append(beat_type)
            row.append(response_type)
            row.append(sound_response_time)
            row.append(response_time)
            print(row)
            writer.writerow(row)
        
        pygame.quit()    


#thread initialization  
t1 = threading.Thread(target=start_read, args=()) 
t2 = threading.Thread(target=oddball,args=())
t1.daemon = True
t2.daemon = True


#checks for COM-ports and lists all available ports  
def findComPorts(menu):
    print("COM port detected")
    menu = menu
    menu.clear()
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswithe('darwin'):
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

#This function sets the choosen comport to the global currentComPort Variable        

def setComPort(menu,a):
    global currentComPort
    currentComPort = a.text()
    label.setText("Com Port : " + currentComPort)
    findComPorts(menu)

#This function handles the top menu bar

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
                #Odd ball disabled for now
                #t2.start()
                
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

    
#When you press Stop button, this function gets called
def stop_read():
    global t1,t2
    global board
    global running
    running = False
    if(board != None):
        board.stop_stream()
    if(t1.isAlive()):
        t1.join() #Stop the data collection thread
        t1 = threading.Thread(target=start_read, args=()) 

    if(t2.isAlive()):
        t2.join() #Stop the odd ball thread
        t2 = threading.Thread(target=oddball, args=()) 
    
    print("Stop")


#PyQtGraph Multiprocessed BCI Plot

def bciPlotFunc(q):
    app2 = QtGui.QApplication([])
    
    win2 = pg.GraphicsWindow(title="Basic plotting examples")
    win2.resize(1000,600)
    win2.setWindowTitle('Open BCI plot')
    p2 = win2.addPlot(title="OpenBCI Feed")
    curve0 = p2.plot(pen='y',)
    curve1 = p2.plot(pen='b',)
    curves = [curve0,curve1]
    def updateInProc(curves):
        updateInProc.y0.append(q.get()[0])
        updateInProc.y1.append(q.get()[1])
        updateInProc.x.append(updateInProc.i)
        updateInProc.i += 1
        updateInProc.y0 = updateInProc.y0[-1000:]
        updateInProc.y1 = updateInProc.y1[-1000:]
        updateInProc.x = updateInProc.x[-1000:]

        curves[0].setData(updateInProc.x,updateInProc.y0)
        curves[1].setData(updateInProc.x,updateInProc.y1)
    
    
    updateInProc.i = 0
    updateInProc.y0 = []
    updateInProc.y1 = []
    updateInProc.x = []

    #update the openBCI chart
    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: updateInProc(curves))
    timer.start(0)

    QtGui.QApplication.instance().exec_()



#Dummy function which is of no use for now
def plot_data():
    pass

#Dummy function which is of no use for now
def updateGraph():
    print("Update Graph")

#Start the openBCI plotting in a new process of its own
def startBciProcess():
    p = Process(target=bciPlotFunc, args=(q,))
    p.start()
    

#Update the graphs here
def update():
    global ecgBuffer
    global heartRate
    global ecgPlot
    global ppgPlot 
    global respPlot
    global respBufy 
    
    try:
        ecgPlot.clear()
        #heartRate.setText("Heart Rate: {}".format(ecgBuffer[0]))
        ecgPlot.plot(ecgBufy)
        ppgPlot.plot(ppgBufy)
        respPlot.plot(respBufy)
    
    except:
        traceback.print_exc()

#This function is called everytime the GUI is closed
def myExitHandler():
    board.disconnect() #Disconnect open BCI stream
    stop_read()
    
    
if __name__ == '__main__':    
    app = QApplication(sys.argv)
    app.aboutToQuit.connect(myExitHandler)
    mainWindow = QMainWindow()
    mainWindow.setGeometry(50, 50, 1200, 800) #Set default dimensions of the window
    mainWindow.setWindowTitle("Readings") #Set title of the Window

    wid = QWidget()
    mainWindow.setCentralWidget(wid)
    hmainBox = QHBoxLayout()
    wid.setLayout(hmainBox)

    toolbar = QToolBar() #Add a top Menu Bar
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
    eX = ecgPlot.getAxis('bottom')
    eX.setLabel('Time')
    print(type(eX))
    eY = ecgPlot.getAxis('left')
    eY.setLabel('Scaled Amplitude')
    ecgPlot.enableAutoRange(enable=True)
    plotSplitter.addWidget(ecgPlot)

    #PPG Chart
    ppgPlot = pg.PlotWidget(title="PPG")
    plotSplitter.addWidget(ppgPlot)
    
    #GSR Chart    
    respPlot = pg.PlotWidget(title="Respiration")
    plotSplitter.addWidget(respPlot)

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
    gsr.setText("GSR: {}".format("--"))
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

