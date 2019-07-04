import pandas  
import time

result = pandas.read_csv("data_1.csv")
l1 = result.values.tolist()
ECG = []
Heart = []


buffer_size1 = 0
buffer_size2 = 0
def ECGFeed():
    count1 = 0
    global ECG
    while count1 < len(l1):
        buffer_size1 = count1%20   
        ECG.append(str(count1) + "," + str(l1[count1][0])+"\n")
        count1 = count1+1
        if (buffer_size1 == 0):
            f1 = open("ECG.txt","a")
            f1.write("".join(ECG))
            ECG = []
            time.sleep(1)
    f1.close() 
def HRFeed():
    count2 = 0
    global Heart
    while count2 < len(l1):
        buffer_size2 = count2%500   
        Heart.append(str(count2) + "," + str(l1[count2][0])+"\n")
        count2 = count2+1
        if (buffer_size2 == 0):
            f2 = open("Heart Rate.txt","a")
            f2.write("".join(Heart))
            Heart = []
            time.sleep(1)
    f2.close()