import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib import figure

MAX_DEVIATION = 1
OFFSET = 5

def average_over_axis(data):
    data = np.mean(data, axis=-1)
    return data
    #np.reshape(data, (1, -1))

def convert_to_hue(data):
    t = 0
    for tube in data:
        tube = cv2.cvtColor(tube, cv2.COLOR_BGR2HSV)
        data[t] = tube
        t+=1
    #print(data)
    data = np.delete(data, [1, 2], -1)
    #print(np.prod(data, axis=-1, ))
    data = np.squeeze(data, axis=-1)
    data = np.add(data, OFFSET)
    data[data > 180] -= 180
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
    return new_data 

if __name__ == "__main__":
    da = np.load("C1.npy")
    da = convert_to_hue(da)
    da = remove_outliers(da)
    avg = average_over_axis(da)

    da2 = np.load("C3.npy")
    da2 = convert_to_hue(da2)
    da2 = remove_outliers(da2)
    avg2 = average_over_axis(da2)

    da3 = np.load("D2.npy")
    da3 = convert_to_hue(da3)
    da3 = remove_outliers(da3)
    avg3 = average_over_axis(da3)

    da4 = np.load("E1.npy")
    da4 = convert_to_hue(da4)
    da4 = remove_outliers(da4)
    avg4 = average_over_axis(da4)

    nc = np.load("NC.npy")
    nc = convert_to_hue(nc)
    nc = remove_outliers(nc)
    avg5 = average_over_axis(nc)

    '''rnge = int(np.amax(avg[0]) + 5)
    print(rnge)
    h = (np.arange(rnge))#np.flip
    h -= OFFSET
    h[h<=0] += 180
    s = [255] * rnge
    v = [255] * rnge
    ref = np.stack((h, s, v), 1)
    ref = np.asarray([ref] * 10, np.uint8)
    ref = np.swapaxes(ref, 1, 0)
    ref = cv2.cvtColor(ref, cv2.COLOR_HSV2RGB)'''

    fig, ax = plt.subplots()
    x = np.arange(len(avg[0])) * (62399/56700)
    #ax.scatter(x, avg[0])
    # plt.imshow(ref, origin='lower', aspect = 20)
    plt.ylabel("pH")
    plt.xlabel("Time (Minutes)")
    ax.plot(x, np.log(((1/avg[0])-0.100867)/0.00000572328)/1.32139, label = "C1")
    '''ax.plot(x, avg2[0], label = "C3")
    ax.plot(x, avg3[0], label = "D2")
    ax.plot(x, avg4[0], label = "E1")
    ax.plot(x, avg5[0], label = "Negative Control")'''
    plt.legend(loc = 'lower right')
    plt.tight_layout()
    # plt.xlim(0, max)
    # plt.xticks(np.arange(min(x), max(x), 100))
    plt.show()