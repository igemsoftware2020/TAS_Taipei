import numpy as np
import cv2
import threading

vid = None
masks = None
data = None

# At which percentage intervals does the program output its percent completion
PERCENT_NOTIFICATION = 2

_notif = PERCENT_NOTIFICATION / 100

def processFrame(fr):
    global data
    dataList = []
    tube = 0
    # for every tube (mask) that exists...
    for mask in masks:
        fr = cv2.bitwise_and(fr, mask)
        fr = np.ma.masked_equal(fr, [0, 0, 0])
        fr = fr.compressed()
        fr = np.reshape(fr, (-1, 3))
        #print(data.shape)
        dataList.append(fr)
        tube += 1
    return dataList

def setup(file, msks):
    global vid
    global masks
    vid = cv2.VideoCapture(file)
    masks = msks

def parse():
    global data
    total = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    invTotal = 1 / total
    success, frame = vid.read()

    data = []
    while success:
        
        # append the data from the next frame to the data 
        # data.append(processFrame(frame))
        parseThread = threading.Thread(target=(lambda f, d: (d.append(processFrame(f)))), args=(frame.copy(), data))
        parseThread.start()

        if ((len(data) / total) % _notif) < invTotal:
            print(int((len(data) * 100) / total), "% done!")
        success, frame = vid.read()

        parseThread.join()

    data = np.asarray(data)
    data = np.moveaxis(data, 0, 1)
    print("\n (tubes, frames)")
    print(data.shape)

    print("video data successfully parsed and collected!")
    np.save("last.npy", data)

    return data

if __name__ == "__main__":
    vidfile = "data/wave.mp4"

    import boxSelector
    msks = boxSelector.selectTubes(vidfile)

    setup(vidfile, msks)
    parse()