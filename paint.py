import cv2
import numpy as np

frameW = 1280
frameH = 720

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Could not open camera")
    exit()
cap.set(3,frameW)
cap.set(4,frameH)
###################################################

myColors = [[5,107,0,19,255,255], #orrange
            [133,56,0,159,156,255], #purple
            [57,76,0,100,255,255],  #green
            [90,48,0,118,255,255]]  #blue
myColorValues = [[51,153,255],          ## BGR
                 [255,0,255],
                 [0,255,0],
                [255,0,0]]

myPoints = []   #(x,y,colID)

def drawOnCanv(myPoints, myColorValues):
    for points in myPoints:
        cv2.circle(imgRes, (points[0],points[1]),10, myColorValues[points[2]],cv2.FILLED)

def getContours(img):
    cont, heirarchy = cv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0
    for cnt in cont:
        area = cv2.contourArea(cnt)

        # cv2.drawContours(imgRes, cnt,-1, (255,0,0),3)
        peri = cv2.arcLength(cnt, True)
        aprx = cv2.approxPolyDP(cnt, 0.02*peri, True)
        x,y,w,h = cv2.boundingRect(aprx)
    return x+w//2,y

def findColor(img,myColors,myColorValues):
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count = 0
    newpoints = []
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        x,y = getContours(mask)
        cv2.circle(imgRes, (x,y),10, myColorValues[count],cv2.FILLED)
        if x and y:
            newpoints.append([x,y,count])
        count+=1
        # cv2.imshow(str(color[0]), mask)
    return newpoints

while True:
    ret,img = cap.read()
    imgRes = img.copy()
    newPoints = findColor(img,myColors,myColorValues)

    if newPoints:
        for points in newPoints:
            myPoints.append(points)
    
    if myPoints:
        drawOnCanv(myPoints, myColorValues)


    if not ret:
        print("Could not read frame")
        break


    cv2.imshow("video", imgRes)
   
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()