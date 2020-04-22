import numpy
import cv2
import boxSelector
from videoReader import parse

if __name__ == "__main__":
    vidfile = "4_20 C-19 Test 3_.MOV"
    parse()
    msks = boxSelector.selectTubes(vidfile)