import time
import math
import random
i = 0
while(True):
    f = open("eegdata.txt","a")
    f.write("{},{}\n".format(i,i*random.randint(1,10) + 5))
    f.close()    
    time.sleep(1)
    i = i + 1
