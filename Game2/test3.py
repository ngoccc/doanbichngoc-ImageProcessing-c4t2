import pygame

display_surf = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
window_width, window_height = pygame.display.get_surface().get_size()
result = pygame.image.load("E:\\C4T\\Image Processing\\Game2\\images\\close\\result.png")
result = pygame.transform.scale(result, (window_width, window_height))
rank_A = pygame.image.load("E:\\C4T\\Image Processing\\Game2\\images\\ranking\\A.png")
WHITE = (255, 255, 255)
pygame.mixer.init()
score = 10
scoree = 19000

def main():
    pygame.init()
    while True:
        pygame.mixer.music.load("E:\\C4T\\Image Processing\\Game2\\Lucky-Strike.mp3")
        pygame.mixer.music.play(1)
        display_surf.blit(result, (0, 0))
        font = pygame.font.Font('Bolt.ttf', 45)
        result_srf = font.render('%s' % (score), True, WHITE)
        display_surf.blit(result_srf, (1020, 160))
        display_surf.blit(result_srf, (1020, 225))
        display_surf.blit(result_srf, (1020, 290))
        display_surf.blit(result_srf, (1020, 357))
        aa = font.render('%s' % (scoree), True, WHITE)
        display_surf.blit(aa, (980, 425))
        display_surf.blit(rank_A, (500, 500))
        pygame.display.update()


if __name__ == '__main__':
    main()
