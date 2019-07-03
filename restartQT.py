from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys



app =QApplication(sys.argv)
window = QMainWindow()
window.setGeometry(50,50,900,500)
mainLayout = QVBoxLayout()
topBar = window.addToolBar("File")
new = QAction(QIcon(""),"new",window)


viewStatAct = QAction('View statusbar', window, checkable=True)
viewStatAct.setStatusTip('View statusbar')
viewStatAct.setChecked(True)

topBar.addAction(new)

window.setLayout(mainLayout)
window.show()
sys.exit(app.exec_())