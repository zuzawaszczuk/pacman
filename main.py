import pygame
import sys
from classes import Pacman
from assets import draw_board

pygame.init()

screen_width = 224
screen_height = 248
real_width = 448
real_height = 496
screen = pygame.Surface((screen_width, screen_height))
real_screen = pygame.display.set_mode((real_width, real_height))
pygame.display.set_caption("Pacman Game")

pacman = Pacman(screen, screen_width // 2, screen_height // 2, 1, 5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                pacman.x -= pacman.speed
            elif event.key == pygame.K_RIGHT:
                pacman.x += pacman.speed
            elif event.key == pygame.K_UP:
                pacman.y -= pacman.speed
            elif event.key == pygame.K_DOWN:
                pacman.y += pacman.speed

    # screen.fill((0, 0, 0))
    draw_board(screen)
    pygame.transform.scale(screen, (real_width, real_height), real_screen)
    pacman.draw()
    pygame.display.flip()
