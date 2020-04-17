import cv2
import numpy as np
from matplotlib.path import Path

POINTS = 3

# 3d array with shape (tubes, 4, 2)
frame = None
boxes = []
tube = 0
point = 0

def mouseEvent(event,x,y,flags,param):
    global boxes
    global tube
    global point

    if event == cv2.EVENT_LBUTTONDOWN:
        if point == 0:
            boxes.append([(x, y)])
            tube += 1
            point += 1
        else:
            boxes[tube - 1].append((x, y))
            point += 1
            if point == POINTS:
                point = 0

def getMask(tb):
    if len(tb) < POINTS:
        return False
    maxCord = np.amax(tb, 0)

    x, y = np.meshgrid(np.arange(frame.shape[1]), np.arange(frame.shape[0]))
    x, y = x.flatten(), y.flatten()
    points = np.vstack((x,y)).T # make a grid 

    tb = np.asarray(tb)
    p = Path(tb)
    mask = p.contains_points(points).reshape(frame.shape[0], frame.shape[1])
    mask = np.multiply(mask, 255).astype(np.uint8)
    while True:
        cv2.imshow("mask", mask)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    return mask

def selectTubes(file):
    global frame
    vid = cv2.VideoCapture(file)
    scc, frame = vid.read()
    vid.release()

    while True:
        for tb in boxes:
            if len(tb) == POINTS:
                ppt = tb[-1]
            else:
                ppt = tb[0]
            for pt in tb:
                cv2.line(frame, ppt, pt, (255, 234, 0), thickness = 2)
                ppt = pt
        cv2.namedWindow('first frame')
        cv2.setMouseCallback('first frame',mouseEvent)
        cv2.imshow("first frame", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            masks = []
            for tb in boxes:
                mask = getMask(tb)
                if mask is bool:
                    break
                masks.append(masks)
            return masks

if __name__ == "__main__":
    selectTubes("data/single.mov")