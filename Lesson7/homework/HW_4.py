import cv2
import math


def Detect_Shape(image, figure):
    shape = "???"

    # find contours
    ret, contours, hierarchy = cv2.findContours(binImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


I = cv2.imread("E:\\C4T\\Image Processing\\Image\\test3.png")
cv2.namedWindow("image", cv2.WINDOW_GUI_NORMAL)
cv2.imshow("image", I)
cv2.waitKey(1)

# convert Image to binary
B = I[:, :, 0]
G = I[:, :, 1]
R = I[:, :, 2]
C_plus = B & G & R
ret, binImg = cv2.threshold(C_plus, 100, 255, cv2.THRESH_BINARY_INV)
# cv2.imshow("binary", binImg)
# cv2.waitKey(1)

# find contours
ret, contours, hierarchy = cv2.findContours(binImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

for i in range(len(contours)):
    cv2.drawContours(I, contours, i, (255, 0, 255), 5)
    # find perimeter
    leni = cv2.arcLength(contours[i], True)
    # find area
    areai = cv2.contourArea(contours[i])
    # find number of edges
    nedges = cv2.approxPolyDP(contours[i], 5, True)

    # approximate polygon
    if len(nedges) == 3:  # triangle
        # calculate lengths of edges
        xA = nedges[0, 0, 0]
        yA = nedges[0, 0, 1]
        xB = nedges[1, 0, 0]
        yB = nedges[1, 0, 1]
        xC = nedges[2, 0, 0]
        yC = nedges[2, 0, 1]

        AB = math.sqrt((xA - xB) ** 2 + (yA - yB) ** 2)
        AC = math.sqrt((xA - xC) ** 2 + (yA - yC) ** 2)
        BC = math.sqrt((xB - xC) ** 2 + (yB - yC) ** 2)

        # error
        a = abs(AB - AC)
        b = abs(AB - BC)
        c = abs(AC - BC)

        r1 = abs(AB ** 2 + AC ** 2 - BC ** 2)
        r2 = abs(AB ** 2 + BC ** 2 - AC ** 2)
        r3 = abs(BC ** 2 + AC ** 2 - AB ** 2)

        # print(AB, AC, BC)
        # print(r1, r2, r3)

        # conditions
        et = 0.95 <= a <= 1.05 and 0.95 <= b <= 1.05 and 0.95 <= c <= 1.05
        it = 0.95 <= a <= 1.05 or 0.95 <= b <= 1.05 or 0.95 <= c <= 1.05
        rt = 0.95 <= r1 <= 1.05 or 0.95 <= r2 <= 1.05 or 0.95 <= r3 <= 1.05

        # equilateral triangle
        if et:
            cv2.putText(I, "Equilateral triangle", (nedges[1][0][0], nedges[1][0][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (0, 255, 0))
        # isosceles triangle
        elif it:
            cv2.putText(I, "Isosceles triangle", (nedges[1][0][0], nedges[1][0][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (0, 255, 0))
        # right triangle
        elif rt:
            cv2.putText(I, "Right triangle", (nedges[1][0][0], nedges[1][0][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (0, 255, 0))
        else:
            cv2.putText(I, "Triangle", (nedges[1][0][0], nedges[1][0][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5,
                        (0, 255, 0))

    elif len(nedges) == 4:  # rectangle
        # square
        (x, y, w, h) = cv2.boundingRect(nedges)
        ar = w / h
        if 0.95 <= ar <= 1.05:
            cv2.putText(I, "Square", (nedges[0][0][0], nedges[0][0][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
        else:
            cv2.putText(I, "Rectangle", (nedges[0][0][0], nedges[0][0][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
    elif len(nedges) > 8:
        (x, y, w, h) = cv2.boundingRect(nedges)
        ar = w / h
        if 0.95 <= ar <= 1.05:
            cv2.putText(I, "Circle", (nedges[1][0][0], nedges[1][0][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))
        else:
            cv2.putText(I, "Ellipse", (nedges[1][0][0], nedges[1][0][1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255, 0))

cv2.imshow("draw contours", I)
cv2.waitKey()
