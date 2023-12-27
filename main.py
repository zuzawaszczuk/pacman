import pygame
import sys
from classes_menu import Button, Menu

pygame.init()

# I use smaller parameters for board surface to get effect of
# retro game.
small_width = 28 * 9
small_height = 31 * 9 + 20
width = 28 * 9 * 2
height = 31 * 9 * 2 + 40
board_surface = pygame.Surface((small_width, small_height))
pacman_surface = pygame.Surface((width, height), pygame.SRCALPHA)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pacman Game")
clock = pygame.time.Clock()

button1 = Button(" Start New Game", 5, 140, 495, 40, Menu.start_new_game,
                 screen, pacman_surface, board_surface, width, height, clock)
button2 = Button(" Resume", 5, 180, 250, 40, Menu.resume_game)
button3 = Button(" Save Game", 5, 220, 340, 40, Menu.save_game)
button4 = Button(" Load Game", 5, 260, 340, 40, Menu.load_game)
button5 = Button(" Exit", 5, 300, 190, 40, Menu.exit_game)
buttons = [button1, button2, button3, button4, button5]
menu = Menu(buttons)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            menu.run(event)
    screen.fill((0, 0, 0))
    menu.draw(screen)
    menu.run(event)

    pygame.display.flip()
    clock.tick(30)
