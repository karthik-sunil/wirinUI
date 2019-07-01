import tkinter as tk 
from tkinter import ttk
import matplotlib 
import matplotlib.animation as anim
from matplotlib import style
style.use("ggplot")
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
LARGE_FONT = ("Times", 12)

f1 = Figure(figsize=(5,5), dpi=100)
a1 = f1.add_subplot(111)


f2 = Figure(figsize=(5,5), dpi=100)
a2 = f2.add_subplot(111)

def animateEEG(i):
    pullData = open("eegdata.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xList.append(float(x))
            yList.append(float(y))
    a1.clear()
    a1.plot(xList,yList)
    
def animatePPG(i):
    pullData = open("ppgdata.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xList.append(float(x))
            yList.append(float(y))
    a2.clear()
    a2.plot(xList,yList)

class Plot1(tk.Frame):
    
    def __init__(self,parent):
        
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = "EEG Page", font = LARGE_FONT)
        label.pack(pady=10, padx=10)
        data = tk.Frame(self,width=1000)
        data.pack(side="right")
        label = tk.Label(data, text = "Data", font = LARGE_FONT)      
        label.pack(pady=50, padx=10)
        canvas = FigureCanvasTkAgg(f1,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = False)
        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = False)


class Plot2(tk.Frame):
    
    def __init__(self,parent):
        
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = "PPG Page", font = LARGE_FONT)
        label.pack(pady=10, padx=10)
        data = tk.Frame(self,width=1000)
        data.pack(side="right")
        label = tk.Label(data, text = "Data                         ", font = LARGE_FONT)      
        label.pack(pady=50, padx=10)
        canvas = FigureCanvasTkAgg(f2,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = False)
        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = False)

class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        
        tabControl = ttk.Notebook(self.master)
        #tab1 = ttk.Frame(tabControl)
        tab1 = Plot1(tabControl)
        quitButton = ttk.Button(tab1, text="Quit")
        quitButton.place(x=0,y=0)

        tabControl.add(tab1,text="All Graphs")
        tab2 = Plot2(tabControl)
        tabControl.add(tab2,text="Graph 1")
        tab3 = ttk.Frame(tabControl)
        tabControl.add(tab3,text="Graph 2")

        
        
        
        
        tabControl.pack(expan = 1, fill="both")


root = tk.Tk()

app = Window(root)

root.title("wirin")
ani1 = anim.FuncAnimation(f1,animateEEG,interval=900)
ani2 = anim.FuncAnimation(f2,animatePPG,interval=900)
print(type(root))
root.mainloop()