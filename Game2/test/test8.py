import webcam
import cv2

test = webcam.Webcam()
test.thread_webcam()
while True:
    frame = test.get_currentFrame()
    # cv2.imshow("aa",frame)
    # cv2.waitKey(30)
    #cv2.rectangle(frame, (10, 786 - 74), (10 + 64, 786 - 74 + 64), (0, 0, 0), 3)
    cv2.imshow("a", frame)
    cv2.waitKey(30)
    print(test.get_pos(10, 10))
