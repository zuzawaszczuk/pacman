import pygame
import sys
from classes_menu import Button, Menu

pygame.init()

# I use smaller parameters for board surface to get effect of
# retro game.
small_width = 224
small_height = 248
width = 448
height = 496
board_surface = pygame.Surface((small_width, small_height))
pacman_surface = pygame.Surface((width, height), pygame.SRCALPHA)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pacman Game")
clock = pygame.time.Clock()

button1 = Button(" Start New Game", 20, 140, 400, 40, Menu.start_new_game,
                 screen, pacman_surface, board_surface, width, height, clock)
button2 = Button(" Resume", 20, 180, 200, 40, Menu.resume_game)
button3 = Button(" Save Game", 20, 220, 270, 40, Menu.save_game)
button4 = Button(" Load Game", 20, 260, 270, 40, Menu.load_game)
button5 = Button(" Exit", 20, 300, 150, 40, Menu.exit_game)
buttons = [button1, button2, button3, button4, button5]
menu = Menu(buttons)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        else:
            menu.run(event)

    menu.draw(screen)
    menu.run(event)

    pygame.display.flip()
    clock.tick(30)
