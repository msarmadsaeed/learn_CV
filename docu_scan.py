import cv2
import numpy as np

frameW = 1280
frameH = 720

wid = 540
hei = 640

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Could not open camera")
    exit()
#####################################################

def getContours(img):
    contours, hei = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    maxArea = 0
    biggest = np.array([])
    for cont in contours:
        area = cv2.contourArea(cont)
        if area > 300:
            # cv2.drawContours(imgCont,cont, -1, (255,0,0),3)
            peri = cv2.arcLength(cont, True)
            apx = cv2.approxPolyDP(cont, peri*0.02, True,)
            if area>maxArea and len(apx) == 4:
                biggest = apx
                maxArea = area
        cv2.drawContours(imgCont,biggest, -1, (255,0,0),3)
    return biggest

def preProcess(img):
    imgG = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgB = cv2.GaussianBlur(imgG,(5,5),1)
    imgCanny = cv2.Canny(imgB,200,200)
    kernel = np.ones((5,5))
    imgD = cv2.dilate(imgCanny,kernel)
    imgE = cv2.erode(imgD, kernel)

    return imgE
def reorder(mypoints):
    mypoints = mypoints.reshape(4,2)
    mypointsnew = np.zeros((4,1,2), np.int32)
    add = mypoints.sum(1)

    return mypointsnew

def getWarp(img, biggest):
    re = reorder(biggest)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0,0],[wid,0][0,hei],[wid,hei]])

#####################################################
while True:
    ret,img = cap.read()
    img = cv2.resize(img,(wid,hei))
    imgCont = img.copy()
    imgThres = preProcess(img)
    persp = getContours(imgThres)
    imgWarped = getWarp(img,persp)


    if not ret:
        print("Could not read frame")
        break

    cv2.imshow("video", imgWarped)
   
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()