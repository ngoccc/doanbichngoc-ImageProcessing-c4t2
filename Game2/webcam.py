import cv2
import numpy as np
from threading import Thread

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


class Webcam():
    def __init__(self):
        self.cap = cv2.VideoCapture(1)
        self.frame = self.cap.read()[1]

    def update(self):
        while True:
            self.frame = self.cap.read()[1]

    def thread_webcam(self):
        Thread(None, self.update).start()

    def get_currentFrame(self):
        return self.frame

    def get_pos(self, x, y):
        hsvImage = cv2.cvtColor(self.frame, cv2.COLOR_RGB2HSV)
        binImage = cv2.inRange(hsvImage, lower, higher)
        return Scan(binImage, x, y)