
import tkinter as tk 
from tkinter import ttk
import matplotlib 
import pandas as pd
import numpy as np 
import os 
import matplotlib.animation as anim
from matplotlib import style
style.use("ggplot")
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
LARGE_FONT = ("Times", 12)

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)



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


class StartPage(tk.Frame):
    
    def __init__(self,parent,controller, obj):
        
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = "Start Page", font = LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text = "Page One", command = lambda: controller.show_frame(PageOne))
        button1.pack()
        button2 = ttk.Button(self, text = "View Heart Rate", command = lambda: controller.show_frame(Plot1))
        button2.pack()
        button3 = ttk.Button(self, text = "View ECG Plot", command = lambda: controller.show_frame(Plot2))
        button3.pack()
        


    
   
class PageOne(tk.Frame):
    
    def __init__(self,parent,controller,obj):
        
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = "Page One", font = LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text = "Back", command = lambda: controller.show_frame(StartPage))
        button1.pack()

class Plot1(tk.Frame):
    
    def __init__(self,parent,controller, obj):
        
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = "Heart Rate", font = LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text = "Back", command = lambda: controller.show_frame(StartPage))
        button1.pack()
        canvas = FigureCanvasTkAgg(f,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        button2 = ttk.Button(self, text = "Close", command = controller.destroy) 
        button2.pack()
      

class Plot2(tk.Frame):
    
    def __init__(self,parent,controller, obj):
        
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text = "ECG Plot", font = LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text = "Back", command = lambda: controller.show_frame(StartPage))
        button1.pack()
        canvas = FigureCanvasTkAgg(f,self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        toolbar = NavigationToolbar2Tk(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand = True)
        button2 = ttk.Button(self, text = "Close", command = controller.destroy()) 
        button2.pack()
    
  
class NewClass(tk.Tk):
    
    def __init__(self):
        
        obj = tk.Tk.__init__(self)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, Plot1,Plot2):
            frame = F(container,self, obj)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky = "nsew")
        self.show_frame(StartPage)
    def show_frame(self, cont):
        
        frame = self.frames[cont]
        frame.tkraise()
  
    def close(self):
        self.destroy()

app = NewClass()
ani = anim.FuncAnimation(f,animate,interval=1000)
app.mainloop()
