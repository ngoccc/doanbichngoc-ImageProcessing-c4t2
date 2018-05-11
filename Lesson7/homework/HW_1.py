import numpy as np
import cv2

# Load Image RGB
I = cv2.imread("E:\\C4T\\Fundamental\\Image\\shape.jpg")
cv2.imshow("I", I)
cv2.waitKey(1)
# convert Whiter color to black
[rows, cols, c] = I.shape
for i in range(rows):
    for j in range(cols):
        if I[i, j, 0] > 200 and I[i, j, 1] > 200 and I[i, j, 2] > 200:
            I[i, j, :] = 0
cv2.imshow("Inew", I)
cv2.waitKey(1)
# Extract chanel B
B = I[:, :, 0]
# Extract chanel G
G = I[:, :, 1]
# Extract chanel R
R = I[:, :, 2]

# Thresold for B
threshB, binB = cv2.threshold(B, 200, 255, cv2.THRESH_BINARY)

# Thresold for G
threshG, binG = cv2.threshold(G, 200, 255, cv2.THRESH_BINARY)

# Thresold for R
threshR, binR = cv2.threshold(R, 200, 255, cv2.THRESH_BINARY)

cv2.imshow("binaryImage1", binB)
cv2.imshow("binaryImage2", binG)
cv2.imshow("binaryImage3", binR)
cv2.imshow("binaryImage", binB + binG + binR)

cv2.waitKey()
