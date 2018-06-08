import pygame
from pygame.locals import *
import cv2
import numpy as np
import math
import webcam

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 255, 255)
MAGENTA = (255, 0, 144)
display_surf = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# display_surf = pygame.display.set_mode((800, 800))
pygame.display.set_caption("dancing2")
window_width, window_height = pygame.display.get_surface().get_size()
fps = 30
fps_clock = pygame.time.Clock()

# load images
upLeft = pygame.image.load("E:\\hmm\\images\\UpLeft.png")
upRight = pygame.image.load("E:\\hmm\\images\\UpRight.png")
downLeft = pygame.image.load("E:\\hmm\\images\\DownLeft.png")
downRight = pygame.image.load("E:\\hmm\\images\\DownRight.png")

upLeftActive = pygame.image.load("E:\\hmm\\images\\UpLeftActive.png")
upRightActive = pygame.image.load("E:\\hmm\\images\\UpRightActive.png")
downLeftActive = pygame.image.load("E:\\hmm\\images\\DownLeftActive.png")
downRightActive = pygame.image.load("E:\\hmm\\images\\DownRightActive.png")

center = pygame.image.load("E:\\hmm\\images\\Center.png")
glow = pygame.image.load("E:\\hmm\\images\\Glow.png")

# load music
pygame.mixer.init(44100, -16, 2, 2048)

# starting positions

posUpLeft = (window_height / 2 - 74, window_height / 2 - 74)
posUpRight = (window_width - (window_height / 2 - 10), window_height / 2 - 74)
posDownLeft = (window_height / 2 - 74, window_height / 2 + 10)
posDownRight = (window_width - (window_height / 2 - 10), window_height / 2 + 10)

# button positions

buttonUpLeft = (10, 10)
buttonUpRight = (window_width - 74, 10)
buttonDownLeft = (10, window_height - 74)
buttonDownRight = (window_width - 74, window_height - 74)

# start menu
title = pygame.image.load("E:\\C4T\Image Processing\\Game2\\images\\start\\text_startmenu.png")
title = pygame.transform.scale(title, (window_width, window_height))
start = pygame.image.load("E:\\C4T\\Image Processing\\Game2\\images\\start\\Press Start.png")

# result
result = pygame.image.load("E:\\C4T\\Image Processing\\Game2\\images\\close\\result.png")
result = pygame.transform.scale(result, (window_width, window_height))
rank_S = pygame.image.load("E:\\C4T\\Image Processing\\Game2\\images\\ranking\\S.png")
rank_A = pygame.image.load("E:\\C4T\\Image Processing\\Game2\\images\\ranking\\A.png")
rank_B = pygame.image.load("E:\\C4T\\Image Processing\\Game2\\images\\ranking\\B.png")
rank_C = pygame.image.load("E:\\C4T\\Image Processing\\Game2\\images\\ranking\\C.png")
rank_D = pygame.image.load("E:\\C4T\\Image Processing\\Game2\\images\\ranking\\D.png")
rank_F = pygame.image.load("E:\\C4T\\Image Processing\\Game2\\images\\ranking\\F.png")


def Start():
    display_surf.blit(title, (0, 0))
    display_surf.blit(start, (350, 450))


def Result(p, g, b, m, s):
    pygame.mixer.music.load("E:\\C4T\\Image Processing\\Game2\\song\\close-song.mp3")
    pygame.mixer.music.play(1)
    while True:
        display_surf.blit(result, (0, 0))
        font = pygame.font.Font('Bolt.ttf', 45)
        perfect = font.render('%s' % (p), True, WHITE)
        display_surf.blit(perfect, (1020, 160))
        great = font.render('%s' % (g), True, WHITE)
        display_surf.blit(great, (1020, 225))
        bad = font.render('%s' % (b), True, WHITE)
        display_surf.blit(bad, (1020, 290))
        miss = font.render('%s' % (m), True, WHITE)
        display_surf.blit(miss, (1020, 357))
        score = font.render('%s' % (s), True, WHITE)
        display_surf.blit(score, (980, 425))

        # ranking
        if s >= 40000:
            rank = rank_S
        elif s >= 35000:
            rank = rank_A
        elif s >= 25000:
            rank = rank_B
        elif s >= 15000:
            rank = rank_C
        elif s >= 5000:
            rank = rank_D
        elif s >= 1000:
            rank = rank_F
        display_surf.blit(rank, (500, 500))
        pygame.display.update()


class Point:

    def __init__(self, img, dir, start_pos, speed):
        self.points = []
        self.image = img
        self.direction = dir
        self.start_pos = start_pos
        self.speed = speed
        # self.points.append(list(self.start_pos))
        self.spawnTime = 0
        self.isMissed = False

    def move(self):
        # move
        for p in self.points:
            if self.direction == 1:  # upLeft
                if p[0] <= -64 and p[1] <= -64:
                    self.points.remove([p[0], p[1]])
                    self.isMissed = True
                else:
                    p[0] -= self.speed
                    p[1] -= self.speed
            elif self.direction == 2:  # upRight
                if p[0] >= window_width and p[1] <= -64:
                    self.points.remove([p[0], p[1]])
                    self.isMissed = True
                else:
                    p[0] += self.speed
                    p[1] -= self.speed
            elif self.direction == 3:  # downLeft
                if p[0] <= - 64 and p[1] >= window_height:
                    self.points.remove([p[0], p[1]])
                    self.isMissed = True
                else:
                    p[0] -= self.speed
                    p[1] += self.speed
            elif self.direction == 4:  # downRight
                if p[0] >= window_width and p[1] >= window_height:
                    self.points.remove([p[0], p[1]])
                    self.isMissed = True
                else:
                    p[0] += self.speed
                    p[1] += self.speed

        # draw
        for p in self.points:
            display_surf.blit(self.image, (p[0], p[1]))

    def add(self):
        self.points.append(list(self.start_pos))

    def spawn(self):
        self.spawnTime += 1


class Scoreboard:
    def __init__(self, fontSize=70, score=0):
        self.x = window_width / 2
        self.y = 20
        self.score = score
        self.font = pygame.font.Font('Bolt.ttf', fontSize)

    def display(self, score):
        result_srf = self.font.render('%s' % (score), True, BLUE)
        result_rect_w = result_srf.get_rect().width
        display_surf.blit(result_srf, (self.x - result_rect_w / 2, self.y))


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
            pygame.mixer.music.load("E:\\C4T\\Image Processing\\Game2\\Lucky-Strike.mp3")
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

        if self.downLeft.spawnTime == 465:
            self.downLeft.add()
        if self.upLeft.spawnTime == 511:
            self.upLeft.add()
        if self.upRight.spawnTime == 548:
            self.upRight.add()
        if self.downRight.spawnTime == 585:
            self.downRight.add()
        if self.downRight.spawnTime == 629:
            self.downRight.add()
        if self.upRight.spawnTime == 669:
            self.upRight.add()
        if self.upLeft.spawnTime == 709:
            self.upLeft.add()
        if self.downLeft.spawnTime == 735:
            self.downLeft.add()
        #
        if self.downRight.spawnTime == 760 and self.downLeft.spawnTime == 760:
            self.downLeft.add()
            self.downRight.add()
        if self.downRight.spawnTime == 805 and self.downLeft.spawnTime == 805:
            self.downLeft.add()
            self.downRight.add()

        if self.upRight.spawnTime == 835 and self.upLeft.spawnTime == 835:  # high
            self.upRight.add()
            self.upLeft.add()
        if self.downRight.spawnTime == 860 and self.downLeft.spawnTime == 860:  # drop
            self.downLeft.add()
            self.downRight.add()

        if self.downRight.spawnTime == 890:
            self.downRight.add()
        if self.upRight.spawnTime == 917:
            self.upRight.add()
        if self.upLeft.spawnTime == 945:
            self.upLeft.add()
        if self.downLeft.spawnTime == 967:
            self.downLeft.add()
        if self.downLeft.spawnTime == 1000:
            self.downLeft.add()
        if self.upLeft.spawnTime == 1020:
            self.upLeft.add()
        if self.upRight.spawnTime == 1040:
            self.upRight.add()
        if self.downRight.spawnTime == 1050:
            self.downRight.add()

        if self.upLeft.spawnTime == 1150:
            self.upLeft.add()
        if self.upLeft.spawnTime == 1170:
            self.upLeft.add()
        if self.upRight.spawnTime == 1215:
            self.upRight.add()
        if self.upRight.spawnTime == 1235:
            self.upRight.add()
        if self.downRight.spawnTime == 1265:
            self.downRight.add()
        if self.downRight.spawnTime == 1285:
            self.downRight.add()
        if self.upLeft.spawnTime == 1315:
            self.upLeft.add()
        if self.upLeft.spawnTime == 1335:
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
        if self.downRight.spawnTime == 1500:  # elevator
            self.downRight.add()
        if self.upLeft.spawnTime == 180 + 1363 and self.downRight.spawnTime == 180 + 1363:
            self.upLeft.add()
            self.downRight.add()
        if self.upRight.spawnTime == 195 + 1363 and self.downLeft.spawnTime == 195 + 1363:
            self.upRight.add()
            self.downLeft.add()
        if self.downRight.spawnTime == 225 + 1363 and self.downLeft.spawnTime == 225 + 1363:
            self.downLeft.add()
            self.downRight.add()
        if self.upRight.spawnTime == 235 + 1363:  # down
            self.upRight.add()
        if self.upRight.spawnTime == 260 + 1363:  # down
            self.upRight.add()
        #
        if self.downLeft.spawnTime == 312 + 1363:  #
            self.downLeft.add()
        if self.upRight.spawnTime == 345 + 1363 and self.downLeft.spawnTime == 345 + 1363:
            self.upRight.add()
            self.downLeft.add()
        if self.upLeft.spawnTime == 373 + 1363 and self.downRight.spawnTime == 373 + 1363:
            self.upLeft.add()
            self.downRight.add()
        if self.downRight.spawnTime == 393 + 1363 and self.downLeft.spawnTime == 393 + 1363:
            self.downLeft.add()
            self.downRight.add()
        if self.upLeft.spawnTime == 410 + 1363:  # now
            self.upLeft.add()
        if self.upLeft.spawnTime == 432 + 1363:  # now
            self.upLeft.add()

        if self.downLeft.spawnTime == 465 + 1363:
            self.downLeft.add()
        if self.upLeft.spawnTime == 511 + 1363:
            self.upLeft.add()
        if self.upRight.spawnTime == 548 + 1363:
            self.upRight.add()
        if self.downRight.spawnTime == 585 + 1363:
            self.downRight.add()
        if self.downRight.spawnTime == 625 + 1363:
            self.downRight.add()
        if self.upRight.spawnTime == 665 + 1363:
            self.upRight.add()
        if self.upLeft.spawnTime == 704 + 1363:
            self.upLeft.add()
        if self.downLeft.spawnTime == 731 + 1363:
            self.downLeft.add()
        if self.downRight.spawnTime == 743 + 1363 and self.downLeft.spawnTime == 752 + 1363:
            self.downLeft.add()
            self.downRight.add()  # one in a million
        if self.downRight.spawnTime == 796 + 1363 and self.downLeft.spawnTime == 805 + 1363:
            self.downLeft.add()
            self.downRight.add()

        if self.upRight.spawnTime == 835 + 1363 and self.upLeft.spawnTime == 835 + 1363:
            self.upLeft.add()
            self.upRight.add()  # high
        if self.downRight.spawnTime == 865 + 1363 and self.downLeft.spawnTime == 865 + 1363:
            self.downRight.add()
            self.downLeft.add()  # drop
        if self.upRight.spawnTime == 895 + 1363:
            self.upRight.add()
        if self.upRight.spawnTime == 915 + 1363:
            self.upRight.add()
        if self.upRight.spawnTime == 937 + 1363 and self.upLeft.spawnTime == 937 + 1363:
            self.upRight.add()
            self.upLeft.add()
        if self.downRight.spawnTime == 960 + 1363 and self.downLeft.spawnTime == 960 + 1363:
            self.downLeft.add()
            self.downRight.add()

        if self.downRight.spawnTime == 990 + 1363:
            self.downRight.add()
        if self.upRight.spawnTime == 1017 + 1363:
            self.upRight.add()
        if self.upLeft.spawnTime == 1045 + 1363:
            self.upLeft.add()
        if self.downLeft.spawnTime == 1070 + 1363:
            self.downLeft.add()
        if self.downLeft.spawnTime == 1100 + 1363:
            self.downLeft.add()
        if self.upLeft.spawnTime == 1120 + 1363:
            self.upLeft.add()
        if self.upRight.spawnTime == 1140 + 1363:
            self.upRight.add()
        if self.downRight.spawnTime == 1150 + 1363:
            self.downRight.add()  # what it sounds like

        if self.upLeft.spawnTime == 1170 + 1363:
            self.upLeft.add()
        if self.upLeft.spawnTime == 1190 + 1363:
            self.upLeft.add()
        if self.upRight.spawnTime == 1235 + 1363:
            self.upRight.add()
        if self.upRight.spawnTime == 1260 + 1387:
            self.upRight.add()
        if self.downRight.spawnTime == 1285 + 1363:
            self.downRight.add()
        if self.downRight.spawnTime == 1305 + 1363:
            self.downRight.add()
        if self.upLeft.spawnTime == 1335 + 1363:
            self.upLeft.add()
        if self.upLeft.spawnTime == 1355 + 1363:
            self.upLeft.add()

        if self.upRight.spawnTime == 1380 + 1363 and self.upLeft.spawnTime == 1380 + 1363:
            self.upLeft.add()
            self.upRight.add()
        if self.upRight.spawnTime == 1400 + 1363 and self.upLeft.spawnTime == 1400 + 1363:
            self.upLeft.add()
            self.upRight.add()
        if self.downRight.spawnTime == 1435 + 1363 and self.downLeft.spawnTime == 1435 + 1363:
            self.downLeft.add()
            self.downRight.add()
        if self.downRight.spawnTime == 1455 + 1363 and self.downLeft.spawnTime == 1455 + 1363:
            self.downLeft.add()
            self.downRight.add()

            # beat drop
        if self.downLeft.spawnTime == 2845:  # hey
            self.downLeft.add()
        if self.downRight.spawnTime == 2865:  # taking
            self.downRight.add()
        if self.downLeft.spawnTime == 2885:  # pain
            self.downLeft.add()
        if self.upRight.spawnTime == 2915 and self.upLeft.spawnTime == 2915:
            self.upLeft.add()
            self.upRight.add()  # away
        if self.downRight.spawnTime == 2945:  # shaking
            self.downRight.add()
        if self.downLeft.spawnTime == 2975:  # earth
            self.downLeft.add()
        if self.upLeft.spawnTime == 3000:
            self.upLeft.add()
        if self.upRight.spawnTime == 3025:
            self.upRight.add()
        if self.downRight.spawnTime == 3050:
            self.downRight.add()
        if self.downRight.spawnTime == 3095:  # eh
            self.downRight.add()
        if self.upRight.spawnTime == 3115:
            self.upRight.add()
        if self.upLeft.spawnTime == 3130:
            self.upLeft.add()
        if self.downLeft.spawnTime == 3145:
            self.downLeft.add()

        if self.downLeft.spawnTime == 3165:  # hey
            self.downLeft.add()
        if self.downRight.spawnTime == 2865 + 320:  # taking
            self.downRight.add()
        if self.downLeft.spawnTime == 2885 + 320:  # pain
            self.downLeft.add()
        if self.upRight.spawnTime == 2915 + 320 and self.upLeft.spawnTime == 2915 + 320:
            self.upLeft.add()
            self.upRight.add()  # away
        if self.downRight.spawnTime == 2945 + 320:  # shaking
            self.downRight.add()
        if self.downLeft.spawnTime == 2975 + 320:  # earth
            self.downLeft.add()
        if self.upLeft.spawnTime == 3000 + 320:
            self.upLeft.add()
        if self.upRight.spawnTime == 3025 + 320:
            self.upRight.add()
        if self.downRight.spawnTime == 3050 + 320:
            self.downRight.add()
        if self.downRight.spawnTime == 3095 + 320:  # eh
            self.downRight.add()
        if self.upRight.spawnTime == 3115 + 320:
            self.upRight.add()
        if self.upLeft.spawnTime == 3130 + 320:
            self.upLeft.add()
        if self.downLeft.spawnTime == 3145 + 320:
            self.downLeft.add()

            # verse 3:
        if self.upRight.spawnTime == 3700 and self.upLeft.spawnTime == 3700:
            self.upLeft.add()
            self.upRight.add()  # high
        if self.downRight.spawnTime == 865 + 1387 + 1502 and self.downLeft.spawnTime == 865 + 1387 + 1502:
            self.downRight.add()
            self.downLeft.add()  # drop
        if self.upRight.spawnTime == 895 + 1387 + 1502:
            self.upRight.add()
        if self.upRight.spawnTime == 915 + 1387 + 1502:
            self.upRight.add()
        if self.upRight.spawnTime == 937 + 1387 + 1502 and self.upLeft.spawnTime == 937 + 1387 + 1502:
            self.upRight.add()
            self.upLeft.add()
        if self.downRight.spawnTime == 960 + 1387 + 1502 and self.downLeft.spawnTime == 960 + 1387 + 1502:
            self.downLeft.add()
            self.downRight.add()

        if self.downLeft.spawnTime == 990 + 1387 + 1502:
            self.downLeft.add()
        if self.upRight.spawnTime == 1017 + 1387 + 1502:
            self.upRight.add()
        if self.upLeft.spawnTime == 1045 + 1387 + 1502:
            self.upLeft.add()
        if self.downRight.spawnTime == 1070 + 1387 + 1502:
            self.downRight.add()
        if self.downLeft.spawnTime == 1100 + 1387 + 1502 and self.upRight.spawnTime == 1100 + 1387 + 1502:
            self.downLeft.add()
            self.upRight.add()
        if self.upLeft.spawnTime == 1120 + 1387 + 1502 and self.upRight.spawnTime == 1120 + 1387 + 1502:
            self.upLeft.add()
        if self.downRight.spawnTime == 1140 + 1387 + 1502 and self.downLeft.spawnTime == 1140 + 1387 + 1502:
            self.upRight.add()
        if self.downRight.spawnTime == 1150 + 1387 + 1502 and self.upLeft.spawnTime == 1150 + 1387 + 1502:
            self.downRight.add()  # what it sounds like

        if self.upLeft.spawnTime == 1170 + 1387 + 1502:
            self.upLeft.add()
        if self.upLeft.spawnTime == 1190 + 1387 + 1502:
            self.upLeft.add()
        if self.upRight.spawnTime == 1235 + 1387 + 1502:
            self.upRight.add()
        if self.upRight.spawnTime == 1260 + 1387 + 1502:
            self.upRight.add()
        if self.downRight.spawnTime == 1285 + 1387 + 1502:
            self.downRight.add()
        if self.downRight.spawnTime == 1305 + 1387 + 1502:
            self.downRight.add()
        if self.upLeft.spawnTime == 1335 + 1387 + 1502 and self.upRight.spawnTime == 1335 + 1387 + 1502:
            self.upLeft.add()
        if self.upLeft.spawnTime == 1355 + 1387 + 1502 and self.upRight.spawnTime == 1355 + 1387 + 1502:
            self.upLeft.add()

        if self.upRight.spawnTime == 1380 + 1387 + 1502 and self.upLeft.spawnTime == 1380 + 1387 + 1502:
            self.upLeft.add()
            self.upRight.add()
        if self.upRight.spawnTime == 1400 + 1387 + 1502 and self.upLeft.spawnTime == 1400 + 1387 + 1502:
            self.upLeft.add()
            self.upRight.add()
        if self.downRight.spawnTime == 1435 + 1387 + 1502 and self.downLeft.spawnTime == 1435 + 1387 + 1502:
            self.downLeft.add()
            self.downRight.add()
        if self.downRight.spawnTime == 1455 + 1387 + 1502 and self.downLeft.spawnTime == 1455 + 1387 + 1502:
            self.downLeft.add()
            self.downRight.add()

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


def Distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# distance from button to center
d = Distance(buttonUpLeft[0], buttonUpLeft[1], posUpLeft[0], posUpLeft[1])


def Draw_Elements():
    display_surf.blit(upLeft, buttonUpLeft)
    display_surf.blit(upRight, buttonUpRight)
    display_surf.blit(downLeft, buttonDownLeft)
    display_surf.blit(downRight, buttonDownRight)
    display_surf.blit(center, posUpLeft)  # upLeft
    display_surf.blit(center, posUpRight)  # upRight
    display_surf.blit(center, posDownLeft)  # downLeft
    display_surf.blit(center, posDownRight)  # downRight


def Display_Performance(s):
    font = pygame.font.Font('Bolt.ttf', 50)
    result_srf = font.render('%s' % (s), True, MAGENTA)
    result_rect_w = result_srf.get_rect().width
    result_rect_h = result_srf.get_rect().height
    display_surf.blit(result_srf, (window_width / 2 - result_rect_w / 2, window_height / 2 - result_rect_h / 2))


def main():
    game = Game()
    cam = webcam.Webcam()
    cam.thread_webcam()
    SONG_END = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(SONG_END)

    while True:
        frame = cam.get_currentFrame()
        frame = cv2.resize(frame, (window_width, window_height), cv2.INTER_CUBIC)

        # connect webcam
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        display_surf.blit(frame, (0, 0))
        Draw_Elements()

        if game.upLeft.isMissed:
            game.performance = "MISS"
            game.miss += 1
            game.upLeft.isMissed = False
        elif game.upRight.isMissed:
            game.performance = "MISS"
            game.miss += 1
            game.upRight.isMissed = False
        elif game.downLeft.isMissed:
            game.performance = "MISS"
            game.miss += 1
            game.downLeft.isMissed = False
        elif game.downRight.isMissed:
            game.performance = "MISS"
            game.miss += 1
            game.downRight.isMissed = False

        if cam.get_pos(buttonUpLeft[1], buttonUpLeft[0]):
            # upLeft
            if len(game.upLeft.points) != 0:
                game.upLeft.isMissed = False
                currentPoint_x = game.upLeft.points[0][0]
                currentPoint_y = game.upLeft.points[0][1]
                button_x = buttonUpLeft[0]
                button_y = buttonUpLeft[1]
                distance = Distance(currentPoint_x, currentPoint_y, button_x, button_y)
                if currentPoint_x >= 10 and currentPoint_y >= 10:  # inside
                    if distance <= d / 3:
                        game.score.score += 200
                        game.performance = "PERFECT"
                        game.perfect += 1
                    elif distance <= 2 * d / 3:
                        game.score.score += 100
                        game.performance = "GREAT"
                        game.great += 1
                    else:
                        game.performance = "BAD"
                        game.bad += 1
                    display_surf.blit(upLeftActive, buttonUpLeft)
                    display_surf.blit(glow, buttonUpLeft)
                    game.upLeft.points.remove([currentPoint_x, currentPoint_y])

        if cam.get_pos(buttonUpRight[1], buttonUpRight[0]):
            if len(game.upRight.points) != 0:
                game.upRight.isMissed = False
                currentPoint_x = game.upRight.points[0][0]
                currentPoint_y = game.upRight.points[0][1]
                button_x = buttonUpRight[0]
                button_y = buttonUpRight[1]
                distance = Distance(currentPoint_x, currentPoint_y, button_x, button_y)
                if currentPoint_x <= window_width - 74 and currentPoint_y >= 10:  # inside
                    if distance <= d / 3:
                        game.score.score += 200
                        game.performance = "PERFECT"
                    elif distance <= 2 * d / 3:
                        game.score.score += 100
                        game.performance = "GREAT"
                    else:
                        game.performance = "BAD"
                    display_surf.blit(upRightActive, buttonUpRight)
                    display_surf.blit(glow, buttonUpRight)
                    game.upRight.points.remove([currentPoint_x, currentPoint_y])

        if cam.get_pos(buttonDownLeft[1], buttonDownLeft[0]):
            if len(game.downLeft.points) != 0:
                game.downLeft.isMissed = False
                currentPoint_x = game.downLeft.points[0][0]
                currentPoint_y = game.downLeft.points[0][1]
                button_x = buttonDownLeft[0]
                button_y = buttonDownLeft[1]
                distance = Distance(currentPoint_x, currentPoint_y, button_x, button_y)
                if currentPoint_x >= 10 and currentPoint_y <= window_height - 74:  # inside
                    if distance <= d / 3:
                        game.score.score += 200
                        game.performance = "PERFECT"
                    elif distance <= 2 * d / 3:
                        game.score.score += 100
                        game.performance = "GREAT"
                    else:
                        game.performance = "BAD"
                    display_surf.blit(downLeftActive, buttonDownLeft)
                    display_surf.blit(glow, buttonDownLeft)
                    game.downLeft.points.remove([currentPoint_x, currentPoint_y])

        if cam.get_pos(buttonDownRight[1], buttonDownRight[0]):
            if len(game.downRight.points) != 0:
                game.downRight.isMissed = False
                currentPoint_x = game.downRight.points[0][0]
                currentPoint_y = game.downRight.points[0][1]
                button_x = buttonDownRight[0]
                button_y = buttonDownRight[1]
                distance = Distance(currentPoint_x, currentPoint_y, button_x, button_y)
                if currentPoint_x <= window_width - 74 and currentPoint_y <= window_height - 74:  # inside
                    if distance <= d / 3:
                        game.score.score += 200
                        game.performance = "PERFECT"
                    elif distance <= 2 * d / 3:
                        game.score.score += 100
                        game.performance = "GREAT"
                    else:
                        game.performance = "BAD"
                    display_surf.blit(downRightActive, buttonDownRight)
                    display_surf.blit(glow, buttonDownRight)
                    game.downRight.points.remove([currentPoint_x, currentPoint_y])
        for event in pygame.event.get():
            if event.type == SONG_END:
                Result(game.perfect, game.great, game.bad, game.miss, game.score.score)
        game.update()
        pygame.display.update()
        fps_clock.tick(fps)


def Init():
    pygame.init()
    cam = webcam.Webcam()
    cam.thread_webcam()
    pygame.mixer.music.load("E:\\C4T\\Image Processing\\Game2\\song\\opening-song.mp3")
    pygame.mixer.music.play(1)

    while True:
        frame = cam.get_currentFrame()
        frame = cv2.resize(frame, (window_width, window_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)

        display_surf.blit(frame, (0, 0))
        Start()  # start menu

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 350 + 500 > mouse[0] > 500 and 800 > mouse[1] > 500:
                    pygame.mixer.music.stop()
                    main()
        pygame.display.update()


Init()
