import cv2
import numpy as np
import matplotlib as plt

# Read image
I = cv2.imread("E:\\C4T\\Image Processing\\Image\\Lenna.png")
# Show image
#cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.imshow("Image", I)
print(I.shape)
print(len(I.shape))

cv2.waitKey(1)  # Wait until press key
# Get dimension
[rows, cols, channel] = I.shape  # return
# convert color to gray
gray = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)
cv2.imshow("gray", gray)
cv2.waitKey(1)
print(gray.shape)
print(len(gray.shape))
# get value
[rows, cols] = gray.shape
for i in range(rows):
    for j in range(cols):
        # print(gray[i, j], end=" ")
        if i % 2 == 0 and j % 2 == 0:
            gray[i, j] = 255
    # print('\n')
cv2.imshow("new gray", gray)
cv2.waitKey(1)

# get pixel
rows = 0
cols = 0
channel = 0
if (len(I.shape) == 3):
    [rows, cols, channel] = I.shape
else:
    [rows, cols] = I.shape
# for i in range(rows):
#     for j in range(cols):
#         print("{", end="")
#         for k in range(channel):
#             if k == channel - 1:
#                 print(I[i, j, k], end="")
#             else:
#                 print(I[i, j, k], end=",")
#         print("}", end="")
#     print('\n')
print(I[0:10, 0:10, 0])
I[100:200, 30:40, :] = 255
cv2.imshow("newI", I)
cv2.waitKey()
