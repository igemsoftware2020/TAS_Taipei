import numpy as np
import cv2
import matplotlib.pyplot as plt

MAX_DEVIATION = 0.1
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

def genSideBar(avg):
    rnge = int(np.amax(avg[0])+5)
    print(rnge)
    h = (np.arange(rnge))#np.flip
    h -= OFFSET
    h[h<=0] += 180
    s = [255] * rnge
    v = [255] * rnge
    ref = np.stack((h, s, v), 1)
    ref = np.asarray([ref] * 30, np.uint8)
    ref = np.swapaxes(ref, 1, 0)
    ref = cv2.cvtColor(ref, cv2.COLOR_HSV2RGB)
    return ref
    
if __name__ == "__main__":
    da = np.load("latest.npy")
    da = convert_to_hue(da)
    da = remove_outliers(da)
    avg = average_over_axis(da)

    ref = genSideBar(avg)

    fig, ax = plt.subplots()
    x = np.arange(len(avg[0]))
    #ax.scatter(x, avg[0])
    plt.imshow(ref, origin='lower', aspect = 20)
    print(x[-1])
    ax.plot(x, avg[0])
    plt.show()
