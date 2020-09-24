import numpy as np
import cv2
import threading

vid = None
mask_indices = []
data = None

# At which percentage intervals does the program output its percent completion
PERCENT_NOTIFICATION = 10

_notif = PERCENT_NOTIFICATION / 100

def processFrame(fr):
    dataList = []
    tube = 0
    # for every tube (mask) that exists...
    for indices in mask_indices:
        fr = fr[indices]
        #print(fr)
        try:
            fr = np.reshape(fr, (-1, 3))
        except:
            print(fr.shape)
            print('indicies', indices[0].shape)
            pass
        #print(fr.shape)
            
        dataList.append(fr)
        tube += 1
    return dataList

def setup(file, msks):
    global vid
    global mask_indices
    vid = cv2.VideoCapture(file)
    masks = msks
    for mask in masks:
        indices = np.nonzero(mask)
        mask_indices.append(indices)


def parse():
    global data
    total = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    invTotal = 1 / total
    success, frame = vid.read()

    data = []
    while success:
        
        # append the data from the next frame to the data 
        # data.append(processFrame(frame))
        fr = frame.copy()
        
        parseThread = threading.Thread(target=(lambda f, d: (d.append(processFrame(f)))), args=(fr, data))
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
    np.save("166fM.npy", data)

    return data

if __name__ == "__main__":
    vidfile = "data/9-4-166pm-0166pm-00166pm-166fm-166am_cropped.mov"

    import boxSelector
    msks = boxSelector.selectTubes(vidfile)

    setup(vidfile, msks)
    parse()