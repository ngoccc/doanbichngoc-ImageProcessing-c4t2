import pygame
import cv2
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
display_surf = pygame.display.set_mode((600, 600))
pygame.display.set_caption("dancing")
window_width, window_height = pygame.display.get_surface().get_size()
fps = 30
fps_clock = pygame.time.Clock()

upLeft = pygame.image.load("E:\\hmm\\images\\UpLeft.png")
upRight = pygame.image.load("E:\\hmm\\images\\UpRight.png")
glow = pygame.image.load("E:\\hmm\\images\\Glow.png")


def main():
    pygame.init()
    cap = cv2.VideoCapture(0)
    fgbg = cv2.createBackgroundSubtractorMOG2()

    while True:
        display_surf.fill(BLACK)
        ret, frame = cap.read()
        frame = cv2.resize(frame, (window_width, window_height), cv2.INTER_CUBIC)
        fgmask = fgbg.apply(frame)

        # connect webcam
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        fgmask = np.rot90(fgmask)
        fgmask = pygame.surfarray.make_surface(fgmask)
        display_surf.blit(fgmask, (0, 0))
        getColor = display_surf.get_at((42, 42))

        # connect webcam
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        display_surf.blit(frame, (0, 0))

        color = (getColor[0], getColor[1], getColor[2])
        if color == WHITE:
            display_surf.blit(glow, (42, 42))
        pygame.display.update()
        fps_clock.tick(fps)


if __name__ == '__main__':
    main()
