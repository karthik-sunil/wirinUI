import pandas 
import time 
result = pandas.read_csv("data_1.csv")
l1 = result.values.tolist()
ECG = []
Heart = []
i1 = 0
i2 = 0
j1 = 0
j2 = 0
while i1 < len(l1):
    j1 = i1%20   
    ECG.append(str(i1) + "," + str(l1[i1][0])+"\n")
    i1 = i1+1
    if (j1 == 0):
        f1 = open("ECG.txt","a")
        f1.write("".join(ECG))
        ECG = []
        time.sleep(1)
f1.close() 
while i2 < len(l1):
    j2 = i2%20   
    Heart.append(str(i2) + "," + str(l1[i2][0])+"\n")
    i2 = i2+1
    if (j2 == 0):
        f2 = open("Heart Rate.txt","a")
        f2.write("".join(Heart))
        Heart = []
        time.sleep(1)
f2.close()