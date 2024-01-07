import pygame
import sys
import time
from math import pi
from classes_button import Button
from typing import List, Tuple, Dict
from pygame.surface import Surface
from pygame.time import Clock
from classes_elements import Pacman, Board, Ghost, Points
from classes_logic import ElementMover, GhostDetectingWalls, NormalGhostAction
from classes_logic import PacmanLogic, FrightenedGhostAction, DeadGhostAction
TColor = Tuple[int, int, int]


class Game():
    def __init__(self, pacman: Pacman, board: Board, ghosts: List[Ghost],
                 screen: Surface, board_surface: Surface,
                 pacman_surface: Surface, clock: Clock,
                 colors: Dict[str, TColor],
                 width: int, height: int, points: Points = Points(),
                 frightened_mode: bool = False, past_time: float = 0) -> None:
        self.pacman = pacman
        self.board = board
        self.ghosts = ghosts
        self.screen = screen
        self.board_surface = board_surface
        self.pacman_surface = pacman_surface
        self.clock = clock
        self.colors = colors
        self.width = width
        self.height = height
        self.points = points
        self._frightened_mode = frightened_mode
        self.past_time = past_time
        self._running = True
        self.start_time = time.time()
        self.frightened_time = 0
        self.current_duraction = 0

    def run(self) -> None:
        undone = True
        tick = 30.0
        self.start_time = time.time()
        self.current_duraction = 0
        button = Button("MENU", 400, 0, 23, 100, 40, self.back_to_menu)
        elementmover = ElementMover(self.board)
        ghostlogic = GhostDetectingWalls(self.board)
        pacmanlogic = PacmanLogic(self.board)
        normalghostsaction = NormalGhostAction(self.ghosts, ghostlogic,
                                               self.pacman, 0)
        frightenedghostsaction = FrightenedGhostAction(self.ghosts, ghostlogic,
                                                       self.pacman)
        deadghostsaction = DeadGhostAction(self.ghosts, ghostlogic)
        while self.running:
            self.current_duraction = time.time() - self.start_time
            timer = self.past_time + self.current_duraction

            elementmover.moves(self.pacman)
            if pacmanlogic.eats_points(self.pacman, self.points):
                normalghostsaction.dot_counter += 1

            # Action in game connected with pacman eating super point
            if pacmanlogic.eats_super_points(self.pacman, self.points):
                self.turn_on_frightened_mode()
                self.past_time -= 6
                self.frightened_time = timer

            # Logic of ghosts moves
            if self.is_frightened:
                frightenedghostsaction.run()
                if timer > self.frightened_time:
                    frightenedghostsaction.back_to_normal()
                    self.turn_off_frightened_mode()

            if not self.is_frightened:
                normalghostsaction.run(timer)

            deadghostsaction.dead_ghosts_go_back()

            door = False
            # Checks collison beetween pacman and ghots
            for ghost in self.ghosts:
                normalghostsaction.correct_next_tile(ghostlogic, ghost)
                if (not ghost.at_home and not ghost.going_out) or \
                        (ghost.at_home and ghost.going_out):
                    # Ghost is moving, when he is out of home and already go
                    # through door or is inside home and goes out move to door
                    elementmover.moves(ghost)
                if ghost.going_out:
                    door = True

                if ghostlogic.collision(ghost, self.pacman):
                    if not self.is_frightened and not ghost.is_dead:
                        self.pacman.lives -= 1
                        normalghostsaction.go_home()
                        self.pacman.go_home()
                        normalghostsaction.dot_counter = 0
                        door = False
                        tick = 0.25
                    elif not ghost.is_dead:
                        normalghostsaction.dot_counter = 0
                        ghost.not_frightened()
                        ghost.dead()
                        self.points.add_to_score(200)

            # Collecting 4 super points gives additional life
            if undone is True and self.points.super_point_left == 0:
                self.pacman.lives += 1
                undone = False

            # Handles keyboard events to change directions of pacman
            eventhandler = EventHandler(self.pacman)
            for event in pygame.event.get():
                eventhandler.handle_event(event)
                # Handles mouse event - exit game to menu if button clicked
                button.handle_event(event)

            # Renders consequences of game logic on surfaces
            renderer = Renderer(self.screen, self.board_surface,
                                self.pacman_surface, self.colors)
            # Cleans surfaces
            renderer.cleans_surfaces()

            # Draws on surfaces
            renderer.render_board(self.board, door)
            renderer.render_pacman(self.pacman)
            renderer.render_ghosts(self.ghosts)

            # Scales board surface to bigger one
            scaled_board_surface = pygame.transform.scale(
                self.board_surface, (self.width, self.height))

            # Puts surfaces on screen
            self.screen.blit(scaled_board_surface, (0, 40))
            self.screen.blit(self.pacman_surface, (0, 40))

            # On top of surfaces last renders to draw on screen
            renderer.render_score(self.points.score)
            renderer.render_lives(self.pacman)
            renderer.render_high_score(self.points.high_score)
            button.draw(self.screen, self.colors)

            # Checks if player won
            if self.points.points_to_win == 0:
                renderer.won()
                tick = 0.25
                self.not_running()

            # Checks if player lost
            if self.pacman.lives == 0:
                renderer.lost()
                tick = 0.25
                self.not_running()

            pygame.display.flip()
            self.clock.tick(tick)
            tick = 30

    @property
    def running(self) -> bool:
        return self._running

    def not_running(self,) -> None:
        self.past_time += self.current_duraction
        self._running = False

    def running_again(self) -> None:
        self._running = True

    def back_to_menu(self) -> None:
        self.not_running()

    @property
    def is_frightened(self) -> bool:
        return self._frightened_mode

    def turn_on_frightened_mode(self) -> None:
        self._frightened_mode = True

    def turn_off_frightened_mode(self) -> None:
        self._frightened_mode = False


class EventHandler():
    def __init__(self, pacman: Pacman):
        self.pacman = pacman

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.pacman.change_direction(pi)
            elif event.key == pygame.K_RIGHT:
                self.pacman.change_direction(0)
            elif event.key == pygame.K_UP:
                self.pacman.change_direction(pi/2)
            elif event.key == pygame.K_DOWN:
                self.pacman.change_direction(1.5*pi)


class Renderer():
    def __init__(self, screen: Surface, board_surface: Surface,
                 pacman_surface: Surface, colors: Dict[str, TColor]) -> None:
        self.screen = screen
        self.board_surface = board_surface
        self.pacman_surface = pacman_surface
        self.colors = colors

    def cleans_surfaces(self) -> None:
        self.screen.fill((0, 0, 0))
        self.board_surface.fill((0, 0, 0))
        self.pacman_surface.fill((0, 0, 0, 0))

    def render_board(self, board: Board, door: bool) -> None:
        board.draw(self.board_surface, self.colors, door)

    def render_pacman(self, pacman: Pacman) -> None:
        pacman.animate_mouth()
        pacman.draw(self.pacman_surface, self.colors)

    def render_ghosts(self, ghosts: List[Ghost]) -> None:
        for ghost in ghosts:
            width = 2*ghost.radius + 8
            if ghost.is_dead:
                image = pygame.image.load("ghosts/dead.png")
            elif ghost.is_frightened:
                image = pygame.image.load("ghosts/frightened.png")
            else:
                image = pygame.image.load(f"ghosts/{ghost.name}.png")
            scaled_image = pygame.transform.scale(image, (width, width))
            rect = [ghost.x - ghost.radius - 3, ghost.y - ghost.radius - 3,
                    width, width]
            self.pacman_surface.blit(scaled_image, rect)

    def render_score(self, score: int) -> None:
        pygame.font.init()
        myfont = pygame.font.Font('arcade_font.ttf', 22)
        label = myfont.render(f"SCORE:{score}", 1, self.colors['blue'])
        self.screen.blit(label, (10, 600))

    def render_lives(self, pacman: Pacman) -> None:
        for i in range(pacman.lives):
            pygame.draw.arc(self.screen, self.colors['yellow'],
                            [400 + 20 * i, 600,
                            2 * pacman.radius, 2 * pacman.radius],
                            pi/4, 1.75*pi, pacman.radius)

    def render_high_score(self, high_score: int) -> None:
        pygame.font.init()
        myfont = pygame.font.Font('arcade_font.ttf', 22)
        label = myfont.render(f"HIGH SCORE:{high_score}", 1,
                              self.colors['blue'])
        self.screen.blit(label, (10, 10))

    def won(self) -> None:
        myfont = pygame.font.Font('arcade_font.ttf', 42)
        label = myfont.render("!!YOU WON!!", 1, self.colors['green'])
        pygame.draw.rect(self.screen, self.colors['black'], [0, 200, 600, 230])
        self.screen.blit(label, (20, 280))

    def lost(self) -> None:
        myfont = pygame.font.Font('arcade_font.ttf', 42)
        label = myfont.render("YOU LOST!;(", 1, self.colors['red'])
        pygame.draw.rect(self.screen, self.colors['black'], [0, 200, 600, 230])
        self.screen.blit(label, (20, 280))
