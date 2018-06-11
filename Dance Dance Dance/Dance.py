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
fps = 60
fps_clock = pygame.time.Clock()

# load images
upLeft = pygame.image.load("images\\buttons\\UpLeft.png")
upRight = pygame.image.load("images\\buttons\\UpRight.png")
downLeft = pygame.image.load("images\\buttons\\DownLeft.png")
downRight = pygame.image.load("images\\buttons\\DownRight.png")

center = pygame.image.load("images\\buttons\\Center.png")
glow = pygame.image.load("images\\buttons\\Glow.png")

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
        if s >= 36000:
            rank = rank_S
        elif s >= 35000:
            rank = rank_A
        elif s >= 25000:
            rank = rank_B
        elif s >= 15000:
            rank = rank_C
        elif s >= 5000:
            rank = rank_D
        else:
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
    def __init__(self, speed=15):
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
            pygame.mixer.music.load("song\\Lucky-Strike.mp3")
            pygame.mixer.music.play(1)

            # verse 1
        if self.upLeft.spawnTime == 0:
            self.upLeft.add()
        if self.upRight.spawnTime == 16:
            self.upRight.add()
        if self.upLeft.spawnTime == 30:
            self.upLeft.add()
        if self.upRight.spawnTime == 45:
            self.upRight.add()
        if self.downRight.spawnTime == 54:  # moti
            self.downRight.add()
        if self.upLeft.spawnTime == 68 and self.downRight.spawnTime == 68:
            self.upLeft.add()
            self.downRight.add()
        if self.upRight.spawnTime == 70 and self.downLeft.spawnTime == 70:
            self.upRight.add()
            self.downLeft.add()
        if self.downRight.spawnTime == 78 and self.downLeft.spawnTime == 78:
            self.downLeft.add()
            self.downRight.add()
        if self.upRight.spawnTime == 85:  # yes
            self.upRight.add()
        if self.upRight.spawnTime == 92:  # yes
            self.upRight.add()

        if self.downLeft.spawnTime == 109:  # insti
            self.downLeft.add()
        if self.upRight.spawnTime == 127 and self.downLeft.spawnTime == 127:
            self.upRight.add()
            self.downLeft.add()
        if self.upLeft.spawnTime == 136 and self.downRight.spawnTime == 136:
            self.upLeft.add()
            self.downRight.add()
        if self.downRight.spawnTime == 141 and self.downLeft.spawnTime == 141:
            self.downLeft.add()
            self.downRight.add()
        if self.upLeft.spawnTime == 145:  # that's
            self.upLeft.add()
        if self.upLeft.spawnTime == 154:  # that's
            self.upLeft.add()

        if self.downLeft.spawnTime == 161:
            self.downLeft.add()
        if self.upLeft.spawnTime == 177:
            self.upLeft.add()
        if self.upRight.spawnTime == 195:
            self.upRight.add()
        if self.downRight.spawnTime == 209:
            self.downRight.add()

        if self.downRight.spawnTime == 227:
            self.downRight.add()
        if self.upRight.spawnTime == 243:
            self.upRight.add()
        if self.upLeft.spawnTime == 254:
            self.upLeft.add()
        if self.downLeft.spawnTime == 262:
            self.downLeft.add()
        if self.downRight.spawnTime == 273 and self.downLeft.spawnTime == 273:
            self.downLeft.add()
            self.downRight.add()

        if self.downRight.spawnTime == 288 and self.downLeft.spawnTime == 288:
            self.downLeft.add()
            self.downRight.add()

        if self.upRight.spawnTime == 298 and self.upLeft.spawnTime == 298:  # high
            self.upRight.add()
            self.upLeft.add()
        if self.downRight.spawnTime == 309 and self.downLeft.spawnTime == 309:  # drop
            self.downLeft.add()
            self.downRight.add()

        if self.downRight.spawnTime == 320:  # drop me
            self.downRight.add()
        if self.upRight.spawnTime == 328:  # drop me
            self.upRight.add()
        if self.upLeft.spawnTime == 336:  # drop me
            self.upLeft.add()
        if self.downLeft.spawnTime == 344:  # drop me
            self.downLeft.add()

        if self.downLeft.spawnTime == 360:
            self.downLeft.add()
        if self.upLeft.spawnTime == 368:
            self.upLeft.add()
        if self.upRight.spawnTime == 376:
            self.upRight.add()
        if self.downRight.spawnTime == 384:
            self.downRight.add()

        if self.upLeft.spawnTime == 413:
            self.upLeft.add()
        if self.upLeft.spawnTime == 418:
            self.upLeft.add()
        if self.upRight.spawnTime == 430 + 5:
            self.upRight.add()
        if self.upRight.spawnTime == 436 + 5:
            self.upRight.add()
        if self.downRight.spawnTime == 448 + 10:
            self.downRight.add()
        if self.downRight.spawnTime == 454 + 10:
            self.downRight.add()
        if self.upLeft.spawnTime == 466 + 10:
            self.upLeft.add()
        if self.upLeft.spawnTime == 472 + 10:
            self.upLeft.add()

        if self.upRight.spawnTime == 490 + 3 and self.upLeft.spawnTime == 490 + 3:
            self.upLeft.add()
            self.upRight.add()
        if self.upRight.spawnTime == 496 + 5 and self.upLeft.spawnTime == 496 + 5:
            self.upLeft.add()
            self.upRight.add()
        if self.downRight.spawnTime == 504 + 5 and self.downLeft.spawnTime == 504 + 5:
            self.downLeft.add()
            self.downRight.add()
        if self.downRight.spawnTime == 510 + 5 and self.downLeft.spawnTime == 510 + 5:
            self.downLeft.add()
            self.downRight.add()

        # verse 2
        if self.downRight.spawnTime == 537:  # elevator
            self.downRight.add()

        if self.upLeft.spawnTime == 68 + 477 and self.downRight.spawnTime == 70 + 477:
            self.upLeft.add()
            self.downRight.add()
        if self.upRight.spawnTime == 70 + 477 and self.downLeft.spawnTime == 70 + 477:
            self.upRight.add()
            self.downLeft.add()

        if self.downRight.spawnTime == 78 + 478 and self.downLeft.spawnTime == 78 + 478:
            self.downLeft.add()  # sky
            self.downRight.add()
        if self.upRight.spawnTime == 85 + 488:  # down
            self.upRight.add()
        if self.upRight.spawnTime == 92 + 488:  # down
            self.upRight.add()

        if self.downLeft.spawnTime == 109 + 488:  #
            self.downLeft.add()
        if self.upRight.spawnTime == 127 + 488 and self.downLeft.spawnTime == 127 + 488:
            self.upRight.add()
            self.downLeft.add()
        if self.upLeft.spawnTime == 136 + 488 and self.downRight.spawnTime == 136 + 488:
            self.upLeft.add()
            self.downRight.add()
        if self.downRight.spawnTime == 141 + 488 and self.downLeft.spawnTime == 141 + 488:
            self.downLeft.add()
            self.downRight.add()
        if self.upLeft.spawnTime == 145 + 488:  # now
            self.upLeft.add()
        if self.upLeft.spawnTime == 154 + 488:  # now
            self.upLeft.add()

        if self.downLeft.spawnTime == 161 + 489:
            self.downLeft.add()
        if self.upLeft.spawnTime == 177 + 489:
            self.upLeft.add()
        if self.upRight.spawnTime == 195 + 489:
            self.upRight.add()
        if self.downRight.spawnTime == 209 + 489:
            self.downRight.add()
        if self.downRight.spawnTime == 227 + 489:
            self.downRight.add()
        if self.upRight.spawnTime == 243 + 490:
            self.upRight.add()
        if self.upLeft.spawnTime == 254 + 489:
            self.upLeft.add()
        if self.downLeft.spawnTime == 262 + 489:
            self.downLeft.add()
        if self.downRight.spawnTime == 273 + 489 and self.downLeft.spawnTime == 273 + 489:
            self.downLeft.add()
            self.downRight.add()  # one in a million
        if self.downRight.spawnTime == 288 + 489 and self.downLeft.spawnTime == 288 + 489:
            self.downLeft.add()
            self.downRight.add()

        if self.upRight.spawnTime == 298 + 489 and self.upLeft.spawnTime == 298 + 489:
            self.upLeft.add()
            self.upRight.add()  # high
        if self.downRight.spawnTime == 309 + 489 and self.downLeft.spawnTime == 309 + 489:
            self.downRight.add()
            self.downLeft.add()  # drop
        if self.upRight.spawnTime == 320 + 489:
            self.upRight.add()
        if self.upRight.spawnTime == 328 + 489:
            self.upRight.add()
        if self.upRight.spawnTime == 336 + 489 and self.upLeft.spawnTime == 336 + 489:
            self.upRight.add()
            self.upLeft.add()
        if self.downRight.spawnTime == 344 + 489 and self.downLeft.spawnTime == 344 + 489:
            self.downLeft.add()
            self.downRight.add()

        if self.downRight.spawnTime == 360 + 489:
            self.downRight.add()
        if self.upRight.spawnTime == 368 + 489:
            self.upRight.add()
        if self.upLeft.spawnTime == 376 + 489:
            self.upLeft.add()
        if self.downLeft.spawnTime == 384 + 489:
            self.downLeft.add()
        if self.downLeft.spawnTime == 413 + 489:
            self.downLeft.add()
        if self.upLeft.spawnTime == 418 + 489:
            self.upLeft.add()
        if self.upRight.spawnTime == 435 + 489:
            self.upRight.add()
        if self.downRight.spawnTime == 441 + 489:
            self.downRight.add()  # what it sounds like

        if self.upLeft.spawnTime == 458 + 489:
            self.upLeft.add()
        if self.upLeft.spawnTime == 464 + 489:
            self.upLeft.add()
        if self.upRight.spawnTime == 476 + 489:
            self.upRight.add()
        if self.upRight.spawnTime == 482 + 5 + 489:
            self.upRight.add()
        # if self.downRight.spawnTime == 493 + 489:
        #     self.downRight.add()
        # if self.downRight.spawnTime == 501 + 489:
        #     self.downRight.add()
        # if self.upLeft.spawnTime == 509 + 489:
        #     self.upLeft.add()
        # if self.upLeft.spawnTime == 515 + 489:
        #     self.upLeft.add()

        if self.upRight.spawnTime == 493 + 489 and self.upLeft.spawnTime == 493 + 489:
            self.upLeft.add()
            self.upRight.add()
        if self.upRight.spawnTime == 501 + 489 and self.upLeft.spawnTime == 501 + 489:
            self.upLeft.add()
            self.upRight.add()
        if self.downRight.spawnTime == 509 + 489 and self.downLeft.spawnTime == 509 + 489:
            self.downLeft.add()
            self.downRight.add()
        if self.downRight.spawnTime == 515 + 489 and self.downLeft.spawnTime == 515 + 489:
            self.downLeft.add()
            self.downRight.add()

            # beat drop
        if self.downLeft.spawnTime == 1015:  # hey
            self.downLeft.add()
        if self.downRight.spawnTime == 1027:  # taking
            self.downRight.add()
        if self.downLeft.spawnTime == 1035:  # pain
            self.downLeft.add()
        if self.upRight.spawnTime == 1055 and self.upLeft.spawnTime == 1055:
            self.upLeft.add()
            self.upRight.add()  # away
        if self.downRight.spawnTime == 1064:  # shaking
            self.downRight.add()
        if self.downLeft.spawnTime == 1076:  # earth
            self.downLeft.add()
        if self.upLeft.spawnTime == 1090:
            self.upLeft.add()
        if self.upRight.spawnTime == 1096:
            self.upRight.add()
        if self.downRight.spawnTime == 1105:
            self.downRight.add()
        if self.downRight.spawnTime == 1110:  # eh
            self.downRight.add()
        if self.upRight.spawnTime == 1118:  # eh
            self.upRight.add()
        if self.upLeft.spawnTime == 1126:  # eh
            self.upLeft.add()

        if self.downLeft.spawnTime == 1015 + 126:  # hey
            self.downLeft.add()
        if self.downRight.spawnTime == 1027 + 126:  # taking
            self.downRight.add()
        if self.downLeft.spawnTime == 1035 + 126:  # pain
            self.downLeft.add()
        if self.upRight.spawnTime == 1055 + 126 and self.upLeft.spawnTime == 1055 + 126:
            self.upLeft.add()
            self.upRight.add()  # away
        if self.downRight.spawnTime == 1064 + 126:  # shaking
            self.downRight.add()
        if self.downLeft.spawnTime == 1076 + 126:  # earth
            self.downLeft.add()
        if self.upLeft.spawnTime == 1090 + 126:
            self.upLeft.add()
        if self.upRight.spawnTime == 1096 + 126:
            self.upRight.add()
        if self.downRight.spawnTime == 1105 + 126:
            self.downRight.add()
        if self.downRight.spawnTime == 1110 + 126:  # eh
            self.downRight.add()
        if self.upRight.spawnTime == 1118 + 126:  # eh
            self.upRight.add()
        if self.upLeft.spawnTime == 1126 + 126:  # eh
            self.upLeft.add()

            # verse 3:
        if self.upRight.spawnTime == 298 + 489 + 502 and self.upLeft.spawnTime == 298 + 489 + 502:
            self.upLeft.add()
            self.upRight.add()  # high
        if self.downRight.spawnTime == 309 + 489 + 502 and self.downLeft.spawnTime == 309 + 489 + 502:
            self.downRight.add()
            self.downLeft.add()  # drop
        if self.upRight.spawnTime == 320 + 489 + 502:
            self.upRight.add()
        if self.upRight.spawnTime == 328 + 489 + 502:
            self.upRight.add()
        if self.upRight.spawnTime == 336 + 489 + 502 and self.upLeft.spawnTime == 336 + 489 + 502:
            self.upRight.add()
            self.upLeft.add()
        if self.downRight.spawnTime == 344 + 489 + 502 and self.downLeft.spawnTime == 344 + 489 + 502:
            self.downLeft.add()
            self.downRight.add()

        if self.downRight.spawnTime == 360 + 489 + 502:
            self.downRight.add()
        if self.upRight.spawnTime == 368 + 489 + 502:
            self.upRight.add()
        if self.upLeft.spawnTime == 376 + 489 + 502:
            self.upLeft.add()
        if self.downLeft.spawnTime == 384 + 489 + 502:
            self.downLeft.add()
        if self.downLeft.spawnTime == 413 + 489 + 502:
            self.downLeft.add()
        if self.upLeft.spawnTime == 418 + 489 + 502:
            self.upLeft.add()
        if self.upRight.spawnTime == 435 + 489 + 502:
            self.upRight.add()
        if self.downRight.spawnTime == 441 + 489 + 502:
            self.downRight.add()  # what it sounds like

        if self.upLeft.spawnTime == 458 + 489 + 502:
            self.upLeft.add()
        if self.upLeft.spawnTime == 464 + 489 + 502:
            self.upLeft.add()
        if self.upRight.spawnTime == 476 + 489 + 502:
            self.upRight.add()
        if self.upRight.spawnTime == 482 + 5 + 489 + 502:
            self.upRight.add()
        # if self.downRight.spawnTime == 493 + 489 + 502:
        #     self.downRight.add()
        # if self.downRight.spawnTime == 501 + 489 + 502:
        #     self.downRight.add()
        # if self.upLeft.spawnTime == 509 + 489 + 502:
        #     self.upLeft.add()
        # if self.upLeft.spawnTime == 515 + 489 + 502:
        #     self.upLeft.add()

        if self.upRight.spawnTime == 493 + 489 + 502 and self.upLeft.spawnTime == 493 + 489 + 502:
            self.upLeft.add()
            self.upRight.add()
        if self.upRight.spawnTime == 501 + 489 + 502 and self.upLeft.spawnTime == 501 + 489 + 502:
            self.upLeft.add()
            self.upRight.add()
        if self.downRight.spawnTime == 509 + 489 + 502 and self.downLeft.spawnTime == 509 + 489 + 502:
            self.downLeft.add()
            self.downRight.add()
        if self.downRight.spawnTime == 515 + 489 + 502 and self.downLeft.spawnTime == 515 + 489 + 502:
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
                        game.perfect += 1
                    elif distance <= 2 * d / 3:
                        game.score.score += 100
                        game.performance = "GREAT"
                        game.great += 1
                    else:
                        game.performance = "BAD"
                        game.bad += 1
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
                        game.perfect += 1
                    elif distance <= 2 * d / 3:
                        game.score.score += 100
                        game.performance = "GREAT"
                        game.great += 1
                    else:
                        game.performance = "BAD"
                        game.bad += 1
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
                        game.perfect += 1
                    elif distance <= 2 * d / 3:
                        game.score.score += 100
                        game.performance = "GREAT"
                        game.great += 1
                    else:
                        game.performance = "BAD"
                        game.bad += 1
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
    pygame.mixer.music.load("song\\opening-song.mp3")
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
