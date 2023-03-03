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

def getContours(img):
    cont, heirarchy = cv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in cont:
        area = cv2.contourArea(cnt)

        cv2.drawContours(imgcpy, cnt,-1, (255,0,0),3)
        peri = cv2.arcLength(cnt, True)
        aprx = cv2.approxPolyDP(cnt, 0.02*peri, True)
        edg = len(aprx)

        x,y,w,h = cv2.boundingRect(aprx)
        cv2.rectangle(imgcpy, (x,y), (x+w,y+h), (0,255,0),2)

        if edg == 3:
            tp = "Triangle"
        elif edg == 4:
            asp = w/float(h)
            if 0.95 < asp < 1.05:
                tp = "Square"
            else: 
                tp = "Rectangle"
        else:
            tp = "Circle"

        cv2.putText(imgcpy, tp, (x+(w//2)-10, y+(h//2)-10), cv2.FONT_HERSHEY_COMPLEX, 0.7, (0,0,0),2)



path = 'res/shapes.png'

img = cv2.imread(path)
imgcpy = img.copy()

imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7,7),1)
imgCanny = cv2.Canny(imgBlur,50,50)

getContours(imgCanny)

imgZ = np.zeros_like(img)
imgSt = stackImages(0.7,[[img,imgGray,imgBlur],[imgCanny,imgcpy,imgZ]])

cv2.imshow("stack",imgSt)
cv2.waitKey(0)