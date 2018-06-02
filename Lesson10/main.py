import Webcam
import cv2

test = Webcam.webcam()
test.thread_webcam()
while True:
    frame = test.get_currentFrame()
    cv2.imshow("threadmain", frame)
    cv2.waitKey(10)