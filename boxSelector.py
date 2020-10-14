import cv2
import numpy as np
from matplotlib.path import Path

POINTS = 4

# 3d array with shape (tubes, 4, 2)
frame = None
boxes = []
box = []
tube = 0
point = 0
size = 1
highlightFrame = 100

def setPoints(p):
    global POINTS
    POINTS = p

def mouseEvent(event,x,y,flags,param):
    global boxes
    global box
    global tube
    global point

    # if mouse L button pressed, add the point to the points list
    # if the vertices for a complete box has already been reached, create a new box
    if event == cv2.EVENT_LBUTTONDOWN:
        if point == POINTS:
            box = []
            point = 0
        
        point += 1
        box.append((int(x / size), int(y / size)))
        #print("box: ", box)
        
        if point == POINTS:
            tube += 1
            boxes.append(box)
        #print(boxes)

def getMask(tb, frameOriginal):
    # if there are less than enough points, return false
    if len(tb) < POINTS:
        return False

    # create a grid that matches the resolution
    x, y = np.meshgrid(np.arange(frameOriginal.shape[1]), np.arange(frameOriginal.shape[0]))
    x, y = x.flatten(), y.flatten()
    points = np.vstack((x,y)).T

    # find all of the points encircled by the polygon
    tb = np.asarray(tb)
    p = Path(tb)
    mask = p.contains_points(points).reshape(frameOriginal.shape[0], frameOriginal.shape[1])

    # turn the points into a black and white mask
    mask = np.multiply(mask, 255).astype(np.uint8)
    mask = np.stack((mask, mask, mask), -1)
    
    return mask

def renderLines():
    global frame

    # draws lines between the current points on the most recent box

    if point < 2: return

    ppt = box[-2]
    pt = box[-1]
    cv2.line(frame, (int(ppt[0] * size), int(ppt[1] * size)), 
        (int(pt[0] * size), int(pt[1] * size)), (255, 234, 0), thickness = 2)
        
    if point != POINTS: return    

    ppt = box[-1]
    pt = box[0]

    cv2.line(frame, (int(ppt[0] * size), int(ppt[1] * size)), 
        (int(pt[0] * size), int(pt[1] * size)), (255, 234, 0), thickness = 2)

def selectTubes(file, insize):
    global frame
    global boxes
    global size

    size = insize

    # open the first frame from the video file
    vid = cv2.VideoCapture(file)
    for i in range(100):
        scc, frame = vid.read()
    vid.release()
    original = frame
    frame = cv2.resize(frame, (int(frame.shape[1]*size), int(frame.shape[0]*size)))

    # add mouselistener
    cv2.namedWindow('highlight frame')
    cv2.setMouseCallback('highlight frame',mouseEvent)
    # until the use presses q, loop through this

    while True:

        # render the lines
        renderLines()

        # display the image or its updated form
        cv2.imshow("highlight frame", frame)

        # if the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            masks = []

            # for each box drawn, make a mask and append it to the list. Ignore if incomplete
            for tb in boxes:
                mask = getMask(tb, original)
                mask = np.asarray(mask)
                if isinstance(mask, bool) == True:
                    return masks
                masks.append(mask)
            
            # return the mask list
            cv2.destroyAllWindows()
            print("masks successfully generated!")
            
            '''
            for mask in masks:
                cv2.imshow("a", mask)
                cv2.waitKey(0)
            '''
            return masks

if __name__ == "__main__":
    mas = selectTubes("data/single.mov")
    
    for m in mas:
        while True:
            cv2.imshow("mask", m)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    