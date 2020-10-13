import numpy as np
import cv2
import threading

vid = None
masks = []
data = None

# At which percentage intervals does the program output its percent completion
PERCENT_NOTIFICATION = 5

_notif = PERCENT_NOTIFICATION / 100

def processFrame(fr):
    dataList = []
    tube = 0
    # for every tube (mask) that exists...
    for mask in masks:
        fr = cv2.bitwise_and(fr, mask)
        fr = np.ma.masked_equal(fr, [0,0,0])
        fr = fr.compressed()
        fr = fr.reshape(-1,3)
        dataList.append(fr)
        tube += 1
        #cv2.imshow("aa", mask)
        #cv2.waitKey(0)
        continue
    return dataList

def setup(file, msks):
    global vid
    global masks
    vid = cv2.VideoCapture(file)
    masks = msks

def parse():
    parse('latest')

def parse(st):
    global data
    total = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    invTotal = 1 / total
    success, frame = vid.read()

    data = []
    while success:
        ff = frame.copy()
        # append the data from the next frame to the data 
        #data.append(processFrame(frame))

        #data.append(processFrame(frame))
        
        parseThread = threading.Thread(target=(lambda f, d: 
            (d.append(processFrame(f)))), args=(ff, data))
        parseThread.start()
        
        if ((len(data) / total) % _notif) < invTotal:
            print(int((len(data) * 100) / total), "% done!")
        success, frame = vid.read()

        parseThread.join()
    print("100% done!")

    data = np.asarray(data)
    data = np.moveaxis(data, 0, 1)
    print("\n(tubes, frames, pixels, channels)")
    print(data.shape)

    print("video data successfully parsed and collected!")
    name = st + ".npy"
    np.save(name, data)

    return data

if __name__ == "__main__":
    vidfile = "data/def.mov"

    import boxSelector
    msks = boxSelector.selectTubes(vidfile)

    setup(vidfile, msks)
    parse()