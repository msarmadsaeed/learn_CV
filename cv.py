import cv2 as cv

frameW = 1280
frameH = 720

cap = cv.VideoCapture(0)
 
if not cap.isOpened():
    print("Could not open camera")
    exit()
cap.set(3,frameW)
cap.set(4,frameH)

while True:
    ret,img = cap.read()
    
    if not ret:
        print("Could not read frame")
        break
    cv.imshow("video", img)
   
    
    if cv.waitKey(1) and 0xFF == ord('q'):
        break