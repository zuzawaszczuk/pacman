import pygame
from classes_menu import Menu
from classes_button import Button
from assets import colors
pygame.init()

# I use smaller parameters for board surface to get effect of
# retro game.
small_width = 28 * 9
small_height = 31 * 9 + 20
width = 28 * 9 * 2
height = 31 * 9 * 2 + 40

board_surface = pygame.Surface((small_width, small_height), pygame.SRCALPHA)
pacman_surface = pygame.Surface((width, height), pygame.SRCALPHA)
screen = pygame.display.set_mode((width, height + 40))

pygame.display.set_caption("Pacman Game")
clock = pygame.time.Clock()

menu = Menu(colors)

button1 = Button(" Start New Game", 5, 140, 32, 495, 40, Menu.start_new_game,
                 menu, screen, pacman_surface, board_surface, width, height,
                 clock)
button2 = Button(" Resume", 5, 180, 32, 250, 40, Menu.resume_game, menu)
button3 = Button(" Save Game", 5, 220, 32, 340, 40, Menu.save_game)
button4 = Button(" Load Game", 5, 260, 32, 340, 40, Menu.load_game)
button5 = Button(" Exit", 5, 300, 32, 190, 40, Menu.exit_game)

buttons = [button1, button2, button3, button4, button5]
menu.set_buttons(buttons)

if __name__ == "__main__":
    menu.run(screen, clock)
