import numpy as np
import cv2
import matplotlib as plt

I = cv2.imread("E:\\C4T\\Image Processing\\Image\\noise_house.jpg")
cv2.imshow("Image", I)
cv2.waitKey(1)
gray = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)
filter_noise = cv2.medianBlur(gray, 5)
cv2.imshow("remove noise", filter_noise)
cv2.waitKey(1)
# convert to binary
ret, binImage = cv2.threshold(filter_noise, 100, 255, cv2.THRESH_BINARY)
cv2.imshow("binImage", binImage)
cv2.waitKey(1)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
img_dilate = cv2.dilate(binImage, kernel)
#cv2.imshow("binImage", binImage)
img_erode = cv2.erode(binImage, kernel)
cv2.imshow("dilate", img_dilate)
cv2.waitKey(1)
cv2.imshow("erode", img_erode)
cv2.waitKey()
