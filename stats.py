import numpy as np
import cv2

def convert_to_hue(data):
    t = 0
    for tube in data:
        tube = cv2.cvtColor(tube, cv2.COLOR_BGR2HSV)
        data[t] = tube
        t+=1
    data = np.delete(data, [1,2], 3)
    return data

def remove_outliers(data):
    data = np.sort(data, -1, 'quicksort')
    print(data)

if __name__ == "__main__":
    da = np.load("last.npy")
    da = convert_to_hue(da)
    da = remove_outliers(da)