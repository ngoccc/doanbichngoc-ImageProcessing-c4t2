import numpy as np
import cv2
import matplotlib.pyplot as plt


class Formatter(object):
    def __init__(self, im):
        self.im = im

    def __call__(self, x, y):
        z = self.im.get_array()[int(y), int(x)]
        return 'x={:}, y={:}, z='.format(int(x), int(y), z)


# data = np.random.random((10,10))
data = cv2.imread("E:\\C4T\\Image Processing\\Image\\Lenna.png")
cv2.imshow("Image", data)
fig, ax = plt.subplots()
data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
im = ax.imshow(data, interpolation='none')
ax.format_coord = Formatter(im)
plt.show()
