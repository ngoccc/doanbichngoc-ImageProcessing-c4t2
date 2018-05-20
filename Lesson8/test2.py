import cv2
import numpy as np
#
# # read image
# I1 = cv2.imread("E:\\C4T\\Image Processing\\Lesson8\\Image_2\\1.png")
#
# # add image
# pattern = cv2.imread("E:\\C4T\\Image Processing\\Lesson8\\Image_2\\1.png")
# pattern = cv2.resize(pattern, (I1.shape[1], I1.shape[0]))
#
# # create mask
# mask = np.ones_like(I1, dtype=np.float32)
#
# # compute SIFT
# gray1 = cv2.cvtColor(I1, cv2.COLOR_RGB2GRAY)
# sift1 = cv2.xfeatures2d.SIFT_create()
# kpt1, des1 = sift1.detectAndCompute(gray1, None)

cap = cv2.VideoCapture(0)

while True:
    ret, I2 = cap.read()
    gray2 = cv2.cvtColor(I2, cv2.COLOR_RGB2GRAY)
    sift2 = cv2.xfeatures2d.SIFT_create()
    kpt2, des2 = sift2.detectAndCompute(gray2, None)



    # matching Bruce force
    bf = cv2.BFMatcher_create()
    matches = bf.knnMatch(des1, des2, 2)
    # OutImg = cv2.drawMatchesKnn(I1, kpt1, I2, kpt2, matches, None)
    # cv2.imshow("matching", OutImg)
    # cv2.waitKey(1)

    # choose good match
    good = []
    newgood = []
    for m, n in matches:
        if m.distance < 0.4 * n.distance:
            good.append([m])
            newgood.append(m)

    # find Homography
    srcPoints = np.float32([kpt1[m.queryIdx].pt for m in newgood]).reshape(-1, 1, 2)
    dstPoints = np.float32([kpt2[m.trainIdx].pt for m in newgood]).reshape(-1, 1, 2)
    M, H = cv2.findHomography(srcPoints, dstPoints)
    w = gray1.shape[1]
    h = gray1.shape[0]

    ncorners = np.float32([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]]).reshape(-1, 1, 2)
    if M is not None:
        # find new corner on image through Homography
        npts = cv2.perspectiveTransform(ncorners, M)
        cv2.polylines(I2, np.int32([npts]), True, (0, 0, 255), 5)

        blendMask = cv2.warpPerspective(mask, M, (I2.shape[1], I2.shape[0]))
        newPattern = cv2.warpPerspective(pattern, M, (I2.shape[1], I2.shape[0]))
        im4 = I2 * (1-blendMask) + newPattern
        im4 = cv2.convertScaleAbs(im4)
        cv2.imshow("insert", im4)
    cv2.imshow("result", I2)
    cv2.waitKey(30)
    # OutImg2 = cv2.drawMatchesKnn(I1, kpt1, I2, kpt2, good, None)
    # cv2.imshow("matching good", OutImg2)
    # cv2.waitKey()
