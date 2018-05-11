import cv2
import numpy as np

cap = cv2.VideoCapture(0)
lower = np.array([0, 25, 61])
higher = np.array([255, 224, 255])

cascade = cv2.CascadeClassifier("E:\\C4T\\Image Processing\\Lesson7\\haarcascade_frontalface_alt2.xml")

while True:
    ret, frame = cap.read()
    # convert image to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # convert image to hsv
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # convert image to binary image
    binImg = cv2.inRange(hsvImage, lower, higher)
    # detect faces
    faces = cascade.detectMultiScale(gray)
    for x, y, w, h in faces:
        # turn faces to black ?????
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), cv2.FILLED)
    # detect hands
    # # find contours
    ret, contours, hierarchy = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # # find center
    for i in range(len(contours)):
        M = cv2.moments(contours[i])
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(frame, (cx, cy), 10, (120, 255, 0), 5)

    cv2.imshow("video", frame)
    cv2.waitKey(30)
