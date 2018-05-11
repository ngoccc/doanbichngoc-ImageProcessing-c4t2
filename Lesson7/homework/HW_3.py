import cv2

I = cv2.imread("E:\\C4T\\Image Processing\\Image\\noise_house.jpg")
cv2.imshow("Image", I)
cv2.waitKey(1)

filter_noise = cv2.medianBlur(I, 5)
cv2.imshow("remove noise", filter_noise)
cv2.waitKey(1)

cv2.imshow("new image", filter_noise * [-110, 101, -101])
cv2.waitKey()
