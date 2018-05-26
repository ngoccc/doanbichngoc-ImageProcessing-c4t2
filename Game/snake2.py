import pygame
from pygame.locals import *
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
window_height = 600
window_width = 800
display_surf = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("snake")
fps = 30
fps_clock = pygame.time.Clock()


class Snake:
    def __init__(self, speed):
        self.speed = speed
        self.xx = self.speed  # để ban đầu đi ngang
        self.yy = 0
        self.moveRight = True
        self.moveLeft = False
        self.moveUp = False
        self.moveDown = False

    snakeBody = [[60, 20], [50, 20], [40, 20], [30, 20], [20, 20]]

    def move(self):
        n = len(self.snakeBody)

        # draw

        for i in range(n - 1):
            # if i != 0:
            self.snakeBody[n - 1 - i][0] = self.snakeBody[n - 1 - i - 1][0]
            self.snakeBody[n - 1 - i][1] = self.snakeBody[n - 1 - i - 1][1]
            pygame.draw.rect(display_surf, WHITE,
                             pygame.Rect(self.snakeBody[i + 1][0], self.snakeBody[i + 1][1], 10, 10))

        self.snakeBody[0][0] += self.xx
        self.snakeBody[0][1] += self.yy
        pygame.draw.rect(display_surf, WHITE,
                         pygame.Rect(self.snakeBody[0][0], self.snakeBody[0][1], 10, 10))

    def reset(self):
        self.moveLeft, self.moveRight, self.moveUp, self.moveDown = False, False, False, False

    def right(self):
        if not self.moveLeft:
            self.reset()
            self.xx = self.speed
            self.yy = 0
            self.moveRight = True

    def left(self):
        if not self.moveRight:
            self.reset()
            self.xx = -self.speed
            self.yy = 0
            self.moveLeft = True

    def up(self):
        if not self.moveDown:
            self.reset()
            self.xx = 0
            self.yy = -self.speed
            self.moveUp = True

    def down(self):
        if not self.moveUp:
            self.reset()
            self.xx = 0
            self.yy = self.speed
            self.moveDown = True

    def eat_apple(self, apple):
        for pos in self.snakeBody:
            if -5 <= (pos[0] - apple.x) <= 5 and -5 <= (pos[1] - apple.y) <= 5:
                return True

    def add(self):
        tail = [self.snakeBody[-1][0] - 10, self.snakeBody[-1][1]]
        self.snakeBody.append(tail)

    def hit_wall(self):
        for pos in self.snakeBody:
            if pos[0] <= 5 or pos[0] >= window_width - 5 or pos[1] <= 5 or pos[1] >= window_height - 5:
                return True

    def hit_self(self):
        head = self.snakeBody[0]
        for block in self.snakeBody[1:]:
            if head[0] == block[0] and head[1] == block[1]:
                return True


class Apple():
    def __init__(self):
        self.x = random.randrange(20 + 10, window_width - (20 + 10), 5)
        self.y = random.randrange(20 + 10, window_height - (20 + 10), 5)

    def draw(self):
        pygame.draw.rect(display_surf, WHITE,
                         pygame.Rect(self.x, self.y, 10, 10))


class Scoreboard:
    def __init__(self, font_size=20, score=0):
        self.x = window_width - 150
        self.y = 20
        self.score = score
        self.font = pygame.font.Font('freesansbold.ttf', font_size)

    def display(self, score):
        result_srf = self.font.render('Score = %s' % score, True, WHITE)
        result_rect = result_srf.get_rect()
        result_rect.topleft = (window_width - 150, 20)
        display_surf.blit(result_srf, result_rect)


class Game:
    def __init__(self, line_thickness=20, speed=5):
        self.speed = speed
        self.line_thickness = line_thickness
        snake_speed = speed
        self.snake = Snake(snake_speed)
        self.apple = Apple()
        self.score = Scoreboard()

    def draw_arena(self):
        display_surf.fill(WHITE)
        pygame.draw.rect(display_surf, BLACK,
                         (10, 10, window_width - self.line_thickness, window_height - self.line_thickness))

    def update(self):
        self.draw_arena()
        self.snake.move()
        self.apple.draw()
        if self.snake.eat_apple(self.apple):
            self.apple.__init__()
            self.snake.add()
            self.score.score += 1
        self.score.display(self.score.score)


def main():
    pygame.init()
    game = Game()
    while True:
        for event in pygame.event.get():
            # if event.type == QUIT:
            #     pygame.quit()
            #     sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    game.snake.up()
                elif event.key == K_DOWN:
                    game.snake.down()
                elif event.key == K_RIGHT:
                    game.snake.right()
                elif event.key == K_LEFT:
                    game.snake.left()
        game.update()
        if game.snake.hit_wall() or game.snake.hit_self():
            break
        pygame.display.update()
        fps_clock.tick(fps)
    # print('Your score:', game.score.score)


if __name__ == '__main__':
    main()
