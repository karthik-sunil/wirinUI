from UI import *
import matplotlib.animation as anim 
def animateECG(i):
    global ecg
    print("Inside animate")
    pullData = open("eegdata.txt","r").read()
    dataList = pullData.split('\n')
    xList = []
    yList = []
    for eachLine in dataList:
        if len(eachLine)>1:
            x,y = eachLine.split(',')
            xList.append(int(x))
            yList.append(int(y))
    ecg.clear()
    ecg.plot(xList,yList)       