import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import biosppy

x = pd.read_csv(r"D:\Aniruddh\Nerdy Stuff\WIRIN\Datasets\Data_CSV\data_1.csv",header=None)
ecg = x[1]
fqs = 500  # Sample frequency (Hz)
f0 = 50.0  # Frequency to be removed from signal (Hz)
Q = 0.5  # Quality factor
len_frames = 6


#Wait for the first len_frames seconds
data = []

for i in range(len_frames+1): 
    data = data + list(ecg[i*fqs: (i+1)*fqs])

#Detect R Peaks
r_peaks = biosppy.signals.ecg.ecg(signal=data, sampling_rate=500.0, show = False)  
x_peaks = r_peaks[2]

#Append the y coordinate values of the peaks in a list 
y_peaks = []
for j in x_peaks:
        y_peaks.append(ecg[j])

#Count the number of R peaks in the specified range     
num_peaks = 0
for i in x_peaks:
    if(i in range(0, len_frames*fqs)):
        num_peaks = num_peaks + 1

print(num_peaks*60/(len_frames))

"""
plt.plot(data, color = 'blue')
plt.scatter(x_peaks, y_peaks, color = 'red')
plt.xlim(0,3000)
plt.show()
"""