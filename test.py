import tkinter as tk
from tkinter import ttk

class Window(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        
        tabControl = ttk.Notebook(self.master)
        tab1 = ttk.Frame(tabControl)
        quitButton = ttk.Button(tab1, text="Quit")
        quitButton.place(x=0,y=0)

        tabControl.add(tab1,text="All Graphs")
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2,text="Graph 1")
        tab3 = ttk.Frame(tabControl)
        tabControl.add(tab3,text="Graph 2")

        
        
        
        
        tabControl.pack(expan = 1, fill="both")


root = tk.Tk()
 
root.geometry("500x500")
app = Window(root)
print(type(root))
root.mainloop()