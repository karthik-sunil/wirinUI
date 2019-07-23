import pandas as pd
import biosppy
import matplotlib.pyplot as plt
def f(datax,datay, sampling_rate):
    
    returns = biosppy.signals.ecg.ecg(signal=datay, sampling_rate=sampling_rate, show = False)
    x_peaks = returns['rpeaks']
    heartRateBiosppy = returns['heart_rate']
    y_peaks = []
    
    for j in x_peaks:
        y_peaks.append(datay[j])
    num_peaks = len(x_peaks)
    timeData = len(datay)/sampling_rate
    heartRate = 60*num_peaks / timeData
    
    # plt.plot(data, color = 'blue')
    # plt.scatter(x_peaks, y_peaks, color = 'red')
    # plt.show()
    #print(returns)
    return (heartRate,heartRateBiosppy, x_peaks,y_peaks,datax,datay)

if __name__ == "__main__":
    x = pd.read_csv(r"E:\\Coding\\Wirin\\wirinUI\\data_1.csv",header=None)[1]
    
    print(f(x[:4000],500.0))