import cv2
from threading import Thread


class Webcam():
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.frame = self.cap.read()[1]

    def update(self):
        while True:
            self.frame = self.cap.read()[1]

    def thread_webcam(self):
        Thread(None, self.update).start()

    def get_currentFrame(self):
        return self.frame
    
