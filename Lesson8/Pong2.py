import pygame, sys
from pygame.locals import *
import cv2
import numpy as np

# make colors

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

window_height = 300
window_width = 400

display_surf = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Ping pong")

fps = 60
fps_clock = pygame.time.Clock()


class Paddle():
    def __init__(self, x, w, h):
        self.w = w
        self.h = h
        self.x = x
        self.y = int(window_height) / 2
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def draw(self):
        pygame.draw.rect(display_surf, WHITE, self.rect)

    def move(self, pos):
        self.rect.y = pos[1]
        self.draw()


class Autopaddle(Paddle):
    def __init__(self, x, w, h, speed, ball):
        super().__init__(x, w, h)
        self.speed = speed
        self.ball = ball

    def move(self):
        if self.ball.dir_x == 1:
            if self.rect.y < self.ball.rect.bottom:
                self.rect.y += self.speed
            if self.rect.y > self.ball.rect.bottom:
                self.rect.y -= self.speed


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


class Ball():
    def __init__(self, x, y, w, h, speed):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.speed = speed
        self.dir_x = -1  # left = -1 and right = 1
        self.dir_y = -1  # up = -1 and down = 1
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self):
        pygame.draw.rect(display_surf, WHITE, self.rect)

    def bounce(self, axis):
        if axis == 'x':
            self.dir_y *= -1
        if axis == 'y':
            self.dir_x *= -1

    def hit_ceiling(self):
        if self.dir_y == -1 and self.rect.top <= self.h:
            return True
        else:
            return False

    def hit_floor(self):
        if self.dir_y == 1 and self.rect.bottom >= window_height - self.h:
            return True
        else:
            return False

    def hit_wall(self):
        if (self.dir_x == -1 and self.rect.left <= self.w) or (
                self.dir_x == 1 and self.rect.right >= window_width - self.w):
            return True
        else:
            return False

    def hit_paddle_user(self, paddle):
        if (self.rect.left <= paddle.rect.right) and (self.rect.bottom >= paddle.rect.top) and (
                self.rect.top <= paddle.rect.bottom):
            return True
        else:
            return False

    def hit_paddle_computer(self, paddle):
        if (self.rect.right >= paddle.rect.left) and (self.rect.bottom >= paddle.rect.top) and (
                self.rect.top <= paddle.rect.bottom):
            return True
        else:
            return False

    def move(self):
        self.rect.x += self.dir_x * self.speed
        self.rect.y += self.dir_y * self.speed

        if self.hit_ceiling() or self.hit_floor():
            self.bounce('x')


class Game():
    def __init__(self, line_thickness=10, speed=2):
        self.line_thickness = line_thickness
        self.speed = speed
        ball_x = int(window_width / 2)
        ball_y = int(window_height / 2)
        ball_w = self.line_thickness
        ball_h = self.line_thickness
        self.ball = Ball(ball_x, ball_y, ball_w, ball_h, self.speed)

        self.paddles = {}
        paddle_x = 20
        paddle_w = self.line_thickness
        paddle_h = 50

        self.paddles['user'] = Paddle(paddle_x, paddle_w, paddle_h)
        self.paddles['computer'] = Autopaddle(window_width - paddle_x - self.line_thickness, paddle_w, paddle_h,
                                              self.speed, self.ball)

        self.score = Scoreboard()

    def draw_arena(self):
        display_surf.fill((255, 255, 255))
        pygame.draw.rect(display_surf, BLACK, (10, 10, window_width - 20, window_height - 20))
        pygame.draw.line(display_surf, WHITE, (window_width / 2, 0), (window_width / 2, window_height))

    def update(self):
        self.ball.move()
        self.paddles['computer'].move()

        if self.ball.hit_paddle_user(self.paddles['user']):
            self.ball.bounce('y')
            self.score.score += 1

        if self.ball.hit_paddle_computer(self.paddles['computer']):
            self.ball.bounce('y')
        if self.ball.hit_wall():
            return True
        self.draw_arena()
        self.ball.draw()
        self.paddles['user'].draw()
        self.paddles['computer'].draw()
        self.score.display(self.score.score)


def main():
    pygame.init()
    game = Game()
    # connect webcam
    cap = cv2.VideoCapture(0)
    lower = np.array([0, 25, 61])
    higher = np.array([255, 224, 255])

    cascade = cv2.CascadeClassifier("E:\\C4T\\Image Processing\\Lesson7\\haarcascade_frontalface_alt2.xml")

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        faces = cascade.detectMultiScale(gray)
        if len(faces) > 0:
            xmax = faces[0, 0]
            ymax = faces[0, 1]
            wmax = faces[0, 2]
            hmax = faces[0, 3]
            cx = 0
            cy = 0
            for x, y, w, h in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                if w * h > wmax * hmax:
                    xmax = x
                    ymax = y
                    wmax = w
                    hmax = h
            if ymax < 0:
                cx = 0
                cy = 0
            elif (ymax + h) > window_height:
                cx = 0
                cy = window_height
            else:
                cx = int(xmax + wmax / 2)
                cy = int(ymax + hmax / 2)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0))
            frame = cv2.resize(frame, (400, 300 + 80))
            cv2.imshow("frame", frame)
            cv2.waitKey(1)
            # for event in pygame.event.get():
            #     if event.type == QUIT:
            #         pygame.quit()
            #         sys.exit()
            game.paddles['user'].move((cx, cy - hmax/2))
        game.update()
        if game.update():
            pygame.quit()
            sys.exit()
        pygame.display.update()
        fps_clock.tick(fps)
    # print('Your score: ',game.score.score)


if __name__ == '__main__':
    main()
