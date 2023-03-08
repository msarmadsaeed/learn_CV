import cv2

img = cv2.imread('res/lena.png')

faceCas = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

imgG = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = faceCas.detectMultiScale(imgG,1.1,4)

for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+w),(255,0,0),2)

cv2.imshow("img",img)
cv2.waitKey(0)