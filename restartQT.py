from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from functools import partial
import serial
 

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
    #menu.clear()

    print(a.text())
    
    findComPorts(menu)
   


app = QApplication(sys.argv)
window = QMainWindow()
window.setGeometry(50,50,900,500)
window.setWindowTitle("WirinUI")

mainLayout = QVBoxLayout()
topBar = QToolBar()
window.addToolBar(topBar)

comPorts = QToolButton()
comPorts.setText("COM")

menu = QMenu()
findComPorts(menu)
menu.triggered.connect(partial(setComPort, menu))
comPorts.setMenu(menu)

comPorts.setPopupMode(QToolButton.InstantPopup)
topBar.addWidget(comPorts)

window.setLayout(mainLayout)
window.show()
sys.exit(app.exec_())