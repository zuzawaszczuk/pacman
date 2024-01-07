import pygame
import sys
from classes_elements import Board, Pacman, Ghost
from classes_game import Game
from typing import Dict, Tuple, List
from pygame.surface import Surface
from pygame.time import Clock
from classes_button import Button
import copy
from math import pi

TColor = Tuple[int, int, int]


class Menu():
    def __init__(self, colors: Dict[str, TColor], screen: Surface,
                 clock: Clock, buttons: List[Button] = []) -> None:

        self.colors = colors
        self.screen = screen
        self.clock = clock
        self._buttons = buttons
        self._current_game = None

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    for button in self.buttons:
                        button.handle_event(event)

            self.screen.fill((0, 0, 0))
            self.draw()

            pygame.display.flip()
            self.clock.tick(30)

    def set_buttons(self, buttons):
        self._buttons = buttons

    @property
    def buttons(self):
        return self._buttons

    @property
    def current_game(self):
        return self._current_game

    def set_game(self, game):
        self._current_game = game

    def run_current_game(self):
        self.current_game.running_again()
        self.current_game.run()

    def start_new_game(self, pacman_surface: Surface, board_surface: Surface,
                       width: int, height: int,
                       cells: List[List[int]]) -> None:

        copy_cells = copy.deepcopy(cells)
        blinky = Ghost(width // 2, 200, 2.3, 8, "blinky")
        inky = Ghost(width // 2 - 30, 260, 2.3, 8, "inky")
        pinky = Ghost(width // 2, 260, 2.3, 8, "pinky")
        clyde = Ghost(width // 2 + 30, 260, 2.3, 8, "clyde")
        ghosts = [blinky, inky, pinky, clyde]
        pacman = Pacman(width // 2, 315, 3, 10)
        board = Board(copy_cells)
        game = Game(pacman, board, ghosts, self.screen, board_surface,
                    pacman_surface, self.clock, self.colors, width, height)
        game.run()
        self.set_game(game)
        self.run()

    def resume_game(self):
        self.run_current_game()

    def save_game(self):
        pass

    def load_game(self):
        pass

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def draw(self):
        pygame.font.init()
        myfont = pygame.font.Font('arcade_font.ttf', 55)
        label = myfont.render("Pacman", 1, self.colors['yellow'])
        self.screen.blit(label, (10, 10))
        myfont = pygame.font.Font('arcade_font.ttf', 32)
        label = myfont.render("MENU", 1, self.colors['blue'])
        self.screen.blit(label, (150, 100))

        for button in self.buttons:
            button.draw(self.screen, self.colors)
        pacman_menu = Pacman(410, 100, 1, 75)
        pacman_menu.change_direction(0.2*pi)
        pacman_menu.angle_added = 0.15*pi
        pacman_menu.draw(self.screen, self.colors)
