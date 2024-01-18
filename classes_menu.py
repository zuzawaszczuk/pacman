import pygame
import sys
import json
from classes_elements import Board, Pacman, Ghost, Points
from classes_game import Game, Serializer, Deserializer
from typing import Dict, Tuple, List
from pygame.surface import Surface
from pygame.time import Clock
from classes_button import Button
import copy
from math import pi

TColor = Tuple[int, int, int]


class Menu():
    def __init__(self, colors: Dict[str, TColor], screen: Surface,
                 board_surface: Surface, pacman_surface: Surface,
                 clock: Clock, width: int, height: int,
                 buttons: List[Button] = [],
                 global_high_score: int = 0) -> None:

        self.colors = colors
        self.screen = screen
        self.board_surface = board_surface
        self.pacman_surface = pacman_surface
        self.clock = clock
        self.width = width
        self.height = height
        self._buttons = buttons
        self.global_high_score = global_high_score
        self._current_game: Game | None = None

    def run(self) -> None:
        self.get_high_score_from_saves()
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

    def set_buttons(self, buttons: List[Button]) -> None:
        self._buttons = buttons

    @property
    def buttons(self) -> List[Button]:
        return self._buttons

    @property
    def current_game(self) -> Game:
        return self._current_game

    def set_game(self, game: Game | None) -> None:
        self._current_game = game
        self.global_high_score = max(self.global_high_score,
                                     game.points.high_score)

    def run_current_game(self) -> None:
        self.current_game.running_again()
        self.current_game.run(self.screen,
                              self.board_surface, self.pacman_surface)

    def start_new_game(self, cells: List[List[int]]) -> None:

        copy_cells = copy.deepcopy(cells)
        blinky = Ghost(self.width // 2, 200, 2.3, 8, "blinky")
        inky = Ghost(self.width // 2 - 30, 260, 2.3, 8, "inky")
        pinky = Ghost(self.width // 2, 260, 2.3, 8, "pinky")
        clyde = Ghost(self.width // 2 + 30, 260, 2.3, 8, "clyde")
        ghosts = [blinky, inky, pinky, clyde]
        pacman = Pacman(self.width // 2, 315, 3, 10)
        board = Board(copy_cells)
        points = Points()
        game = Game(pacman, board, ghosts, self.clock, self.colors,
                    self.width, self.height, self.global_high_score,
                    points, False, 0, 0)
        game.run(self.screen, self.board_surface, self.pacman_surface)
        self.set_game(game)
        self.run()

    def resume_game(self):
        self.run_current_game()

    def save_game(self):
        text = ("You cannot save the game because"
                " no game is currently in progress.")
        try:
            if self.current_game is None:
                raise ValueError(text)
        except ValueError as e:
            print(f"Error: {e}")
            return

        try:
            with open("saved_games.json", 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {}

        keys_list = list(existing_data.keys())
        user_input = self.gets_user_input_save(keys_list)
        serializer = Serializer(self.current_game)
        existing_data[user_input] = serializer.serialize()

        with open("saved_games.json", 'w') as file:
            json.dump(existing_data, file, indent=1)
            print("Game state saved successfully!!")

    def load_game(self):
        try:
            with open("saved_games.json", 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {}

        if existing_data == {}:
            print("No saved game states to load.")
            return

        keys_list = list(existing_data.keys())
        print(f'Avaiable saves to load: {keys_list}')

        save = self.gets_user_input_load(keys_list)
        print(f'Loading save from {save}')
        deserializer = Deserializer()
        game = deserializer.deserialize(existing_data[save],
                                        self.global_high_score, self.clock,
                                        self.colors, self.width, self.height)
        game.run(self.screen, self.board_surface, self.pacman_surface)
        if game.points.points_to_win == 0:
            print("Can't load the game that was already won!")
        self.set_game(game)
        self.run()

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def gets_user_input_save(self, keys_list: List) -> str:
        instruction = "Enter the name under which you want to save the game: "
        while True:
            try:
                user_input = input(instruction)
                if not user_input.strip():
                    raise ValueError("You cannot enter an empty name.")
                if user_input in keys_list:
                    message = ("A game state is already saved under the name."
                               "Do you want to overwrite it? (y/n): ")
                    user_response = input(message)

                    if user_response.lower() == 'y':
                        print("Saving game state...")
                        break
                    else:
                        print("Game state not overwritten."
                              "Choose a different name!")
                break
            except ValueError as e:
                print(f"Error: {e}")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        return user_input

    def gets_user_input_load(self, keys_list: List) -> str:
        instruction = "Enter the name of the saved game you want to load: "
        while True:
            try:
                user_input = input(instruction)
                if user_input not in keys_list:
                    raise ValueError("This saved game state does not exist."
                                     "Please enter a valid name.")
                break
            except ValueError as e:
                print(f"Error: {e}")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        return user_input

    def get_high_score_from_saves(self):
        try:
            with open("saved_games.json", 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = {}

        for save in existing_data.keys():
            high_score = existing_data[save]['points'].get('high_score', 0)
            if high_score > self.global_high_score:
                self.global_high_score = high_score

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
