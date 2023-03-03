import cv2
import numpy as np

def empty(a):
    pass
 
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

path = "res/lambo.png"
cv2.namedWindow("bars")
cv2.resizeWindow("bars",1000,800)
cv2.createTrackbar('Hue min','bars',0,179,empty)
cv2.createTrackbar('Hue max','bars',179,179,empty)
cv2.createTrackbar('Sat min','bars',0,255,empty)
cv2.createTrackbar('Sat max','bars',255,255,empty)
cv2.createTrackbar('Vak min','bars',0,255,empty)
cv2.createTrackbar('Val max','bars',255,255,empty)

while True:
    img = cv2.imread(path)
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos('Hue min', 'bars')
    h_max = cv2.getTrackbarPos('Hue max', 'bars')
    s_min = cv2.getTrackbarPos('Sat min', 'bars')
    s_max = cv2.getTrackbarPos('Sat max', 'bars')
    v_min = cv2.getTrackbarPos('Val min', 'bars')
    v_max = cv2.getTrackbarPos('Val max', 'bars')

    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper)

    imgres = cv2.bitwise_and(img,img,mask = mask)

    imstack = stackImages(0.6,[img,imgHSV,mask,imgres])
    cv2.imshow("stack",imstack)
    # cv2.imshow("image",img)
    # cv2.imshow('imgHSV',imgHSV)
    # cv2.imshow('imgres',imgres)
    cv2.waitKey(1)