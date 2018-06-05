import cv2
import numpy as np
import keyboard
from Variables import *
from Functions import Draw_Elements
from Game import Game
from Webcam import Webcam


def main():
    #pygame.init()
    game = Game()
    cam = Webcam()
    cam.thread_webcam()

    while True:
        frame = cam.get_currentFrame()
        frame = cv2.resize(frame, (window_width, window_height), cv2.INTER_CUBIC)

        # connect webcam

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        display_surf.blit(frame, (0, 0))
        Draw_Elements()

        if game.upLeft.isMissed:
            game.performance = "MISS"
            game.miss += 1
            game.upLeft.isMissed = False
        elif game.upRight.isMissed:
            game.performance = "MISS"
            game.miss += 1
            game.upRight.isMissed = False
        elif game.downLeft.isMissed:
            game.performance = "MISS"
            game.miss += 1
            game.downLeft.isMissed = False
        elif game.downRight.isMissed:
            game.performance = "MISS"
            game.miss += 1
            game.downRight.isMissed = False

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == K_q:
                    # upLeft
                    # Scoring(upLeft, buttonUpLeft) ko dc??
                    if len(game.upLeft.points) != 0:
                        game.upLeft.isMissed = False
                        currentPoint_x = game.upLeft.points[0][0]
                        currentPoint_y = game.upLeft.points[0][1]
                        button_x = buttonUpLeft[0]
                        button_y = buttonUpLeft[1]
                        distance = Distance(currentPoint_x, currentPoint_y, button_x, button_y)
                        if currentPoint_x >= 10 and currentPoint_y >= 10:  # inside
                            if distance <= d / 3:
                                game.score.score += 200
                                game.performance = "PERFECT"
                                game.perfect += 1
                            elif distance <= 2 * d / 3:
                                game.score.score += 100
                                game.performance = "GREAT"
                                game.great += 1
                            else:
                                game.performance = "BAD"
                                game.bad += 1
                            display_surf.blit(glow, buttonUpLeft)
                            game.upLeft.points.remove([currentPoint_x, currentPoint_y])

                        else:
                            game.performance = "MISS"
                            game.miss += 1

                elif event.key == K_p:
                    # upRight
                    if len(game.upRight.points) != 0:
                        game.upRight.isMissed = False
                        currentPoint_x = game.upRight.points[0][0]
                        currentPoint_y = game.upRight.points[0][1]
                        button_x = buttonUpRight[0]
                        button_y = buttonUpRight[1]
                        distance = Distance(currentPoint_x, currentPoint_y, button_x, button_y)
                        if currentPoint_x <= window_width - 74 and currentPoint_y >= 10:  # inside
                            if distance <= d / 3:
                                game.score.score += 200
                                game.performance = "PERFECT"
                            elif distance <= 2 * d / 3:
                                game.score.score += 100
                                game.performance = "GREAT"
                            else:
                                game.performance = "BAD"
                            display_surf.blit(glow, buttonUpRight)
                            game.upRight.points.remove([currentPoint_x, currentPoint_y])

                        else:
                            game.performance = "MISS"

                elif event.key == K_z:
                    # downLeft
                    if len(game.downLeft.points) != 0:
                        game.downLeft.isMissed = False
                        currentPoint_x = game.downLeft.points[0][0]
                        currentPoint_y = game.downLeft.points[0][1]
                        button_x = buttonDownLeft[0]
                        button_y = buttonDownLeft[1]
                        distance = Distance(currentPoint_x, currentPoint_y, button_x, button_y)
                        if currentPoint_x >= 10 and currentPoint_y <= window_height - 74:  # inside
                            if distance <= d / 3:
                                game.score.score += 200
                                game.performance = "PERFECT"
                            elif distance <= 2 * d / 3:
                                game.score.score += 100
                                game.performance = "GREAT"
                            else:
                                game.performance = "BAD"
                            display_surf.blit(glow, buttonDownLeft)
                            game.downLeft.points.remove([currentPoint_x, currentPoint_y])

                        else:
                            game.performance = "MISS"
                elif event.key == K_m:
                    # downRight
                    if len(game.downRight.points) != 0:
                        game.downRight.isMissed = False
                        currentPoint_x = game.downRight.points[0][0]
                        currentPoint_y = game.downRight.points[0][1]
                        button_x = buttonDownRight[0]
                        button_y = buttonDownRight[1]
                        distance = Distance(currentPoint_x, currentPoint_y, button_x, button_y)
                        if currentPoint_x <= window_width - 74 and currentPoint_y <= window_height - 74:  # inside
                            if distance <= d / 3:
                                game.score.score += 200
                                game.performance = "PERFECT"
                            elif distance <= 2 * d / 3:
                                game.score.score += 100
                                game.performance = "GREAT"
                            else:
                                game.performance = "BAD"
                            display_surf.blit(glow, buttonDownRight)
                            game.downRight.points.remove([currentPoint_x, currentPoint_y])

                        else:
                            game.performance = "MISS"
        game.update()
        try:
            if keyboard.is_pressed('a'):
                break
            else:
                pass
        except:
            break
        # if game.upLeft.spawnTime == 1000: ?????
        #     break
        pygame.display.update()
        fps_clock.tick(fps)


if __name__ == '__main__':
    main()
