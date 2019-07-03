import math
import subprocess
import sys
import threading
import time
import tkinter as tk
from tkinter import ttk

import matplotlib
import matplotlib.animation as anim
from matplotlib import style
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
from matplotlib.figure import Figure



style.use("ggplot")
matplotlib.use("TkAgg")
LARGE_FONT = ("Times", 12)

f1 = Figure(figsize=(5,5), dpi=100)
a1 = f1.add_subplot(111)


f2 = Figure(figsize=(5,5), dpi=100)
a2 = f2.add_subplot(111)

def animateEEG(i):
    print("Inside animate")
    pullData = open("eegdata.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    

    for eachLine in dataList:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xList.append(float(x))
            yList.append(float(y))
    xList = xList[-20:]
    yList = yList[-20:]
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
        
        outerani = self.animate()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = False)
        
    def animate(self):
        print("Calling ani1")
        self.ani1 = anim.FuncAnimation(f1,self.animateEEG, interval=1000)
        return self.ani1

            
    def animateEEG(self,i):
        print("Inside animate")
        pullData = open("eegdata.txt","r").read()
        dataList = pullData.split('\n')
        xList = []
        yList = []
        

        for eachLine in dataList:
            if len(eachLine)>1:
                x,y = eachLine.split(',')
                xList.append(float(x))
                yList.append(float(y))
        xList = xList[-20:]
        yList = yList[-20:]
        a1.clear()
        a1.plot(xList,yList)
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
        
        menubar = tk.Menu(self.master)
        menubar.add_command(label="Quit")
        self.master.config(menu = menubar)
        
        self.thread = updateData(self)
        self.thread.start()
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)
        
        
        
    def on_close(self):
        #print("Closing")
        self.thread.stop()
        self.master.destroy()
        



class updateData(threading.Thread):
    
    def __init__(self,wnd):
        threading.Thread.__init__(self)
        self.wnd = wnd
        self.is_quit = False
        

    def stop(self):
        self.is_quit = True

    def run(self):
        i = 0
        try:    
            while not self.is_quit:
                #print("OK")
                f = open("eegdata.txt","a")
                f.write("{},{}\n".format(i, math.sin(i)))
                f.close()    
                time.sleep(0.01)
                i = i + 1
        except:
            print("Application terminated")


if __name__ == "__main__":
    root = tk.Tk()
    app = Window(root)
    root.mainloop()