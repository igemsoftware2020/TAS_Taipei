import numpy as np
import matplotlib.pyplot as plt
import cv2
import boxSelector as bS
import videoReader as vR
import stats
import sys

# run 
#   alias vp=python vpH.py -i
# then
#   vp -p "filename.MOV"

MAX_DEVIATION = 0.1
OFFSET = 5
DEFAULT_FILE = "data/default.mov"
CROP = 0
global data
global size
global process
global vidfile
process = False
size = 1
x = 0


def checkArgs(arg, ind):
    global size
    global process

    if arg == "-p":
        try:
            global vidfile
            vidfile = sys.argv[ind + 1]
        except:
            print("error")
            exit()
        process = True
        

    if arg == "-r":
        try:
            data = np.load(sys.argv[ind + 1])
        except:
            print("error")
            exit()

    if arg == "-sm":
        try:
            size = float(sys.argv[ind+1])
        except:
            size = 1
            print("error")
            exit()

    if arg == "-m":
        try:
            x = int(sys.argv[ind])
        except:
            print("error")
            exit()
      
if __name__ == "__main__":
    global data
    global vidfile
    vidfile = DEFAULT_FILE #default video file name

    for argin in range(len(sys.argv)):
        arg = sys.argv[argin]
        if arg[0] == "-":
            checkArgs(arg, argin)
    
    if process:
        print(vidfile)
        msks = bS.selectTubes(vidfile, size)
        x = 0
        for msk in msks:
            vR.setup(vidfile, np.asarray(msk))
            vR.parse(str(x))
            x+=1


    fig, ax = plt.subplots()
    for i in range(x):
        name = str(i)+'.npy'
        data = np.load(name)
        print(data.shape)

        da = stats.convert_to_hue(data)
        da = stats.remove_outliers(da)
        avg = stats.average_over_axis(da)
        mmf = stats.hueTopH(avg[0])

        #ref = stats.genSideBar(avg)

        x = np.arange(len(mmf))
        #ax.scatter(x, avg[0])
        #plt.imshow(ref, origin='lower', aspect = 20)
        ax.plot(x, mmf)
    ax.set_ylabel("pH")
    ax.set_title("pH change over time")
    plt.show()
    # avg has become an equation of [H+] over time