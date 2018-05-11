import cv2

cap = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier("E:\\C4T\\Image Processing\\Lesson7\\haarcascade_frontalface_alt2.xml")
mask = cv2.imread("E:\\C4T\\Image Processing\\Lesson7\\31959779_1784661771592939_6272517058240446464_n.jpg")

while (True):
    ret, frame = cap.read()
    # convert image to gray
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    # ?
    faces = cascade.detectMultiScale(gray)
    for x, y, w, h in faces:
        # draw rectangle
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))
        newMask = cv2.resize(mask, (w, h), cv2.INTER_CUBIC)
        [rows, cols] = gray.shape
        for i in range(rows):
            for j in range(cols):
                if gray[i][j] != 0:
                    frame[y:y + h, x:x + w, :] -= newMask

    cv2.imshow("Video", gray)
    check = cv2.waitKey(30)
    if check == ord('q'):
        break
