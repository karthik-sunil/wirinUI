import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import signal

dataset = pd.read_csv(r"D:\Aniruddh\Nerdy Stuff\WIRIN\Datasets\Data_CSV\data_1.csv", header = None)
ppg = dataset[0]

# First, design the Buterworth filter
N  = 4    # Filter order
Wn = 0.1  # Cutoff frequency
B, A = signal.butter(N, Wn, output='ba')

fs = 500          # Sampling Frequency(dynamic variable)
num_roll = 275    # Number of rolling mean indices(dynamic variable)
len_frames = 6    # Length of the window from which the heart rate is calculated

rolling_mean = [0]*(num_roll-1)     # Array that stores the rolling mean values

greater = []    # Used to calculate rolling mean
x_peaks = []    # X coordinates of peaks
y_peaks = []    # Y coordinates of peaks
base = 0

# Take data for len_frames+2 seconds
ppg_val = []
for i in range(len_frames+2):
    ppg_val = ppg_val + list(ppg[i*fs:(i+1)*fs])

for i in range(num_roll, fs*(len_frames+2)):
    smooth_data = signal.filtfilt(B,A, ppg_val) # Smoothen the signal
    # Rolling mean calculation
    rolling_mean.append(sum(smooth_data[i-num_roll:i])/(num_roll))
    if(rolling_mean[i-1] < smooth_data[i-1]):
        if(greater == []):
            base = i-1
        greater.append(smooth_data[i-1])
        
    else:
        if(greater == []):
            continue
        else:
            x_peaks.append(base+greater.index(max(greater)))
            y_peaks.append(max(greater))            
            greater = []

# Calculate the number of beats in the window
beats = 0
for i in x_peaks:
    if(i in range(0, fs*len_frames)):
        beats = beats + 1

# Calculate heart beat
print(60*(beats/len_frames))

plt.plot(smooth_data, color = 'blue')
plt.plot(rolling_mean, color = 'green')
plt.scatter(x_peaks, y_peaks, color = 'red')
plt.xlim(500, 3500)
plt.show()

j = 0
loop_num = 5      # Number of times the while loop has to run
frame_pos = len_frames + 2

while(j < loop_num):
    prev_roll_mean = smooth_data[(j+1)*fs-num_roll:(j+1)*fs] # Store the last fs data points from the first frame ()
    
    # Shift data to the left
    for i in range(len(ppg_val)-fs):
        ppg_val[i] = ppg_val[i+fs]
    
    # Update the last few values
    ppg_val[-fs:] = ppg[fs*(frame_pos): fs*(frame_pos+1)]
    frame_pos = frame_pos + 1
    
    greater = []    # Used to calculate rolling mean
    x_peaks = []    # X coordinates of peaks     
    y_peaks = []    # Y coordinates of peaks
    rolling_mean = [0]*(num_roll-1)     # Array that stores the rolling mean values
    
    for i in range(num_roll, fs*(len_frames+2)):
        smooth_data = signal.filtfilt(B,A, ppg_val) #Smoothen the signal
        # Rollong mean
        rolling_mean.append(sum(smooth_data[i-num_roll:i])/(num_roll))
        if(rolling_mean[i-1] < smooth_data[i-1]):
            if(greater == []):
                base = i-1
            greater.append(smooth_data[i-1])
            
        else:
            if(greater == []):
                continue
            else:
                x_peaks.append(base+greater.index(max(greater)))
                y_peaks.append(max(greater))            
                greater = []
    
    # Calculate the number of beats in the window
    beats = 0
    for k in x_peaks:
        if(k in range(0, fs*len_frames)):
            beats = beats + 1
    print(x_peaks)
    
    #Calculate the heart beat
    print(60*(beats/len_frames))
    
    j = j + 1
    
    # Plot the signals
    plt.plot(smooth_data, color = 'blue')
    plt.plot(rolling_mean, color = 'green')
    plt.scatter(x_peaks, y_peaks, color = 'red')
    plt.grid(True)
    plt.xlim(500, 3500)
    plt.show()