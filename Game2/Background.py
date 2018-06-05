import pygame
import cv2
import numpy as np
import sys

camera = cv2.VideoCapture(0)

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("dancing2")
window_width, window_height = pygame.display.get_surface().get_size()

fps = 30
fps_clock = pygame.time.Clock()

title = pygame.image.load("E:\\C4T\\Image Processing\\Game2\\text_startmenu.png")
start = pygame.image.load("E:\\C4T\\Image Processing\\Game2\Press Start.png")

while True:
    ret, frame = camera.read()
    frame = cv2.resize(frame, (window_width, window_height))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)

    screen.blit(frame, (0, 0))
    title_x = title.get_rect().width
    screen.blit(title, (window_width/2 - title_x/2, 20))
    screen.blit(start, (350, 450))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if 350 + 500 > mouse[0] > 500 and 800 > mouse[1] > 500:
                sys.exit()
