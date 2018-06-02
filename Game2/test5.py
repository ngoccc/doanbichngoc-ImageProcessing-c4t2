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


center = pygame.image.load("E:\\hmm\\images\\Center.png")
glow = pygame.image.load("E:\\hmm\\images\\Glow.png")

# starting positions

posUpLeft = (window_width / 2 - 74, window_height / 2 - 74)
posUpRight = (window_width / 2 + 10, window_height / 2 - 74)
posDownLeft = (window_width / 2 - 74, window_height / 2 + 10)
posDownRight = (window_width / 2 + 10, window_height / 2 + 10)

# button positions

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
        self.points.append(list(self.start_pos))
        self.spawnTime = 50
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

    def spawn(self):
        if self.spawnTime > 0:
            self.spawnTime -= 1
        else:
            self.points.append(list(self.start_pos))
            self.spawnTime = 50


class Scoreboard():
    def __init__(self, fontSize=70, score=0):
        self.x = window_width / 2
        self.y = 20
        self.score = score
        self.font = pygame.font.Font('Bolt.ttf', fontSize)  # font?????

    def display(self, score):
        result_srf = self.font.render('%s' % (score), True, BLUE)
        result_rect_w = result_srf.get_rect().width
        display_surf.blit(result_srf, (self.x - result_rect_w / 2, self.y))


class Game:
    def __init__(self, speed=7):
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
        self.combo = []
        self.performance = ""

    def update(self):
        self.upLeft.spawn()
        self.upLeft.move()
        self.upRight.spawn()
        self.upRight.move()
        self.downLeft.spawn()
        self.downLeft.move()
        self.downRight.spawn()
        self.downRight.move()
        self.score.display(self.score.score)
        # # display miss perfomance??
        # if self.upLeft.performance == "MISS":
        #     self.performance = self.upLeft.performance
        if self.upLeft.isMissed:
            self.performance = "MISS"
            self.miss += 1
        elif self.upRight.isMissed:
            self.performance = "MISS"
            self.miss += 1
        elif self.downLeft.isMissed:
            self.performance = "MISS"
            self.miss += 1
        elif self.downRight.isMissed:
            self.performance = "MISS"
            self.miss += 1

        Display_Performance(self.performance)


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

    # result_rect.center = (window_width / 2, window_height / 2)
    display_surf.blit(result_srf, (window_width / 2 - result_rect_w / 2, window_height / 2 - result_rect_h / 2))


def main():
    pygame.init()
    game = Game()
    cam = webcam.Webcam()
    cam.thread_webcam()
    # cap = cv2.VideoCapture(0)

    # def Scoring(pos, pos_button):
    #     if len(game.pos.points) != 0:
    #         currentPoint_x = game.pos.points[0][0]
    #         currentPoint_y = game.pos.points[0][1]
    #         button_x = pos_button[0]
    #         button_y = pos_button[1]
    #         distance = Distance(currentPoint_x, currentPoint_y, button_x, button_y)
    #         if currentPoint_x >= 10 and currentPoint_y >= 10:  # inside
    #             if distance <= d / 3:
    #                 game.score.score += 200
    #             elif distance <= 2 * d / 3:
    #                 game.score.score += 100
    #             else:
    #                 game.score.score += 50
    #             display_surf.blit(glow, pos_button)
    #             game.pos.points.remove([currentPoint_x, currentPoint_y])

    while True:
        frame = cam.get_currentFrame()
        frame = cv2.resize(frame, (window_width, window_height), cv2.INTER_CUBIC)

        # connect webcam

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        display_surf.blit(frame, (0, 0))
        Draw_Elements()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    # upLeft
                    # Scoring(upLeft, buttonUpLeft) ko dc??
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

                        else:
                            game.performance = "MISS"
                            game.miss += 1

                elif event.key == K_p:
                    # upRight
                    if len(game.upRight.points) != 0:
                        game.upRight.isMissed = False
                        currentPoint_x = game.upRight.points[0][0]
                        currentPoint_y = game.upRight.points[0][1]
                        button_x = buttonUpRight[0]
                        button_y = buttonUpRight[1]
                        distance = Distance(currentPoint_x, currentPoint_y, button_x, button_y)
                        if currentPoint_x >= 10 and currentPoint_y >= 10:  # inside
                            if distance <= d / 3:
                                game.score.score += 200
                                game.performance = "PERFECT"
                            elif distance <= 2 * d / 3:
                                game.score.score += 100
                                game.performance = "GREAT"
                            else:
                                game.performance = "BAD"
                            display_surf.blit(glow, buttonUpRight)
                            game.upRight.points.remove([currentPoint_x, currentPoint_y])

                        else:
                            game.performance = "MISS"

                elif event.key == K_z:
                    # downLeft
                    if len(game.downLeft.points) != 0:
                        game.downLeft.isMissed = False
                        currentPoint_x = game.downLeft.points[0][0]
                        currentPoint_y = game.downLeft.points[0][1]
                        button_x = buttonDownLeft[0]
                        button_y = buttonDownLeft[1]
                        distance = Distance(currentPoint_x, currentPoint_y, button_x, button_y)
                        if currentPoint_x >= 10 and currentPoint_y >= 10:  # inside
                            if distance <= d / 3:
                                game.score.score += 200
                                game.performance = "PERFECT"
                            elif distance <= 2 * d / 3:
                                game.score.score += 100
                                game.performance = "GREAT"
                            else:
                                game.performance = "BAD"
                            display_surf.blit(glow, buttonDownLeft)
                            game.downLeft.points.remove([currentPoint_x, currentPoint_y])

                        else:
                            game.performance = "MISS"
                elif event.key == K_m:
                    # downRight
                    if len(game.downRight.points) != 0:
                        game.downRight.isMissed = False
                        currentPoint_x = game.downRight.points[0][0]
                        currentPoint_y = game.downRight.points[0][1]
                        button_x = buttonDownRight[0]
                        button_y = buttonDownRight[1]
                        distance = Distance(currentPoint_x, currentPoint_y, button_x, button_y)
                        if currentPoint_x >= 10 and currentPoint_y >= 10:  # inside
                            if distance <= d / 3:
                                game.score.score += 200
                                game.performance = "PERFECT"
                            elif distance <= 2 * d / 3:
                                game.score.score += 100
                                game.performance = "GREAT"
                            else:
                                game.performance = "BAD"
                            display_surf.blit(glow, buttonDownRight)
                            game.downRight.points.remove([currentPoint_x, currentPoint_y])

                        else:
                            game.performance = "MISS"
        game.update()
        pygame.display.update()
        fps_clock.tick(fps)


if __name__ == '__main__':
    main()
