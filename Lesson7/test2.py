import numpy as np
import cv2

# connect cam
cap = cv2.VideoCapture(0)
lower = np.array([0, 25, 61])
higher = np.array([255, 224, 150])

cascade = cv2.CascadeClassifier("E:\\C4T\\Image Processing\\Lesson7\\haarcascade_frontalface_alt2.xml")

while True:
    ret, frame = cap.read()
    # convert to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # hsv
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # binary image
    binImg = cv2.inRange(hsvImage, lower, higher)
    cv2.imshow("binimg", binImg)
    cv2.waitKey(30)
    # # detect face and chuyển chúng into black =))))
    # faces = cascade.detectMultiScale(gray)
    # for x, y, w, h in faces:
    #     cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), cv2.FILLED)
    # #     CODE tim` contuor
    # ret, contours, hierachy = cv2.findContours(binImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # for i in range(len(contours)):
    #     cv2.drawContours(binImg, contours, i, (255, 0, 255), 5)
    #     M = cv2.moments(contours[i])
    #     cx = int(M['m10'] / M['m00'])
    #     cy = int(M["m01"] / M['m00'])
    #     cv2.circle(frame, (cx, cy), 10, (255, 0, 0), 5)
    # key = cv2.waitKey(30)
    # if key == ord("q"):
    #     break
