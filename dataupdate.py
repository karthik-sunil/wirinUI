import time
import math

i = 0
while(True):
    f = open("eegdata.txt","a")
    f.write("{},{}\n".format(i, pow(2,i)))
    f.close()    
    time.sleep(1)
    i = i + 1
