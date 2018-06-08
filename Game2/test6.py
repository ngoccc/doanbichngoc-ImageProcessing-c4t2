import cv2
import numpy as np
import time

lower = np.array([0, 0, 0])
higher = np.array([255, 255, 117])

x = []
x.append(False)
x.append(False)


def Scan(a, m, n):
    time = Time()
    count = 0
    for i in range(m, m + 64 + 1):
        for j in range(n, n + 64 + 1):
            if a[i, j] >= 200:
                count += 1
    if count >= 64 * 64 * 1 / 2:
        time.Time()
        if time.Check() and not x[-1] == True and not x[-2] == True:
            # return True
            x.append(True)
        else:
            x.append(False)
    else:
        x.append(False)


class Time():
    def Time(self):
        self.start_time = time.clock()
        while True:
            self.elapsed = time.clock() - self.start_time
            # print(self.elapsed)
            if self.elapsed >= 0.02:
                # print(self.elapsed)
                self.start_time = time.clock()
                return False

    def Check(self):
        if self.elapsed >= 0.02:
            return True
        else:
            return False


cap = cv2.VideoCapture(0)
a = Time()
while True:
    frame = cap.read()[1]
    frame = cv2.resize(frame, (1366, 786), cv2.INTER_CUBIC)
    frame = cv2.flip(frame, 1)
    hsvImage = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
    binImage = cv2.inRange(hsvImage, lower, higher)
    # print(Scan(binImage, 10, 10))
    cv2.imshow("binImg", binImage)
    cv2.waitKey(1)
    # a.Time()
    # print(Scan(binImage, 10, 10))
    Scan(binImage, 10, 1366 - 74)
    print(x[-1])
