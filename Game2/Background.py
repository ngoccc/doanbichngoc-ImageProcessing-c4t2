import pygame
import cv2
import numpy as np
import sys

camera = cv2.VideoCapture(0)
pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("E:\\C4T\\Image Processing\\Game2\\song\\opening-song.mp3")
pygame.mixer.music.play(1)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("dancing2")
window_width, window_height = pygame.display.get_surface().get_size()

fps = 30
fps_clock = pygame.time.Clock()


title = pygame.image.load("E:\\C4T\Image Processing\\Game2\\images\\start\\text_startmenu.png")
title = pygame.transform.scale(title, (window_width, window_height))
start = pygame.image.load("E:\\C4T\\Image Processing\\Game2\\images\\start\\Press Start.png")



def Start():
    screen.blit(title, (0, 0))
    screen.blit(start, (350, 450))


while True:
    ret, frame = camera.read()
    frame = cv2.resize(frame, (window_width, window_height))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)

    screen.blit(frame, (0, 0))
    # Start()  # start menu

    # pygame.mixer.music.set_volume(0.5)
    pygame.display.update()
    fps_clock.tick(fps)
    #
    # for event in pygame.event.get():
    #     if event.type == pygame.MOUSEBUTTONDOWN:
    #         mouse = pygame.mouse.get_pos()
    #         if 350 + 500 > mouse[0] > 500 and 800 > mouse[1] > 500:
    #             sys.exit()  # escape start menu
