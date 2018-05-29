import pygame
from pygame.locals import *
import math
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
window_height = 600
window_width = 800
display_surf = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("dancing")
fps = 30
fps_clock = pygame.time.Clock()


class Point():
    points = []

    def __init__(self, spd, r=20):
        self.x = random.randrange(20 + 10, window_width - (20 + 10), 5)
        self.y = random.randrange(20 + 10, window_height - (20 + 10), 5)
        self.radius = r
        self.spd = spd
        self.spawnTime = 20 / self.spd
        self.existTime = 50
        self.points.append([self.x, self.y, self.existTime])

    def draw(self):
        for p in self.points:
            pygame.draw.circle(display_surf, (255, 255, 255), (p[0], p[1]), self.radius, 0)
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


class Game():
    def __init__(self, line_thickness=20):
        self.line_thickness = line_thickness
        self.point = Point(1)
        self.score = Scoreboard()

    def draw_arena(self):
        display_surf.fill(BLACK)

    def update(self):
        self.draw_arena()
        self.point.spawn()
        self.point.draw()
        self.score.display(self.score.score)


def main():
    pygame.init()
    game = Game()
    speedUp = 1
    while True:
        game.update()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if game.point.is_clicked(mx, my):
                    game.score.score += 1
        if game.point.out_of_time():
            break
        # if fps_clock.get_ticks() == 500:
        #     # speed up
        #     pass
        # speedUp += 0.05
        # if speedUp >= 3:

        pygame.display.update()
        fps_clock.tick(fps)


if __name__ == '__main__':
    main()
