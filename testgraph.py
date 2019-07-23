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

#program parameters and files   
baudRate = 115200
programPath = ""
graphInterval = 10
openBCIFile = "newFile2"#.csv
arduinoFile = "newFile1" #.csv
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
    global running, buffer, buttonAction, board, ecgBuffer, ecgBufx, ecgBufy, ppgBuffer, ppgBufx, ppgBufy 
    
    ser = serial.Serial(currentComPort, baudRate)
    
    running = True
    
    result = pd.read_csv(programPath + arduinoFile, header=None)
    
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
        #data = data.decode().strip()
        mySer.handle_data(int.from_bytes(data,"little"))
        try:
          
            ecgBufy.append(mySer.PPG_Red[-1])
            ecgBufy = ecgBufy[-4000:]
            
        except:
            pass
      
#module implementing the oddball paradigm experiment 
def oddball():
    global running
    pygame.init()
    win = pygame.display.set_mode((500, 500))
    precision = 50 # Dynamic variable
    beat_sl_no = 0
  
    with open(programPath + oddballFile, 'w+', newline = '') as writeFile:
        print(writeFile)
        writer = csv.writer(writeFile, delimiter = ',')
        row = []

        row_append = ["Experiment: Odd Ball Expt","Normal sound: 500 Hz","Odd sound: 1000 Hz","Marker for normal sound: 5","Marker for odd sound: 7","Marker for correct click: 1","Marker for incorrect click: 0"," "]
        row_append_index = len(row_append)
        count = 0 
        for  count in range(row_append_index):
            row = []
            row.append(row_append[count])
            writer.writerow(row)
        #Table 
        row = []
        row.append("Sound")
        row.append("Response")
        row.append("Result")
        writer.writerow(row)
        
        row = []
        row.append("5")
        row.append("CLick")
        row.append("0")
        writer.writerow(row)
        
        row = []
        row.append("5")
        row.append("No CLick")
        row.append("1")
        writer.writerow(row)
        
        row = []
        row.append("7")
        row.append("CLick")
        row.append("1")
        writer.writerow(row)
        
        row = ["7", "No Click", "0"]
        writer.writerow(row)
        
        
        row = []
        row.append(" ")
        writer.writerow(row)
        
        row = []        #Get column headers
        row.append("Sl No")
        row.append("Sound Present Time")
        row.append("Beat Type")
        row.append("Response Type")
        row.append("Key Press Time")
        row.append("Response Time")
        
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
                pygame.mixer.music.load(path+r"500hz.wav")
                pygame.mixer.music.play(0)        
                sound_present_time = datetime.datetime.now().time()
                
                # Store the time at which the beat occurs            
                start = time.time() 
                flag = True
                break_flag = False
                while(1):
                    pygame.event.get()
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
                pygame.mixer.music.load(path+r"1000hz.wav")
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
            #a = time.time()
            time1 = []
            
            
            row.append(sound_present_time)
            -row.append(beat_sl_no)
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

    

def stop_read():
    global t1,t2
    global board
    global running
    running = False
    if(board != None):
        board.stop_stream()
    if(t1.isAlive()):
        t1.join()
        t1 = threading.Thread(target=start_read, args=()) 

    if(t2.isAlive()):
        t2.join()
        t2 = threading.Thread(target=oddball, args=()) 
    
    print("Stop")

def plot_data():
    print("plot")


def updateGraph():
    print("Update Graph")

#Junk code from Matplotlib

# """ def animateECG(i):
#     global buffer
#     #print("Inside animate")
#     #pullData = open("eegdata.txt","r").read()
#     #dataList = pullData.split('\n')louikjh
    
#     x = (pd.read_csv(r"data_1.csv",header=None)[1][:4000]).tolist()
#     m = wirinECGx.f(data,500.0)
#      for eachLine in dataList:
#         if len(eachLine)>1:
#             x,y = eachLine.split(',')
#             xList.append(int(x))
#             yList.append(int(y)) 
#     ecg.clear()
#     if(len(m[2])):
#         ecg.plot(m[1],m[2]) """


# def animatePPG(i):
#     #print("Inside animate")fwiri
#     # pullData = open("eegdata.txt","r").read()
#     # dataList = pullData.split('\n')
#     # xList = []
#     # yList = []
#     # for eachLine in dataList:
#     #     if len(eachLine)>1:
#     #         x,y = eachLine.split(',')
#     #         xList.append(int(x))
#     #         yList.append(int(y))
#     # ppg.clear()
#     # ppg.plot(xList,yList)
#     pass


# def animateBCI(q,i):
#     openBCIStream = []
#     global ix
#     global bx
#     uVolts_per_count = (4500000)/24/(2**23-1)
#     #print(type(q))
    
#     for i in range(250):    
#         if(not q.empty()):
#             openBCIStream = q.get()
            
            
#             try:
#                 #print("From animate =>", end="")
#                 #print(openBCIStream)
#                 y1.append(openBCIStream[0]*uVolts_per_count)
#                 # y2.append(openBCIStream[1]*uVolts_per_count)
#                 # y3.append(openBCIStream[2]*uVolts_per_count)
#                 # y4.append(openBCIStream[3]*uVolts_per_count)
#                 # y5.append(openBCIStream[4]*uVolts_per_count)
#                 # y6.append(openBCIStream[5]*uVolts_per_count)
#                 # y7.append(openBCIStream[6]*uVolts_per_count)
#                 # y8.append(openBCIStream[7]*uVolts_per_count) 
#                 xss.append(ix)
#                 ix += 1
#                 xs = xss[-50:]
#             except:
#                 pass

#         bciSub.clear()
#         bciSub.plot(xs, y1[-50:])
#         # bciSub.plot(xs, y2[-50:])
#         # bciSub.plot(xs, y3[-50:])
#         # bciSub.plot(xs, y4[-50:])
#         # bciSub.plot(xs, y5[-50:])
#         # bciSub.plot(xs, y6[-50:])
#         # bciSub.plot(xs, y7[-50:])
#         # bciSub.plot(xs, y8[-50:]) 
        


def startBciProcess():
    
    p = Process(target=bciPlotFunc, args=(q,))
    p.start()
    

def update():
    global ecgBuffer
    global q
    global heartRate
    global ecgBufy
    global ecgPlot
    global ppgBufy
    global ppgPlot 
    
     
    
    try:
        #print(ecgBufy)
        #print(ecgBuffer[4])
        ecgPlot.clear()
        #heartRate.setText("Heart Rate: {}".format(ecgBuffer[0]))
        #ecgPlot.plot(ecgBuffer[2],ecgBuffer[3] ,pen=None, symbol='o')
        #ecgPlot.plot(ecgBuffer[5])
        ecgPlot.plot(ecgBufy)
    
    except:
        traceback.print_exc()


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
    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: updateInProc(curves))
    timer.start(0)

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
    gsrPlot = pg.PlotWidget(title="Respiration")
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

