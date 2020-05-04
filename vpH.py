import numpy as np
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
    vidfile = DEFAULT_FILE

    if len(sys.argv) > 2:
        if sys.argv[1] == "-p" or sys.argv[1] == "--process":
            vidfile = sys.argv[2]

            msks = bS.selectTubes(vidfile)

            vR.setup(vidfile, msks)
            vR.parse()
            
        if sys.argv[1] == "-r" or sys.argv[1] == "--read":
            data = np.load(sys.argv[2])
    else:
        data = np.load('lastest.npy')


    da = stats.convert_to_hue(data)
    da = stats.remove_outliers(da)
    avg = stats.average_over_axis(da)

    ref = stats.genSideBar(avg)

    fig, ax = plt.subplots()
    x = np.arange(len(avg[0]))
    #ax.scatter(x, avg[0])
    plt.imshow(ref, origin='lower', aspect = 20)
    ax.plot(x, avg[0])
    plt.show()