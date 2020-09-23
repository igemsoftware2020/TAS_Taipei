import numpy as np
import cv2
import matplotlib.pyplot as plt

MAX_DEVIATION = 1000 # 0.1
OFFSET = 20 # Adjust the offset to tune for specific indicators
# A vector offset would be more universal, but a constant offset is good enough for phenol red

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
    data[data >= 180] -= 180
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
    rnge = int(np.amax(avg[0])+5) # 5 is an arbitrary constant just to make the graph look nicer
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

def hueTopH(hue):
    hue = hue / 5
    conversion = np.reciprocal(hue)
    conversion = conversion * 163864
    conversion = conversion - 16635.6
    conversion = np.log(conversion)
    pH = conversion * 0.768933
    return pH

if __name__ == "__main__":
    da = np.load("latest.npy")
    da = convert_to_hue(da)
    da = remove_outliers(da)
    avg = average_over_axis(da)


    x = np.arange(len(avg[0]))
    fig, ax = plt.subplots()
    #ax.scatter(x, avg[0])
    ref = genSideBar(avg)
    plt.imshow(ref, origin='lower', aspect = 20)
    ax.plot(x, avg[0])
    plt.show()

'''
x = np.arange(len(avg[0])) * (1290.67/606) # multiply by frame to time conversion ratio
    fig, ax = plt.subplots()
    # ax.scatter(x, avg[0])
    # ref = genSideBar(avg)
    # plt.imshow(ref, origin='lower', aspect = 20)
    ax.plot(x, hueTopH(avg[0]), label = "nC19")
    ax.plot(x, hueTopH(avg2[0]), label = "pC19")
    ax.plot(x, hueTopH(navg[0]), label = "nNC")
    ax.plot(x, hueTopH(navg2[0]), label = "pNC")
    ax.plot(x, hueTopH(navg3[0]), label = "NC")
    plt.ylabel("pH")
    plt.xlabel("Time (Minutes)")
    plt.legend(loc = 'upper right')
    plt.tight_layout
    plt.show()
    # np.savetxt('7_28_C19_nM.csv', hueTopH(avg[0]), delimiter='.\n')
'''