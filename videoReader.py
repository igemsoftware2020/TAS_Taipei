import numpy as np
import cv2

vid = None
masks = None
data = None

PERCENT_NOTIFICATION = 2

_notif = PERCENT_NOTIFICATION / 100

def processFrame(frame):
    global data
    dataList = []
    tube = 0
    # for every tube (mask) that exists...
    for mask in masks:
        fr = frame.copy()
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
        if ((len(data) / total) % _notif) < invTotal:
            print(int((len(data) * 100) / total), "% done!")
        data.append(processFrame(frame))
        success, frame = vid.read()
    data = np.asarray(data)
    data = np.moveaxis(data, 0, 1)
    print("\n (tubes, frames)")
    print(data.shape)

    print("video data successfully parsed and collected!")

if __name__ == "__main__":
    vidfile = "data/single.mov"

    import boxSelector
    msks = boxSelector.selectTubes(vidfile)

    setup(vidfile, msks)
    parse()