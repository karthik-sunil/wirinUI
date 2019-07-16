from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas(FigureCanvas):

    def __init__( self ):
        self.fig = Figure()
        self.ax = self.fig.add_subplot( 111 )

        FigureCanvas.__init__( self, self.fig )
        FigureCanvas.setSizePolicy( self, QSizePolicy.Expanding,QSizePolicy.Expanding )
        FigureCanvas.updateGeometry( self )


class matplotlibWidget(QWidget):

    def __init__( self, parent = None ):
        QWidget.__init__( self, parent )
        self.canvas = MplCanvas() #create canvas that will hold our plot
        self.navi_toolbar = NavigationToolbar(self.canvas, self) #createa navigation toolbar for our plot canvas

        self.vbl = QVBoxLayout()
        self.vbl.addWidget( self.canvas )
        self.vbl.addWidget(self.navi_toolbar)
        self.setLayout( self.vbl )