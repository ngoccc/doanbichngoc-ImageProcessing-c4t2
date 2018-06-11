import numpy as np
import cv2

def Scan(a, m, n):
    count = 0
    for i in range(m, n + 1):
        for j in range(m, n + 1):
            if a[i, j] >= 100:
                count += 1
    if count >= 64 * 64 / 2:
        return True
    return False


cap = cv2.VideoCapture(1)
# fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
# init_bg = cap.read()[1]
# init_bg = cv2.cvtColor(init_bg, cv2.COLOR_RGB2GRAY)
# # get first frame
# for i in range(100):
#     ret, frame = cap.read()
#     init_bg = frame
#     init_bg = cv2.cvtColor(init_bg, cv2.COLOR_RGB2GRAY)
#
# history = 100
# nGauss = 20
# bgThresh = 0.2
# noise = 7
# print(init_bg.shape[0])
# print(init_bg.shape[1])
# bsmog  = cv2.bgsegm.createBackgroundSubtractorMOG(history,nGauss,bgThresh,noise)
while True:
    ret, frame = cap.read()
    roi = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
    fgmask = fgbg.apply(frame)
    # fgmask = cv2.flip(fgmask, 1)
    #fgmask = init_bg - frame
    #fgmask = cv2.threshold(fgmask,100,255,cv2.THRESH_BINARY)
    # # remove noise
    #
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # fgmask = cv2.erode(fgmask, kernel)
    # fgmask = cv2.medianBlur(fgmask, 3)
    # filter_noise = cv2.flip(filter_noise, 1)

    # [rows, cols] = fgmask.shape
    print(Scan(fgmask, 10, 10 + 64))
    cv2.imshow("frame", fgmask)
    # print(fgmask[10][10])
    # roi = cv2.GaussianBlur(roi, (7, 7), 0)
    #
    # result = bsmog.apply(roi, None, 0.5)
    #
    #
    # cv2.imshow('frame', result)
    # k = cv2.waitKey(30) & 0xff
    # if k == 27:
    #     break
cap.release()
cv2.destroyAllWindows()
