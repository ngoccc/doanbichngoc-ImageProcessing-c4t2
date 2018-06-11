import cv2
import numpy as np
from threading import Thread
import time
from numba import jit

lower = np.array([0, 0, 0])
higher = np.array([255, 255, 117])


class Time:
    def Time(self):
        self.start_time = time.clock()
        while True:
            self.elapsed = time.clock() - self.start_time
            if self.elapsed >= 0.02:
                self.start_time = time.clock()
                return False

    def Check(self):
        if self.elapsed >= 0.02:
            return True
        else:
            return False


class Webcam():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.frame = self.cap.read()[1]
        self.x = []
        self.x.append(False)
        self.x.append(False)

    def update(self):
        while True:
            self.frame = self.cap.read()[1]
            self.frame = cv2.resize(self.frame, (1366, 786), cv2.INTER_CUBIC)

    def thread_webcam(self):
        Thread(None, self.update).start()

    def get_currentFrame(self):
        return self.frame

    @jit
    def Scan(self, a, m, n):
        time = Time()
        count = 0
        for i in range(m, m + 64 + 1):
            for j in range(n, n + 64 + 1):
                if a[i, j] >= 200:
                    count += 1
        if count >= 64 * 64 * 1 / 2:
            time.Time()
            if time.Check() and not self.x[-1] == True and not self.x[-2] == True:
                # return True
                self.x.append(True)
            else:
                self.x.append(False)
        else:
            self.x.append(False)

    def get_pos(self, y, x):
        self.frame = cv2.resize(self.frame, (1366, 786), cv2.INTER_CUBIC)
        hsvImage = cv2.cvtColor(self.frame, cv2.COLOR_RGB2HSV)
        binImage = cv2.inRange(hsvImage, lower, higher)
        binImage = cv2.flip(binImage, 1)
        self.Scan(binImage, y, x)
        return self.x[-1]
