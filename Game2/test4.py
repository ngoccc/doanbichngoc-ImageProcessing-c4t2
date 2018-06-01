import pygame
import cv2
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# display_surf = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
display_surf = pygame.display.set_mode((600, 600))
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

# starting positions

posUpLeft = (window_width / 2 - 74, window_height / 2 - 74)
posUpRight = (window_width / 2 + 10, window_height / 2 - 74)
posDownLeft = (window_width / 2 - 74, window_height / 2 + 10)
posDownRight = (window_width / 2 + 10, window_height / 2 + 10)


class Point:

    def __init__(self, img, dir, start_pos, speed):
        self.points = []
        self.image = img
        self.direction = dir
        self.start_pos = start_pos
        self.speed = speed
        self.points.append(list(self.start_pos))
        self.spawnTime = 50

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

    def spawn(self):
        if self.spawnTime > 0:
            self.spawnTime -= 1
        else:
            self.points.append(list(self.start_pos))
            self.spawnTime = 50


class Game:
    def __init__(self, speed=5):
        self.speed = speed
        point_speed = self.speed
        self.upLeft = Point(upLeft, 1, posUpLeft, point_speed)
        self.upRight = Point(upRight, 2, posUpRight, point_speed)
        self.downLeft = Point(downLeft, 3, posDownLeft, point_speed)
        self.downRight = Point(downRight, 4, posDownRight, point_speed)

    def update(self):
        self.upLeft.spawn()
        self.upLeft.move()
        self.upRight.spawn()
        self.upRight.move()
        self.downLeft.spawn()
        self.downLeft.move()
        self.downRight.spawn()
        self.downRight.move()


def Draw_Elements():
    display_surf.blit(upLeft, (10, 10))
    display_surf.blit(upRight, (window_width - 74, 10))
    display_surf.blit(downLeft, (10, window_height - 74))
    display_surf.blit(downRight, (window_width - 74, window_height - 74))
    display_surf.blit(center, posUpLeft)  # upLeft
    display_surf.blit(center, posUpRight)  # upRight
    display_surf.blit(center, posDownLeft)  # downLeft
    display_surf.blit(center, posDownRight)  # downRight


# def Get_Color(x, y):
#     get_color = display_surf.get_at((x, y))
#     color = (get_color[0], get_color[1], get_color[2])
#     if color == WHITE:
#         display_surf.blit(glow, (10, 10))

# def Check_Collision(img, x, y):
#     if img[x, y] != 0:
#         display_surf.blit(glow, (x, y))


def main():
    pygame.init()
    game = Game()
    cap = cv2.VideoCapture(0)
    fgbg = cv2.createBackgroundSubtractorMOG2()

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (window_width, window_height), cv2.INTER_CUBIC)
        fgmask = fgbg.apply(frame)

        # connect webcam

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        display_surf.blit(frame, (0, 0))
        Draw_Elements()

        # get color

        if fgmask[10, 10] != 0: # upLeft
            display_surf.blit(glow, (10, 10))
            if len(game.upLeft.points) != 0:
                game.upLeft.points.remove([game.upLeft.points[0][0], game.upLeft.points[0][1]])
        if fgmask[window_width - 74, 10] != 0:  # upRight
            display_surf.blit(glow, (window_width - 74, 10))
            if len(game.upRight.points) != 0:
                game.upRight.points.remove([game.upRight.points[0][0], game.upRight.points[0][1]])
        if fgmask[10, window_height - 74] != 0:  # downLeft
            display_surf.blit(glow, (10, window_height - 74))
            if len(game.downLeft.points) != 0:
                game.downLeft.points.remove([game.downLeft.points[0][0], game.downLeft.points[0][1]])
        if fgmask[window_width - 74, window_height - 74] != 0:  # downRight
            display_surf.blit(glow, (window_width - 74, window_height - 74))
            if len(game.downRight.points) != 0:
                game.downRight.points.remove([game.downRight.points[0][0], game.downRight.points[0][1]])

        game.update()
        pygame.display.update()
        fps_clock.tick(fps)


if __name__ == '__main__':
    main()
