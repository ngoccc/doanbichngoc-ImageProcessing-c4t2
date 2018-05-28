import cv2


def MatMul(a, b):
    sum = 0
    if len(a) == len(b):
        for i in range(len(a)):
            for j in range(len(b)):
                sum += a[i][j] * b[i][j]
    return sum


A = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
I = cv2.imread("E:\\C4T\\Image Processing\\Image\\noise_house.jpg")
I = cv2.resize(I, (100, 100), cv2.INTER_CUBIC)
gray = cv2.cvtColor(I, cv2.COLOR_RGB2GRAY)
[rows, cols] = gray.shape
cv2.imshow("image", gray)
cv2.waitKey()
