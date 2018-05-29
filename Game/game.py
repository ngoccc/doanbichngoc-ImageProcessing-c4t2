import pygame
import random
import cv2
import time

# pygame.mixer.pre_init(44100, -16, 2, 4096)
# pygame.init()
# eat_sound = pygame.mixer.Sound("C:\\Download\\coin.wav")
# die_sound = pygame.mixer.Sound("C:\\Download\\die.wav")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
window_height = 600
window_width = 800
display_surf = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("snake")
fps = 30
fps_clock = pygame.time.Clock()

# # Play background music
# pygame.mixer.music.load("D:\\nhacnen.mp3")
# pygame.mixer.music.get_volume()
# pygame.mixer.music.play(-1)


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
        self.font = pygame.font.Font('freesansbold.ttf', 115)

    def draw_arena(self):
        display_surf.fill(WHITE)
        pygame.draw.rect(display_surf, BLACK,
                         (10, 10, window_width - self.line_thickness, window_height - self.line_thickness))

    def game_over(self):
        result_srf = self.font.render('GAME OVER', True, WHITE)
        display_surf.blit(result_srf, (window_width / 2, window_height / 2))

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

    # connect webcam
    cap = cv2.VideoCapture(0)
    cascade = cv2.CascadeClassifier("E:\\C4T\\Image Processing\\Lesson7\\haarcascade_frontalface_alt2.xml")

    while True:

        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame = cv2.resize(frame, (400, 300))
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

            # draw region
            cv2.rectangle(frame, (135, 0), (265, 100), (57, 255, 20), 1)
            cv2.rectangle(frame, (135, 200), (265, 300), (57, 255, 20), 1)
            cv2.rectangle(frame, (5, 100), (135, 200), (57, 255, 20), 1)
            cv2.rectangle(frame, (265, 100), (395, 200), (57, 255, 20), 1)

            # move
            if 0 <= cx <= 130 and 100 <= cy <= 200:
                game.snake.left()
            elif 270 <= cx <= 400 and 100 <= cy <= 200:
                game.snake.right()
            elif 135 <= cx <= 265 and 0 <= cy <= 100:
                game.snake.up()
            elif 135 <= cx <= 265 and 200 <= cy <= 300:
                game.snake.down()

        cv2.imshow("frame", frame)
        cv2.waitKey(1)

        game.update()
        if game.snake.hit_wall() or game.snake.hit_self():
            game.game_over()
            break
        pygame.display.update()
        fps_clock.tick(fps)
    # print('Your score:', game.score.score)


if __name__ == '__main__':
    main()
