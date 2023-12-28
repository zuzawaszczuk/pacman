import pygame
import sys
from classes import Board, Pacman, Game, Ghost
from assets import cells
import copy


class Menu():
    def __init__(self, colors, buttons=[]):
        self.colors = colors
        self._buttons = buttons
        self._current_game = None

    def run(self, screen, clock):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                else:
                    for button in self.buttons:
                        button.handle_event(event)

            screen.fill((0, 0, 0))
            self.draw(screen, self.colors)

            pygame.display.flip()
            clock.tick(30)

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

    def start_new_game(self, screen, pacman_surface, board_surface, width,
                       height, clock):
        copy_cells = copy.deepcopy(cells)
        blinky = Ghost(pacman_surface, width // 2, 250, 3, 10, 0, "blinky")
        ghosts = [blinky]
        pacman = Pacman(pacman_surface, width // 2, 315, 3, 10)
        board = Board(copy_cells)
        game = Game(pacman, board, ghosts, screen, board_surface,
                    pacman_surface, clock, width, height)
        game.run()
        self.set_game(game)
        self.run(screen, clock)

    def resume_game(self):
        self.run_current_game()

    def save_game():
        pass

    def load_game():
        pass

    def exit_game():
        pygame.quit()
        sys.exit()

    def draw(self, screen, colors):
        pygame.font.init()
        myfont = pygame.font.Font('arcade_font.ttf', 32)
        label = myfont.render("MENU", 1, colors['blue'])
        screen.blit(label, (180, 50))
        for button in self.buttons:
            button.draw(screen, colors)
