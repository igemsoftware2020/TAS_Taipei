import numpy as np
import cv2

vid = None
masks = None
data = np.asarray([])

def processFrame(frame, n):
    global data
    tube = 0
    print(n)
    # for every tube (mask) that exists...
    for mask in masks:
        fr = frame.copy()
#data = np.append(data, np.asarray(frame[column][pixel]))
        tube += 1

def setup(file, msks):
    global vid
    global masks
    vid = cv2.VideoCapture(file)
    masks = msks

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