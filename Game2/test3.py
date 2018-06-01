import pygame
from pygame.locals import *
import math
import random
import cv2
import numpy as np
import os

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# display_surf = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display_surf = pygame.display.set_mode((400, 300))
pygame.display.set_caption("dancing2")
window_width, window_height = pygame.display.get_surface().get_size()
fps = 30
fps_clock = pygame.time.Clock()


class Point():
    def __init__(self):
        self.downLeft = pygame.image.load("E:\\hmm\\images\\DownLeft.png")
        self.downRight = pygame.image.load("E:\\hmm\\images\\DownRight.png")
        self.upLeft = pygame.image.load("E:\\hmm\\images\\UpLeft.png")
        self.upRight = pygame.image.load("E:\\hmm\\images\\UpRight.png")

        self.downLeftActive = pygame.image.load("E:\\hmm\\images\\DownLeftActive.png")
        self.downRightActive = pygame.image.load("E:\\hmm\\images\\DownRightActive.png")
        self.upLeftActive = pygame.image.load("E:\\hmm\\images\\UpLeftActive.png")
        self.upRightActive = pygame.image.load("E:\\hmm\\images\\UpRightActive.png")

        self.center = pygame.image.load("E:\\hmm\\images\\Center.png")
        self.glow = pygame.image.load("E:\\hmm\\images\\Glow.png")


class Game():
    def __init__(self):
        # draw elements
        self.point = Point()
        # display_surf.blit(self.point.upLeft, (50, 50))
        # display_surf.blit(self.point.upRight, (window_width - 50, 50))
        # display_surf.blit(self.point.downLeft, (50, window_height - 50))
        # display_surf.blit(self.point.downRight, (window_width - 50, window_height - 50))
        pygame.draw.rect(display_surf, (0, 0, 255), (50, 50, 30, 30), 0)
        pygame.draw.rect(display_surf, (255, 0, 0), (window_width - 50, 50, 30, 30), 0)
        pygame.draw.rect(display_surf, (0, 255, 0), (50, window_height - 50, 30, 30), 0)
        pygame.draw.rect(display_surf, (255, 0, 255), (window_width - 50, window_height - 50, 30, 30), 0)

    def draw_arena(self):
        display_surf.fill(BLACK)

    def update(self):
        self.draw_arena()
        # self.point.spawn()
        # self.point.draw()
        # self.score.display(self.score.score)


def main():
    pygame.init()
    game = Game()
    while True:
        display_surf.fill(BLACK)
        # game.update()
        pygame.display.update()
        fps_clock.tick(fps)


if __name__ == '__main__':
    main()
