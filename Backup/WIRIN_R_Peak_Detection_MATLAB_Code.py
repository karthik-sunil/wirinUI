import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
#import numpy as np

x = pd.read_csv(r"D:\Aniruddh\Nerdy Stuff\WIRIN\Datasets\Data_CSV\data_7.csv", header = None)
ecg = x[1]
fqs = 500.0  # Sample frequency (Hz)
f0 = 50.0  # Frequency to be removed from signal (Hz)
Q = 2  # Quality factor
# Design notch filter
nyq = 0.5 * fqs
lowcut = 0.7/nyq
highcut = 50/nyq
b, a = signal.iirnotch(f0, Q, fqs)
filtered = signal.filtfilt(b,a,ecg)
y = sp.fft(filtered)
b1, a1 = signal.butter(4,[lowcut,highcut],btype = 'bandpass')
bandpassed = signal.filtfilt(b1,a1,filtered)

bandpassed[0:5] = 0
diff_1 = [] # First derivative
diff_2 = [] # Second derivative

for i in range(5, len(bandpassed)):
    diff_1.append(abs(bandpassed[i] - bandpassed[i-2]))
    diff_2.append(abs(bandpassed[i] - 2*bandpassed[i-2] + bandpassed[i-4]))

res = [] # Form resultant array from the derivatives
for i in range(len(diff_1)):
    res.append(1.3*diff_1[i]+1.1*diff_2[i])


thresh_val = 0.03 # Threshold value 

thresh = [] # Contains 1 when the resultant signal crosses the threshold value
for i in res:
    if(i > thresh_val):
        thresh.append(1)
    else:
        thresh.append(0)

flag = [False]*len(thresh) # Get the starting and ending points of the QRS complex

for i in range(0, len(thresh)-6):
    s = sum(thresh[i:i+6])
    if(s >= 4):
        flag[i] = True

t_lim = int(0.2*fqs)  # Assume the width of the QRS complex is one fifth the width of the heart beat

i = 0

r_peak = [] # List of R peaks 

while(i < len(thresh)-100):
    if(flag[i]):        
        mID = list(bandpassed[i: i+(t_lim)]).index(max((bandpassed[i: i+(t_lim)]))) # Store the x coordinates of the R Peaks
        r_peak.append(mID+i)
        i += t_lim        
    
    else:
        i += 1

plt.plot(bandpassed, color='blue')
plt.scatter(r_peak, bandpassed[r_peak], color='red')
plt.xlim(15000, 20000)
plt.grid()
plt.show()

"""
plt.plot(res, color='orange')
plt.xlim(15000, 20000)
plt.grid()
plt.show()
"""