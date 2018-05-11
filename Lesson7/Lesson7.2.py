import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier("E:\\C4T\\Image Processing\\Lesson7\\haarcascade_frontalface_alt2.xml")
mask = cv2.imread("E:\\C4T\\Image Processing\\Lesson7\\31959779_1784661771592939_6272517058240446464_n.jpg")

while (True):
    ret, frame = cap.read()

    # convert image to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # detect face
    faces = cascade.detectMultiScale(gray)
    for x, y, w, h in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        newmask = cv2.resize(mask, (w, h), cv2.INTER_CUBIC)
        frame[y:y + h, x:x + w, :] -= newmask
    cv2.imshow("video", frame)
    key = cv2.waitKey(30)
    if key == ord('q'):
        break
# BTVN:
# 1. detect được tay?, tâm bàn tay (hình tròn màu đỏ), (xóa mặt???) - "làm việc webcam"??? <viết 1 hàm con bên ngoài thay vào chỗ trừ đi>
# 2. giữ được màu hồng????? -- đang không hiểu tsao màu hồng bị nhiễu
