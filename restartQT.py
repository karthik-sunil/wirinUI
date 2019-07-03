from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

import serial

def findComPorts(menu):
    menu = menu
    print("Hello")
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    result = []
    print(menu)
    for port in ports:
        
        try:
            s = serial.Serial(port)
            s.close()
            print(type(port))
            result.append(port)
            
        except (OSError, serial.SerialException):
            pass
       
    if len(result) == 0:
        menu.addAction("NO PORTS")
    for r in result:
        menu.addAction(r)


app =QApplication(sys.argv)
window = QMainWindow()
window.setGeometry(50,50,900,500)
mainLayout = QVBoxLayout()
topBar = QToolBar()
window.addToolBar(topBar)

comPorts = QToolButton()
comPorts.setText("COM")
menu = QMenu()
findComPorts(menu)

comPorts.setMenu(menu)
comPorts.setPopupMode(QToolButton.InstantPopup)
topBar.addWidget(comPorts)

window.setLayout(mainLayout)
window.show()
sys.exit(app.exec_())