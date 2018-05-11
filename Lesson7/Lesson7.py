import numpy as np
import cv2
import matplotlib as plt

# read image
I = cv2.imread("E:\\C4T\\Image Processing\\Image\\shape.jpg")

# show image
# cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.imshow("Image", I)
cv2.waitKey(1)
# Extract 3 channels: B - G - R
B = I[:, :, 0]
G = I[:, :, 1]
R = I[:, :, 2]
# cv2.imshow("Blue", B)
# cv2.imshow("Green", G)
# cv2.imshow("Red", R)
# cv2.waitKey(1)

#
C_plus = B & G & R
cv2.imshow("newImg", C_plus)
cv2.waitKey(1)

# convert Image to binary
ret, binImg = cv2.threshold(C_plus, 100, 255, cv2.THRESH_BINARY_INV)
cv2.imshow("binary", binImg)
cv2.waitKey(1)

# find contour
ret, contours, hierarchy = cv2.findContours(binImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# simple: tiết kiệm bộ nhớ (không bao hết); none: (bao hết)
# print(ret)

# for i in contours:
#     cv2.drawContours(I, i, -1, (255, 0, 255), 5) # truy xuất theo giá trị (value)
# cv2.imshow("Image contour ", I)
# cv2.waitKey()

for i in range(len(contours)):
    cv2.drawContours(I, contours, i, (255, 0, 255), 5)  # tx thông qua chỉ số (index) (giống mảng)
    leni = cv2.arcLength(contours[i], True)
    print("len of contour: ", leni)
    areai = cv2.contourArea(contours[i])
    print("area contour: ", areai)
    # approximate polygon
    nedges = cv2.approxPolyDP(contours[i], 5, True)
    print(nedges)
    print("polyedges: ", len(nedges))
    if len(nedges) == 3:
        cv2.putText(I, "Triangle", (nedges[1][0][0], nedges[1][0][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
        # 0,0: hàng và cột đầu; 0-1: vị trí x,y)
    elif len(nedges) == 4:
        cv2.putText(I, "Rectangle", (nedges[0][0][0], nedges[0][0][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
    elif len(nedges) > 8:
        cv2.putText(I, "Circle", (nedges[1][0][0], nedges[1][0][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))

    # tìm tâm
    ## ko có lực - thay = intensity
    M = cv2.moments(contours[i])
    cx = int(M['m10'] / M['m00']) #theo chiều x (00: tổng số điểm)
    cy = int(M['m01'] / M['m00']) #theo chiều y
    cv2.circle(I, (cx, cy), 10, (120, 255, 0), 5)

cv2.imshow("Image contour ", I)
cv2.waitKey()

#
# BTVN: dựa vào tọa độ, diện tích... -> hình ???
