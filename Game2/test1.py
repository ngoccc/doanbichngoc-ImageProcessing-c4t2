import cv2


class Point():
    def __init__(self, r=5):
        self.x = random.randrange(20 + 10, window_width - (20 + 10), 5)
        self.y = random.randrange(20 + 10, window_height - (20 + 10), 5)
        self.radius = r
        self.spawnTime = 0

    def spawn(self, f):
        if self.spawnTime > 0:
            self.spawnTime -= 1
        else:
            self.__init__()
            cv2.circle(f, (self.x, self.y), self.radius, (255, 0, 0), -1)
            self.spawnTime = 100


# class Spawner():
#     def __init__(self):
#         pass


class Game():
    def __init__(self):
        pass

    def update(self):
        pass


def main():
    # # connect webcam
    # cap = cv2.VideoCapture(0)
    # # cascade = cv2.CascadeClassifier("E:\\C4T\\Image Processing\\Lesson7\\haarcascade_frontalface_alt2.xml")
    #
    # while True:
    #     ret, frame = cap.read()
    #     cv2.imshow("dancing", frame)
    #     cv2.waitKey(30)
    pass


if __name__ == '__main__':
    main()
