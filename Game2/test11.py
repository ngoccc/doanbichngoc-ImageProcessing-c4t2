import webcam
import cv2
import numpy as np
import pygame

display_surf = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

pygame.init()
cam = webcam.Webcam()
cam.thread_webcam()
while True:
    frame = cam.get_currentFrame()
    frame = cv2.resize(frame, (1366, 786), cv2.INTER_CUBIC)

    # connect webcam
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)

    display_surf.blit(frame, (0, 0))
    # cv2.rectangle(frame, (1366 - 74, 10), (1366 - 74 + 64, 10 + 64), (255, 255, 255), 3)
    print(cam.get_pos(10, 1366 - 74))
    pygame.display.update()
