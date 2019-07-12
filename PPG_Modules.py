import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import signal

def filter_signal(sig, N, Wn):
   # Designing a Buuterwoth filter
    N  = 4    # Filter order
    Wn = 0.1  # Cutoff frequency
    B, A = signal.butter(N, Wn, output='ba')    
    smooth_data = signal.filtfilt(B, A, sig) # Smoothen the signal
    
    return(smooth_data)
    
def roll_mean(sig, fs, num_roll, len_frames):
    rolling_mean = [0]*(num_roll-1)     # Array that stores the rolling mean values
    
    greater = []    # Used to calculate rolling mean
    x_peaks = []    # X coordinates of peaks
    y_peaks = []    # Y coordinates of peaks
    base = 0
    for i in range(num_roll, fs*(len_frames+2)):
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
        
    return(rolling_mean, x_peaks, y_peaks)

def plot_data(smooth_data, rolling_mean, x_peaks, y_peaks, len_frames, fs):
    plt.plot(smooth_data, color = 'blue')
    plt.plot(rolling_mean, color = 'green')
    plt.scatter(x_peaks, y_peaks, color = 'red')
    plt.xlim(fs, (1 + len_frames)*fs)
    plt.grid()
    plt.show()

def calc_hr(x_peaks, len_frames):
    beats = 0
    for i in x_peaks:
        if(i in range(fs, fs*(len_frames+1))):
            beats = beats + 1

    return(60*(beats/len_frames))

def shift_data_left(ppg, fs):
    for i in range(len(ppg_val)-fs):
        ppg_val[i] = ppg_val[i+fs]
    return(ppg_val)

def new_values(ppg_val, fs, new_data):
    ppg_val[-fs:] = new_data
    return(ppg_val)
    
def store_previous_rolling_mean(smooth_data, fs, num_roll):
    prev_roll_mean = smooth_data[(j+1)*fs-num_roll:(j+1)*fs]
    return(prev_roll_mean)