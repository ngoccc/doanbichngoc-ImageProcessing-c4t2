import cv2
import numpy as np

cap = cv2.VideoCapture(0)
lower = np.array([0, 25, 61])
higher = np.array([255, 224, 255])

cascade = cv2.CascadeClassifier("E:\\C4T\\Image Processing\\Lesson7\\haarcascade_frontalface_alt2.xml")

while (True):
    ret, frame = cap.read()
    # get ROI
    roi = frame[0:int(3 / 4 * frame.shape[1]), 0:int(frame.shape[0] / 2), :]
    roi = cv2.flip(roi, 1)
    # convert
    hsvImage = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
    binImage = cv2.inRange(hsvImage, lower, higher)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    img_erode = cv2.erode(binImage, kernel)
    filter_noise = cv2.medianBlur(img_erode, 3)

    # find contours
    ret, contours, hierarchy = cv2.findContours(binImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    # draw contour
    for i in contours:
        cv2.drawContours(roi, i, -1, (255, 0, 255), 5)

    #
    if len(contours) > 0:
        maxlen = cv2.arcLength(contours[0], True)
        indexmax = 0
        for i in range(len(contours)):
            leni = cv2.arcLength(contours[i], True)
            if leni > maxlen:
                maxlen = leni
                indexmax = i
        cv2.drawContours(roi, contours, indexmax, (255, 0, 0), 5)

        # find center
        M = cv2.moments(contours[indexmax])
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        cv2.circle(roi, (cx, cy), 10, (120, 255, 0), 5)
        cv2.circle(filter_noise, (cx, cy), 10, (120, 255, 0), 5)

    cv2.imshow("roi", roi)
    cv2.imshow("video", filter_noise)
    cv2.waitKey(30)
