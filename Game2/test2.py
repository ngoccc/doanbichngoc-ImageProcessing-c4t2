import pygame
from pygame.locals import *
import math
import random
import cv2
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
display_surf = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
# display_surf = pygame.display.set_mode((800, 600))
pygame.display.set_caption("dancing")
window_width, window_height = pygame.display.get_surface().get_size()
note = pygame.image.load("E:\\C4T\\Image Processing\\Game2\\note4.png")
note = pygame.transform.scale(note, (100, 100))
fps = 30
fps_clock = pygame.time.Clock()


class Point:
    points = []

    def __init__(self, spd, r=100):
        self.radius = r
        self.x = random.randrange(self.radius + 10, window_width - (self.radius + 10), 5)
        self.y = random.randrange(self.radius + 10, window_height - (self.radius + 10), 5)
        self.spd = spd
        self.spawnTime = 20 / self.spd
        self.existTime = 50
        self.points.append([self.x, self.y, self.existTime])

    def draw(self):
        for p in self.points:
            # pygame.draw.circle(display_surf, (255, 255, 255), (p[0], p[1]), self.radius, 0)
            display_surf.blit(note, (p[0], p[1]))
            p[2] -= 1

    def spawn(self):
        if self.spawnTime > 0:
            self.spawnTime -= 1
        else:
            if self.spd <= 3:  # speed up to maximum 3 times initial speed
                self.spd += 0.05
            self.__init__(self.spd)
            self.spawnTime = 50 / self.spd

    def is_clicked(self, x, y):
        for p in self.points:
            dx = x - p[0]
            dy = y - p[1]
            distance = math.sqrt(dx ** 2 + dy ** 2)
            if distance <= self.radius:  # if mouse is inside the circle
                self.points.remove([p[0], p[1], p[2]])
                return True

    def out_of_time(self):
        for p in self.points:
            if p[2] < 0:
                return True


class Scoreboard():
    def __init__(self, fontSize=20, score=0):
        self.x = window_width - 150
        self.y = 20
        self.score = score
        self.font = pygame.font.Font('freesansbold.ttf', fontSize)

    def display(self, score):
        result_srf = self.font.render('Score = %s' % (score), True, WHITE)
        result_rect = result_srf.get_rect()
        result_rect.topleft = (window_width - 150, 20)
        display_surf.blit(result_srf, (window_width - 150, 20))


class Game:
    def __init__(self):
        self.point = Point(1)
        self.score = Scoreboard()

    def draw_arena(self):
        display_surf.fill(BLACK)

    def update(self):
        # self.draw_arena()
        self.point.spawn()
        self.point.draw()
        self.score.display(self.score.score)


def main():
    pygame.init()
    game = Game()
    cap = cv2.VideoCapture(0)
    while True:
        display_surf.fill(BLACK)

        ret, frame = cap.read()
        frame = cv2.resize(frame, (window_width, window_height), cv2.INTER_CUBIC)
        cascade = cv2.CascadeClassifier("E:\\C4T\\Image Processing\\Lesson7\\haarcascade_frontalface_alt2.xml")

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = cascade.detectMultiScale(gray)
        cx = 0
        cy = 0
        if len(faces) > 0:
            xmax = faces[0, 0]
            ymax = faces[0, 1]
            wmax = faces[0, 2]
            hmax = faces[0, 3]
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                if w * h > wmax * hmax:
                    xmax = x
                    ymax = y
                    wmax = w
                    hmax = h
            cx = int(xmax + wmax / 2)
            cy = int(ymax + hmax / 2)
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0))

        # for event in pygame.event.get():
        #     if event.type == MOUSEBUTTONDOWN:
        #         mx, my = pygame.mouse.get_pos()
        #         if game.point.is_clicked(mx, my):
        #             game.score.score += 1
        #     if event.type == KEYDOWN:
        #         break

        # connect webcam
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        display_surf.blit(frame, (0, 0))

        if game.point.is_clicked(window_width - cx, cy):
            game.score.score += 1
            pygame.mixer.music.load("E:\\C4T\\Image Processing\\Game2\\SoundEffect.wav")
            pygame.mixer.music.play(0)
        game.update()

        if game.point.out_of_time():
            break
        pygame.display.update()
        fps_clock.tick(fps)


if __name__ == '__main__':
    main()
