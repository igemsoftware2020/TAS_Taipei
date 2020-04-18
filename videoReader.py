import numpy as np
import cv2

vid = None
masks = None
data = []

def processFrame(frame, n):
    tube = 0
    # for every tube (mask) that exists...
    for mask in masks:
        # for each mask array, add a new frame slot
        data[tube].append([])
        y = 0
        for column in mask:
            x = 0
            for pixel in column:
                if pixel == 255:
                    print("pix")
                    print(y," ", x)
                    print(frame[y][x])
                    data[tube][n].append(frame[y][x])
                x += 1
            y += 1
        tube += 1

def setup(file, msks):
    global vid
    global masks
    vid = cv2.VideoCapture(file)
    masks = msks
    for mask in masks:
        data.append([])

def parse():
    success, frame = vid.read()
    frameIter = 0
    while success:  
        processFrame(frame, frameIter)
        success, frame = vid.read()
        frameIter += 1

if __name__ == "__main__":
    vidfile = "data/single.mov"

    import boxSelector
    msks = boxSelector.selectTubes(vidfile)

    setup(vidfile, msks)
    parse()