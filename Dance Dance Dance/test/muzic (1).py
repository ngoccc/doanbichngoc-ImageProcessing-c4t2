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
# display_surf = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Dance")
window_width, window_height = pygame.display.get_surface().get_size()
fps = 30
fps_clock = pygame.time.Clock()

#  load images
upLeft = pygame.image.load("E:\\hmm\\images\\UpLeft.png")
upRight = pygame.image.load("E:\\hmm\\images\\UpRight.png")
downLeft = pygame.image.load("E:\\hmm\\images\\DownLeft.png")
downRight = pygame.image.load("E:\\hmm\\images\\DownRight.png")

center = pygame.image.load("E:\\hmm\\images\\Center.png")
glow = pygame.image.load("E:\\hmm\\images\\Glow.png")

# starting positions

posUpLeft = (window_height / 2 - 74, window_height / 2 - 74)
posUpRight = (window_width - (window_height / 2 - 10), window_height / 2 - 74)
posDownLeft = (window_height / 2 - 74, window_height / 2 + 10)
posDownRight = (window_width - (window_height / 2 - 10), window_height / 2 + 10)

#  load music
pygame.mixer.init(44100, -16, 2, 2048)
pygame.mixer.music.load("E:\\C4T\\Image Processing\\Game2\\Lucky-Strike.mp3")
pygame.mixer.music.set_volume(0.5)
# pygame.mixer.music.play(1)

#  starting positions

posUpLeft = (window_height / 2 - 74, window_height / 2 - 74)
posUpRight = (window_width - (window_height / 2 - 10), window_height / 2 - 74)
posDownLeft = (window_height / 2 - 74, window_height / 2 + 10)
posDownRight = (window_width - (window_height / 2 - 10), window_height / 2 + 10)

#  button positions

buttonUpLeft = (10, 10)
buttonUpRight = (window_width - 74, 10)
buttonDownLeft = (10, window_height - 74)
buttonDownRight = (window_width - 74, window_height - 74)


class Point:

    def __init__(self, img, dir, start_pos, speed):
        self.points = []
        self.image = img
        self.direction = dir
        self.start_pos = start_pos
        self.speed = speed
        # self.points.append(list(self.start_pos))
        self.spawnTime = 0

    def move(self):
        # move
        for p in self.points:
            if self.direction == 1:  # upLeft
                if p[0] <= -64 and p[1] <= -64:
                    self.points.remove([p[0], p[1]])
                else:
                    p[0] -= self.speed
                    p[1] -= self.speed
            elif self.direction == 2:  # upRight
                if p[0] >= window_width and p[1] <= -64:
                    self.points.remove([p[0], p[1]])
                else:
                    p[0] += self.speed
                    p[1] -= self.speed
            elif self.direction == 3:  # downLeft
                if p[0] <= - 64 and p[1] >= window_height:
                    self.points.remove([p[0], p[1]])
                else:
                    p[0] -= self.speed
                    p[1] += self.speed
            elif self.direction == 4:  # downRight
                if p[0] >= window_width and p[1] >= window_height:
                    self.points.remove([p[0], p[1]])
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


def distance(a, b, c, d):
    return math.sqrt((a - c) ** 2 + (b - d) ** 2)


class Game:
    def __init__(self, speed=5):
        self.speed = speed
        point_speed = self.speed
        # points
        self.upLeft = Point(upLeft, 1, posUpLeft, point_speed)
        self.upRight = Point(upRight, 2, posUpRight, point_speed)
        self.downLeft = Point(downLeft, 3, posDownLeft, point_speed)
        self.downRight = Point(downRight, 4, posDownRight, point_speed)

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
        # if self.downRight.spawnTime == 2895:  # taking
        #     self.downRight.add()
        # if self.downLeft.spawnTime == 2915:  # pain
        #     self.downLeft.add()
        # if self.upRight.spawnTime == 2930 and self.upLeft.spawnTime == 2930:
        #     self.upLeft.add()
        #     self.upRight.add()  # away
        # if self.downRight.spawnTime == 2955:  # shaking
        #     self.downRight.add()
        # if self.downLeft.spawnTime == 2980:  # earth
        #     self.downLeft.add()
        # if self.upLeft.spawnTime == 3000:
        #     self.upLeft.add()
        # if self.upRight.spawnTime == 3020:
        #     self.upRight.add()
        # if self.downRight.spawnTime == 3040:
        #     self.downRight.add()
        # if self.downRight.spawnTime == 2980:  # eh
        #     self.downRight.add()
        # if self.upRight.spawnTime == 3000:
        #     self.upRight.add()
        # if self.upLeft.spawnTime == 3020:
        #     self.upLeft.add()
        # if self.downLeft.spawnTime == 3040:
        #     self.downLeft.add()
        #
        #     # verse 3:
        if self.upRight.spawnTime == 3700 and self.upLeft.spawnTime == 3700:
            self.upLeft.add()
            self.upRight.add()  # high
        # if self.downRight.spawnTime == 865 + 1387 and self.downLeft.spawnTime == 865 + 1387:
        #     self.downRight.add()
        #     self.downLeft.add()  # drop
        # if self.upRight.spawnTime == 895 + 1387:
        #     self.upRight.add()
        # if self.upRight.spawnTime == 915 + 1387:
        #     self.upRight.add()
        # if self.upRight.spawnTime == 937 + 1387 and self.upLeft.spawnTime == 937 + 1387:
        #     self.upRight.add()
        #     self.upLeft.add()
        # if self.downRight.spawnTime == 960 + 1387 and self.downLeft.spawnTime == 960 + 1387:
        #     self.downLeft.add()
        #     self.downRight.add()
        #
        # if self.downRight.spawnTime == 990 + 1387:
        #     self.downRight.add()
        # if self.upRight.spawnTime == 1017 + 1387:
        #     self.upRight.add()
        # if self.upLeft.spawnTime == 1045 + 1387:
        #     self.upLeft.add()
        # if self.downLeft.spawnTime == 1070 + 1387:
        #     self.downLeft.add()
        # if self.downLeft.spawnTime == 1100 + 1387:
        #     self.downLeft.add()
        # if self.upLeft.spawnTime == 1120 + 1387:
        #     self.upLeft.add()
        # if self.upRight.spawnTime == 1140 + 1387:
        #     self.upRight.add()
        # if self.downRight.spawnTime == 1150 + 1387:
        #     self.downRight.add()  # what it sounds like
        #
        # if self.upLeft.spawnTime == 1170 + 1387:
        #     self.upLeft.add()
        # if self.upLeft.spawnTime == 1190 + 1387:
        #     self.upLeft.add()
        # if self.upRight.spawnTime == 1235 + 1387:
        #     self.upRight.add()
        # if self.upRight.spawnTime == 1260 + 1387:
        #     self.upRight.add()
        # if self.downRight.spawnTime == 1285 + 1387:
        #     self.downRight.add()
        # if self.downRight.spawnTime == 1305 + 1387:
        #     self.downRight.add()
        # if self.upLeft.spawnTime == 1335 + 1387:
        #     self.upLeft.add()
        # if self.upLeft.spawnTime == 1355 + 1387:
        #     self.upLeft.add()
        #
        # if self.upRight.spawnTime == 1380 + 1387 and self.upLeft.spawnTime == 1380 + 1387:
        #     self.upLeft.add()
        #     self.upRight.add()
        # if self.upRight.spawnTime == 1400 + 1387 and self.upLeft.spawnTime == 1400 + 1387:
        #     self.upLeft.add()
        #     self.upRight.add()
        # if self.downRight.spawnTime == 1435 + 1387 and self.downLeft.spawnTime == 1435 + 1387:
        #     self.downLeft.add()
        #     self.downRight.add()
        # if self.downRight.spawnTime == 1455 + 1387 and self.downLeft.spawnTime == 1455 + 1387:
        #     self.downLeft.add()
        #     self.downRight.add()

        self.upLeft.spawn()
        self.upLeft.move()
        self.upRight.spawn()
        self.upRight.move()
        self.downLeft.spawn()
        self.downLeft.move()
        self.downRight.spawn()
        self.downRight.move()


def Draw_Elements():
    display_surf.blit(upLeft, buttonUpLeft)
    display_surf.blit(upRight, buttonUpRight)
    display_surf.blit(downLeft, buttonDownLeft)
    display_surf.blit(downRight, buttonDownRight)
    display_surf.blit(center, posUpLeft)  # upLeft
    display_surf.blit(center, posUpRight)  # upRight
    display_surf.blit(center, posDownLeft)  # downLeft
    display_surf.blit(center, posDownRight)  # downRight


def main():
    pygame.init()
    game = Game()
    cam = webcam.Webcam()
    cam.thread_webcam()

    while True:
        frame = cam.get_currentFrame()
        frame = cv2.resize(frame, (window_width, window_height), cv2.INTER_CUBIC)
        #  connect webcam

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        display_surf.blit(frame, (0, 0))

        Draw_Elements()
        game.update()
        pygame.display.update()
        fps_clock.tick(fps)


if __name__ == '__main__':
    main()
