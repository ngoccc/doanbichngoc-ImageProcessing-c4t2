from Variables import *
from Point import Point
from Scoreboard import Scoreboard
from Functions import Display_Performance


class Game:
    def __init__(self, speed=5):
        self.speed = speed
        point_speed = self.speed
        # points
        self.upLeft = Point(upLeft, 1, posUpLeft, point_speed)
        self.upRight = Point(upRight, 2, posUpRight, point_speed)
        self.downLeft = Point(downLeft, 3, posDownLeft, point_speed)
        self.downRight = Point(downRight, 4, posDownRight, point_speed)
        # score
        self.score = Scoreboard()
        #
        self.perfect = 0
        self.great = 0
        self.bad = 0
        self.miss = 0
        self.performance = ""

    def update(self):
        if self.upLeft.spawnTime == 0:
            pygame.mixer.music.play(1)

        # verse 1
        if self.upLeft.spawnTime == 0:
            self.upLeft.add()
        if self.upRight.spawnTime == 34:
            self.upRight.add()
        if self.upLeft.spawnTime == 76:
            self.upLeft.add()
        if self.upRight.spawnTime == 115:
            self.upRight.add()
        if self.downRight.spawnTime == 142:  # moti
            self.downRight.add()
        if self.upLeft.spawnTime == 180 and self.downRight.spawnTime == 180:
            self.upLeft.add()
            self.downRight.add()
        if self.upRight.spawnTime == 195 and self.downLeft.spawnTime == 195:
            self.upRight.add()
            self.downLeft.add()
        if self.downRight.spawnTime == 225 and self.downLeft.spawnTime == 225:
            self.downLeft.add()
            self.downRight.add()
        if self.upRight.spawnTime == 235:  # yes
            self.upRight.add()
        if self.upRight.spawnTime == 260:  # yes
            self.upRight.add()

        if self.downLeft.spawnTime == 312:  # insti
            self.downLeft.add()
        if self.upRight.spawnTime == 355 and self.downLeft.spawnTime == 355:
            self.upRight.add()
            self.downLeft.add()
        if self.upLeft.spawnTime == 383 and self.downRight.spawnTime == 383:
            self.upLeft.add()
            self.downRight.add()
        if self.downRight.spawnTime == 403 and self.downLeft.spawnTime == 403:
            self.downLeft.add()
            self.downRight.add()
        if self.upLeft.spawnTime == 420:  # that's
            self.upLeft.add()
        if self.upLeft.spawnTime == 442:  # that's
            self.upLeft.add()

        if self.downLeft.spawnTime == 474:
            self.downLeft.add()
        if self.upLeft.spawnTime == 520:
            self.upLeft.add()
        if self.upRight.spawnTime == 557:
            self.upRight.add()
        if self.downRight.spawnTime == 594:
            self.downRight.add()
        if self.downRight.spawnTime == 634:
            self.downRight.add()
        if self.upRight.spawnTime == 674:
            self.upRight.add()
        if self.upLeft.spawnTime == 713:
            self.upLeft.add()
        if self.downLeft.spawnTime == 740:
            self.downLeft.add()

        if self.downRight.spawnTime == 752 and self.downLeft.spawnTime == 752:
            self.downLeft.add()
            self.downRight.add()
        if self.downRight.spawnTime == 805 and self.downLeft.spawnTime == 805:
            self.downLeft.add()
            self.downRight.add()

        if self.upRight.spawnTime == 835 and self.upLeft.spawnTime == 835:
            self.upLeft.add()
            self.upRight.add()
        if self.downRight.spawnTime == 865 and self.downLeft.spawnTime == 865:
            self.downRight.add()
            self.downLeft.add()
        if self.upRight.spawnTime == 895:
            self.upRight.add()
        if self.upRight.spawnTime == 915:
            self.upRight.add()
        if self.upRight.spawnTime == 937 and self.upLeft.spawnTime == 937:
            self.upRight.add()
            self.upLeft.add()
        if self.downRight.spawnTime == 960 and self.downLeft.spawnTime == 960:
            self.downLeft.add()
            self.downRight.add()

        if self.downRight.spawnTime == 990:
            self.downRight.add()
        if self.upRight.spawnTime == 1017:
            self.upRight.add()
        if self.upLeft.spawnTime == 1045:
            self.upLeft.add()
        if self.downLeft.spawnTime == 1070:
            self.downLeft.add()
        if self.downLeft.spawnTime == 1100:
            self.downLeft.add()
        if self.upLeft.spawnTime == 1120:
            self.upLeft.add()
        if self.upRight.spawnTime == 1140:
            self.upRight.add()
        if self.downRight.spawnTime == 1150:
            self.downRight.add()

        if self.upLeft.spawnTime == 1170:
            self.upLeft.add()
        if self.upLeft.spawnTime == 1190:
            self.upLeft.add()
        if self.upRight.spawnTime == 1235:
            self.upRight.add()
        if self.upRight.spawnTime == 1260:
            self.upRight.add()
        if self.downRight.spawnTime == 1285:
            self.downRight.add()
        if self.downRight.spawnTime == 1305:
            self.downRight.add()
        if self.upLeft.spawnTime == 1335:
            self.upLeft.add()
        if self.upLeft.spawnTime == 1355:
            self.upLeft.add()

        if self.upRight.spawnTime == 1380 and self.upLeft.spawnTime == 1380:
            self.upLeft.add()
            self.upRight.add()
        if self.upRight.spawnTime == 1400 and self.upLeft.spawnTime == 1400:
            self.upLeft.add()
            self.upRight.add()
        if self.downRight.spawnTime == 1435 and self.downLeft.spawnTime == 1435:
            self.downLeft.add()
            self.downRight.add()
        if self.downRight.spawnTime == 1455 and self.downLeft.spawnTime == 1455:
            self.downLeft.add()
            self.downRight.add()

        # verse 2
        if self.upLeft.spawnTime == 1529:
            self.upLeft.add()
        if self.upRight.spawnTime == 34 + 1529:
            self.upRight.add()
        if self.upLeft.spawnTime == 76 + 1529:
            self.upLeft.add()
        if self.upRight.spawnTime == 115 + 1529:
            self.upRight.add()

        if self.downRight.spawnTime == 1529:  # moti
            self.downRight.add()
        if self.upLeft.spawnTime == 180 + 1387 and self.downRight.spawnTime == 180 + 1387:
            self.upLeft.add()
            self.downRight.add()
        if self.upRight.spawnTime == 195 + 1387 and self.downLeft.spawnTime == 195 + 1387:
            self.upRight.add()
            self.downLeft.add()
        if self.downRight.spawnTime == 225 + 1387 and self.downLeft.spawnTime == 225 + 1387:
            self.downLeft.add()
            self.downRight.add()
        if self.upRight.spawnTime == 235 + 1387:  # yes
            self.upRight.add()
        if self.upRight.spawnTime == 260 + 1387:  # yes
            self.upRight.add()

        if self.downLeft.spawnTime == 312 + 1387:  # insti
            self.downLeft.add()
        if self.upRight.spawnTime == 355 + 1387 and self.downLeft.spawnTime == 355 + 1387:
            self.upRight.add()
            self.downLeft.add()
        if self.upLeft.spawnTime == 383 + 1387 and self.downRight.spawnTime == 383 + 1387:
            self.upLeft.add()
            self.downRight.add()
        if self.downRight.spawnTime == 403 + 1387 and self.downLeft.spawnTime == 403 + 1387:
            self.downLeft.add()
            self.downRight.add()
        if self.upLeft.spawnTime == 420 + 1387:  # that's
            self.upLeft.add()
        if self.upLeft.spawnTime == 442 + 1387:  # that's
            self.upLeft.add()

        if self.downLeft.spawnTime == 474 + 1387:
            self.downLeft.add()
        if self.upLeft.spawnTime == 520 + 1387:
            self.upLeft.add()
        if self.upRight.spawnTime == 557 + 1387:
            self.upRight.add()
        if self.downRight.spawnTime == 594 + 1387:
            self.downRight.add()
        if self.downRight.spawnTime == 634 + 1387:
            self.downRight.add()
        if self.upRight.spawnTime == 674 + 1387:
            self.upRight.add()
        if self.upLeft.spawnTime == 713 + 1387:
            self.upLeft.add()
        if self.downLeft.spawnTime == 740 + 1387:
            self.downLeft.add()

        if self.downRight.spawnTime == 752 + 1387 and self.downLeft.spawnTime == 752 + 1387:
            self.downLeft.add()
            self.downRight.add()  # one in a million
        if self.downRight.spawnTime == 805 + 1387 and self.downLeft.spawnTime == 805 + 1387:
            self.downLeft.add()
            self.downRight.add()

        if self.upRight.spawnTime == 835 + 1387 and self.upLeft.spawnTime == 835 + 1387:
            self.upLeft.add()
            self.upRight.add()  # high
        if self.downRight.spawnTime == 865 + 1387 and self.downLeft.spawnTime == 865 + 1387:
            self.downRight.add()
            self.downLeft.add()  # drop
        if self.upRight.spawnTime == 895 + 1387:
            self.upRight.add()
        if self.upRight.spawnTime == 915 + 1387:
            self.upRight.add()
        if self.upRight.spawnTime == 937 + 1387 and self.upLeft.spawnTime == 937 + 1387:
            self.upRight.add()
            self.upLeft.add()
        if self.downRight.spawnTime == 960 + 1387 and self.downLeft.spawnTime == 960 + 1387:
            self.downLeft.add()
            self.downRight.add()

        if self.downRight.spawnTime == 990 + 1387:
            self.downRight.add()
        if self.upRight.spawnTime == 1017 + 1387:
            self.upRight.add()
        if self.upLeft.spawnTime == 1045 + 1387:
            self.upLeft.add()
        if self.downLeft.spawnTime == 1070 + 1387:
            self.downLeft.add()
        if self.downLeft.spawnTime == 1100 + 1387:
            self.downLeft.add()
        if self.upLeft.spawnTime == 1120 + 1387:
            self.upLeft.add()
        if self.upRight.spawnTime == 1140 + 1387:
            self.upRight.add()
        if self.downRight.spawnTime == 1150 + 1387:
            self.downRight.add()  # what it sounds like

        if self.upLeft.spawnTime == 1170 + 1387:
            self.upLeft.add()
        if self.upLeft.spawnTime == 1190 + 1387:
            self.upLeft.add()
        if self.upRight.spawnTime == 1235 + 1387:
            self.upRight.add()
        if self.upRight.spawnTime == 1260 + 1387:
            self.upRight.add()
        if self.downRight.spawnTime == 1285 + 1387:
            self.downRight.add()
        if self.downRight.spawnTime == 1305 + 1387:
            self.downRight.add()
        if self.upLeft.spawnTime == 1335 + 1387:
            self.upLeft.add()
        if self.upLeft.spawnTime == 1355 + 1387:
            self.upLeft.add()

        if self.upRight.spawnTime == 1380 + 1387 and self.upLeft.spawnTime == 1380 + 1387:
            self.upLeft.add()
            self.upRight.add()
        if self.upRight.spawnTime == 1400 + 1387 and self.upLeft.spawnTime == 1400 + 1387:
            self.upLeft.add()
            self.upRight.add()
        if self.downRight.spawnTime == 1435 + 1387 and self.downLeft.spawnTime == 1435 + 1387:
            self.downLeft.add()
            self.downRight.add()
        if self.downRight.spawnTime == 1455 + 1387 and self.downLeft.spawnTime == 1455 + 1387:
            self.downLeft.add()
            self.downRight.add()

        # beat drop
        if self.downLeft.spawnTime == 2870:
            self.downLeft.add()

        self.upLeft.spawn()
        self.upLeft.move()
        self.upRight.spawn()
        self.upRight.move()
        self.downLeft.spawn()
        self.downLeft.move()
        self.downRight.spawn()
        self.downRight.move()
        self.score.display(self.score.score)

        Display_Performance(self.performance)
        # self.performance = ""
