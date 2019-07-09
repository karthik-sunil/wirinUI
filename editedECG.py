import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal
import numpy as np
import biosppy


class ECG:

    def __init(self):
        
        self.fqs = 500.0  # Sample frequency (Hz)
        self.f0 = 50.0  # Frequency to be removed from signal (Hz)
        self.Q = 0.5  # Quality factor
        self.len_frames = 6
        self.data = []
        
        def analyze(self, data):
            self.data =  self.data[-self.fqs:]
            self.data += (data)
            self.r_peaks = biosppy.signals.ecg.ecg(signal=data, sampling_rate=self.fqs, show = False)
            self.x_peaks = self.r_peaks[2]
            
            self.y_peaks = []
            for k in self.x_peaks:
                self.y_peaks.append(data[k])
            
            self.num_peaks = 0
            for i in self.x_peaks:
                if(i in range(fqs, (len_frames+1)*(fqs))):
                    self.num_peaks = self.num_peaks + 1

            print(self.num_peaks*60/(self.len_frames))
        
        #print(fqs, len_frames*(fqs+1), len_frames, fqs+1)
        
        def plot(self):
            plt.plot(self.data, color = 'blue')
            plt.scatter(self.x_peaks, self.y_peaks, color = 'red')
            #plt.xlim(self.fqs,self.fqs*(self.len_frames+1))
            plt.show()
