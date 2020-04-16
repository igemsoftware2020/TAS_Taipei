import numpy as np
import cv2

vid = None

def processFrame(frame, n):
    return
    
def openFile(file):
    global vid
    vid = cv2.VideoCapture(file)

def readFile():
    success, frame = vid.read()
    frameIter = 0
    while success:  
        processFrame(frame, frameIter)
        success, frame = vid.read()
        frameIter += 1

if __name__ == "__main__":
    openFile("data/single.mov")
    readFile()