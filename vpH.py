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

if __name__ == "__main__":
    vidfile = DEFAULT_FILE #default video file name

    if len(sys.argv) > 1: #if there are arguments
        if sys.argv[1] == "-p" or sys.argv[1] == "--process":
            try:
                vidfile = sys.argv[2]
            except:
                print("error")
                exit()
            msks = bS.selectTubes(vidfile)

            vR.setup(vidfile, msks)
            vR.parse()
            data = np.load('latest.npy')

        if sys.argv[1] == "-r" or sys.argv[1] == "--read":
            try:
                data = np.load(sys.argv[2])
            except:
                data = np.load('latest.npy')


    da = stats.convert_to_hue(data)
    da = stats.remove_outliers(da)
    avg = stats.average_over_axis(da)
    mmf = stats.hueTopH(avg[0])

    #ref = stats.genSideBar(avg)

    fig, ax = plt.subplots()
    x = np.arange(len(mmf))
    #ax.scatter(x, avg[0])
    #plt.imshow(ref, origin='lower', aspect = 20)
    ax.plot(x, mmf)
    ax.set_ylabel("pH")
    ax.set_title("pH change of the test over time")
    plt.show()