import numpy as np
import cv2

vid = None
masks = None
data = []

def processFrame(frame, n):
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
    dataList = np.reshape(dataList, (-1, 1))
    data = np.append(data, dataList, axis=1)
    print(data.shape)

def setup(file, msks):
    global vid
    global masks
    global data
    vid = cv2.VideoCapture(file)
    masks = msks
    for m in masks:
        data.append([None])
    data = np.asarray(data)

def parse():
    success, frame = vid.read()
    frameIter = 0
    while success:  
        processFrame(frame, frameIter)
        success, frame = vid.read()
        frameIter += 1
    print("video data successfully parsed and collected!")

if __name__ == "__main__":
    vidfile = "data/single.mov"

    import boxSelector
    msks = boxSelector.selectTubes(vidfile)

    setup(vidfile, msks)
    parse()