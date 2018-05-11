import cv2

I = cv2.imread("E:\\C4T\\Image Processing\\Image\\erosion.jpg")
cv2.imshow("image", I)
cv2.waitKey(1)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
bin_erode = cv2.erode(I, kernel)
bin_dilate = cv2.dilate(bin_erode, kernel)
cv2.imshow("new image", kernel)
cv2.waitKey()
