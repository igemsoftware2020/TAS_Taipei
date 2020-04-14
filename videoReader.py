import numpy as np
import cv2

vid = None

def processFrame(frame, n):
    return

def openFile():
    global vid
    vid = cv2.VideoCapture("data/read.MOV")

def readFile():
    success, frame = vid.read()
    frameIter = 0
    while success:  
        processFrame(frame, frameIter)
        success, frame = vid.read()

