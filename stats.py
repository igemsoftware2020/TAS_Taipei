import numpy as np
import cv2
import matplotlib.pyplot as plt

MAX_DEVIATION = 0.2

def average_over_axis(data):
    return np.mean(data, axis=2)

def convert_to_hue(data):
    t = 0
    for tube in data:
        tube = cv2.cvtColor(tube, cv2.COLOR_BGR2HSV)
        data[t] = tube
        t+=1
    data = np.delete(data, [1,2], 3)
    data = np.squeeze(data, 3)
    return data    

def remove_outliers(data):
    data = np.sort(data, -1, 'quicksort')
    for tube in range(len(data)):
        fr = 0
        sample = data[tube][fr].copy()
        m = np.mean(sample)
        std = np.std(sample)
        mask = [abs(sample - m) < MAX_DEVIATION * std]
        mask = mask * len(data[tube])
        mask = np.asarray(mask)
        new_data = data[tube][mask]
        new_data = np.reshape(new_data, (len(data), len(data[tube]), -1))
    return data 
    
if __name__ == "__main__":
    da = np.load("last.npy")
    da = convert_to_hue(da)
    da = remove_outliers(da)
    avg = average_over_axis(da)
    fig, ax = plt.subplots()
    x = np.arange(len(avg[0]))
    ax.plot(x, avg[0])
    plt.show()
