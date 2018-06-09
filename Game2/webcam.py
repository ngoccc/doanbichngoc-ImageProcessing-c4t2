import cv2
import numpy as np
from threading import Thread
from numba import jit

lower = np.array([0, 0, 0])
higher = np.array([255, 255, 117])

@jit
def Scan(a, m, n):
    count = 0
    for i in range(m, m + 64 + 1):
        for j in range(n, n + 64 + 1):
            if a[i, j] >= 200:
                count += 1
    if count >= 64 * 64 / 2:
        return True
    return False


class Webcam():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.frame = self.cap.read()[1]

    def update(self):
        while True:
            self.frame = self.cap.read()[1]
            self.frame = cv2.resize(self.frame, (1366, 786), cv2.INTER_CUBIC)

    def thread_webcam(self):
        Thread(None, self.update).start()

    def get_currentFrame(self):
        return self.frame

    def get_pos(self, y, x):
        self.frame = cv2.resize(self.frame, (1366, 786), cv2.INTER_CUBIC)
        hsvImage = cv2.cvtColor(self.frame, cv2.COLOR_RGB2HSV)
        binImage = cv2.inRange(hsvImage, lower, higher)
        binImage = cv2.flip(binImage, 1)
        return Scan(binImage, y, x)

