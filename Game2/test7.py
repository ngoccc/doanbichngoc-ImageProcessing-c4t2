import cv2
import numpy as np

lower = np.array([0, 0, 0])
higher = np.array([255, 255, 117])


def Scan(a, m, n):
    count = 0
    for i in range(m, n + 64 + 1):
        for j in range(m, n + 64 + 1):
            if a[i, j] >= 200:
                count += 1
    if count >= 64 * 64 / 2:
        return True
    return False


cap = cv2.VideoCapture(0)

while True:
    frame = cap.read()[1]
    frame = cv2.flip(frame, 1)
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    binImage = cv2.inRange(hsvImage, lower, higher)
    print(Scan(binImage, 10, 10))
    cv2.imshow("binImg", binImage)
    cv2.waitKey(1)
