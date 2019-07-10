import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import biosppy


## x = pd.read_csv(r"D:\Aniruddh\Nerdy Stuff\WIRIN\Datasets\Data_CSV\data_1.csv",header=None)
ecg = x[1]
fqs = 500  # Sample frequency (Hz)
f0 = 50.0  # Frequency to be removed from signal (Hz)
Q = 0.5  # Quality factor
len_frames = 6

#Wait for the first len_frames+2 seconds because peaks in the first and last frames are not detected accurately
data = []
#Append all the elements into 'data'
for pos in range(len_frames+2): 
    data = data + list(ecg[pos*fqs: (pos+1)*fqs])


#Detect R Peaks
r_peaks = biosppy.signals.ecg.ecg(signal=data, sampling_rate=500.0, show = False)
x_peaks = r_peaks[2]

#Append the y coordinate values of the peaks to a list 
y_peaks = []
for j in x_peaks:
        y_peaks.append(ecg[j])

#Count the number of R peaks in the desired range     
num_peaks = 0
for i in x_peaks:
    if(i in range(fqs, (len_frames+1)*(fqs))):
        num_peaks = num_peaks + 1

#Print Heart rate
print(num_peaks*60/(len_frames))


plt.plot(data, color = 'blue')
plt.scatter(x_peaks, y_peaks, color = 'red')
plt.xlim(fqs,fqs*(len_frames+1))
plt.show()


j = 0                   
loop_num = 5

while(j < loop_num):
    for k in range(fqs*(len_frames+1)):
        data[k] = data[k+fqs]
    
    data[-fqs:] = (ecg[(pos+1)*fqs: (pos+2)*fqs])
    pos = pos + 1

    r_peaks = biosppy.signals.ecg.ecg(signal=data, sampling_rate=500.0, show = False)
    x_peaks = r_peaks[2]
    
    y_peaks = []
    for k in x_peaks:
        y_peaks.append(data[k])
    
    num_peaks = 0
    for i in x_peaks:
        if(i in range(fqs, (len_frames+1)*(fqs))):
            num_peaks = num_peaks + 1

    print(num_peaks*60/(len_frames))
    #print(fqs, len_frames*(fqs+1), len_frames, fqs+1)
    
    plt.plot(data, color = 'blue')
    plt.scatter(x_peaks, y_peaks, color = 'red')
    plt.xlim(fqs,fqs*(len_frames+1))
    plt.show()
    
    j = j + 1


class ECG:

    def __init(self):
        
        self.fqs = 500.0  # Sample frequency (Hz)
        self.f0 = 50.0  # Frequency to be removed from signal (Hz)
        self.Q = 0.5  # Quality factor
        self.len_frames = 6
        self.data = []
        
        def analyze(self, data):
            self.data =  self.data[-self.fqs:]
            self.data.append(data)
            r_peaks = biosppy.signals.ecg.ecg(signal=data, sampling_rate=self.fqs, show = False)
            x_peaks = r_peaks[2]
            
            y_peaks = []
            for k in x_peaks:
                y_peaks.append(data[k])
            
            num_peaks = 0
            for i in x_peaks:
                if(i in range(fqs, (len_frames+1)*(fqs))):
                    num_peaks = num_peaks + 1

            print(num_peaks*60/(len_frames))
        
        #print(fqs, len_frames*(fqs+1), len_frames, fqs+1)
        
        def plot(self):
            plt.plot(self.data, color = 'blue')
            plt.scatter(self.x_peaks, self.y_peaks, color = 'red')
            #plt.xlim(self.fqs,self.fqs*(self.len_frames+1))
            plt.show()
