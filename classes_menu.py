import pygame
import sys
from assets import colors
from classes import Board, Pacman, Game
from assets import cells
from functools import partial


class Menu():
    def __init__(self, buttons):
        self.buttons = buttons

    def draw(self, screen):
        pygame.font.init()
        myfont = pygame.font.Font('arcade_font.ttf', 26)
        label = myfont.render("MENU", 1, colors['blue'])
        screen.blit(label, (150, 50))
        for button in self.buttons:
            label = myfont.render(button.text, 1, colors['blue'])
            screen.blit(label, (button.x, button.y))
            button.draw(screen)

    def run(self, event):
        for button in self.buttons:
            button.handle_event(event)

    def start_new_game(screen, pacman_surface, board_surface, width,
                       height, clock):
        pacman = Pacman(pacman_surface, width // 2, 315, 3, 10)
        board = Board(cells)
        game = Game(pacman, board, screen, board_surface, pacman_surface,
                    clock, width, height)
        game.run()

    def resume_game():
        pass

    def save_game():
        pass

    def load_game():
        pass

    def exit_game():
        pygame.quit()
        sys.exit()


class Button():

    def __init__(self, text, x, y, width, height, command, *args):
        self.text = text
        self.command = command
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.command = partial(command, *args)
        self.rect = pygame.Rect(x, y, width, height)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_x, mouse_y):
                print("Przycisk został kliknięty!")
                self.command()

    def draw(self, screen):
        pygame.draw.rect(screen, colors['blue'],
                         (self.x, self.y, self.width, self.height), 1)
