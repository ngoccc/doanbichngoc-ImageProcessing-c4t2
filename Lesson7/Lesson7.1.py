import numpy as np
import cv2

# connect webcam
cap = cv2.VideoCapture(0)
lower = np.array([0, 45, 61])
higher = np.array([255, 224, 255])
# 82

while (True):
    ret, frame = cap.read()
    # ret: return True / False (đọc dc ảnh k)
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    binImage = cv2.inRange(hsvImage, lower, higher)
    cv2.imshow("binimage", binImage)
    cv2.imshow("hsvimage", hsvImage)
    cv2.imshow("video", frame)
    key = cv2.waitKey(30)

    if key == ord('q'):
        break
