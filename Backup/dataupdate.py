import time
import math
import random
i = 0
while(True):
    f = open("eegdata.txt","a")
    f.write("{},{}\n".format(i, math.sin(i)))
    f.close()    
    time.sleep(0.001)
    i = i + 1
