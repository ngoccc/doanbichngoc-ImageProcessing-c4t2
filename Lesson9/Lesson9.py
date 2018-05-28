import numpy as np
import cv2


def MatMul(a, b):
    c = []
    ma = len(a)
    na = len(a[0])
    mb = len(b)
    nb = len(b[0])

    if na == mb:
        for i in range(ma):
            c1 = []
            for j in range(nb):
                x = 0
                for k in range(na):
                    x += a[i][k] * b[k][j]
                c1.append(x)
            c.append(c1)
    return c


A = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
B = [[-1, -2, 1], [0, 0, 0], [1, 2, 1]]
C = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]
I = cv2.imread("E:\\C4T\\Image Processing\\Image\\noise_house.jpg")
I = cv2.resize(I, (100, 100), cv2.INTER_CUBIC)
gray = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)
[rows, cols] = gray.shape
for i in range(1, rows - 1):
    for j in range(1, cols - 1):
        # create mat
        d = []
        for m in range(i - 1, i + 2):
            d1 = []
            for n in range(j - 1, j + 2):
                d1.append(gray[m][n])
            d.append(d1)

        # multiply mat
        newMat = MatMul(C, d)

        # replace mat
        for m in range(i - 1, i + 2):
            for n in range(j - 1, j + 2):
                gray[m][n] = newMat[m - (i - 1)][n - (j - 1)]

cv2.imshow("image", gray)
cv2.waitKey()
