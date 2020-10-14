import numpy as np
import cv2
import threading

vid = None
mask_indices = []
data = None

# At which percentage intervals does the program output its percent completion
PERCENT_NOTIFICATION = 2

_notif = PERCENT_NOTIFICATION / 100

def processFrame(fr):
    dataList = []
    tube = 0
    # for every tube (mask) that exists...
    for indices in mask_indices:
        fr = fr[indices]
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

def setup(file, msk):
    global vid
    global mask_indices
    vid = cv2.VideoCapture(file)
    vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
    indices = np.nonzero(msk)
    mask_indices = []
    mask_indices.append(indices)


def parse(name):
    global data
    data = None
    total = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    invTotal = 1 / total
    vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
    success, frame = vid.read()

    data = []
    while success:
        
        # append the da
        # ta from the next frame to the data 
        # data.append(processFrame(frame))
        fr = frame.copy()
        
        parseThread = threading.Thread(target=(lambda f, d: (d.append(processFrame(f)))), args=(fr, data))
        parseThread.start()

        if ((len(data) / total) % _notif) < invTotal:
            print(int((len(data) * 100) / total), "% done!")
        success, frame = vid.read()

        parseThread.join()
    vid.release()
    print("100% done!")

    data = np.asarray(data)
    data = np.moveaxis(data, 0, 1)

    print("video data successfully parsed and collected!")
    np.save("data/"+name+".npy", data)

    
    return data

if __name__ == "__main__":
    vidfile = "data/def.mov"

    import boxSelector
    msks = boxSelector.selectTubes(vidfile)

    setup(vidfile, msks)
    parse()