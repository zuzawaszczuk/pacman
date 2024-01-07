from classes_elements import Pacman, Board, Ghost
from main import cells, colors
import pygame.time
from classes_game import Game, EventHandler
import pytest
from math import pi


def test_game_init():
    pacman = Pacman(50, 50, 4, 5)
    clock = pygame.time.Clock()
    board = Board(cells)
    ghost = Ghost(5, 100, 150, 4, 9, False, "blinky")
    ghosts = [ghost]
    game = Game(pacman, board, ghosts, 10, 10, 10, clock, colors, 50, 50)
    assert game.pacman == pacman
    assert game.board == board
    assert game.ghosts == ghosts
    assert game.screen == 10
    assert game.board_surface == 10
    assert game.pacman_surface == 10
    assert game.clock == clock
    assert game.colors == colors
    assert game.width == 50
    assert game.height == 50
    assert game.points.points_to_win == 242
    assert game.points.super_point_left == 4


def test_game_running():
    pacman = Pacman(50, 50, 4, 5)
    clock = pygame.time.Clock()
    board = Board(cells)
    ghost = Ghost(5, 100, 150, 4, 9, False, "blinky")
    ghosts = [ghost]
    game = Game(pacman, board, ghosts, 10, 10, 10, clock, colors, 50, 50)
    assert game.running is True
    game.not_running()
    assert game.running is False
    game.running_again()
    assert game.running is True


def test_game_frightened_mode():
    pacman = Pacman(50, 50, 4, 5)
    clock = pygame.time.Clock()
    board = Board(cells)
    ghost = Ghost(5, 100, 150, 4, 9, False, "blinky")
    ghosts = [ghost]
    game = Game(pacman, board, ghosts, 10, 10, 10, clock, colors, 50, 50)
    assert game.is_frightened is False
    game.turn_on_frightened_mode()
    assert game.is_frightened is True
    game.turn_off_frightened_mode()
    assert game.is_frightened is False


def test_event_handler_init():
    pacman = Pacman(50, 50, 4, 5)
    event_handler = EventHandler(pacman)
    assert event_handler.pacman == pacman


def test_handle_event_quit():
    pacman = Pacman(50, 50, 4, 5)
    event_handler = EventHandler(pacman)
    quit_event = pygame.event.Event(pygame.QUIT)
    with pytest.raises(SystemExit):
        event_handler.handle_event(quit_event)


def test_handle_event_key_left():
    pacman = Pacman(50, 50, 4, 5)
    event_handler = EventHandler(pacman)
    key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_LEFT})
    assert pacman.angle == 0
    event_handler.handle_event(key_event)
    assert pacman.angle == pi


def test_handle_event_key_right():
    pacman = Pacman(50, 50, 4, 5)
    event_handler = EventHandler(pacman)
    key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_RIGHT})
    pacman.change_direction(pi)
    assert pacman.angle == pi
    event_handler.handle_event(key_event)
    assert pacman.angle == 0


def test_handle_event_key_up():
    pacman = Pacman(50, 50, 4, 5)
    event_handler = EventHandler(pacman)
    key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_UP})
    assert pacman.angle == 0
    event_handler.handle_event(key_event)
    assert pacman.angle == pi/2


def test_handle_event_key_down():
    pacman = Pacman(50, 50, 4, 5)
    event_handler = EventHandler(pacman)
    key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_DOWN})
    assert pacman.angle == 0
    event_handler.handle_event(key_event)
    assert pacman.angle == 1.5*pi


def test_handle_event_key_unknown():
    pacman = Pacman(50, 50, 4, 5)
    event_handler = EventHandler(pacman)
    key_event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_SPACE})
    assert pacman.angle == 0
    event_handler.handle_event(key_event)
    assert pacman.angle == 0
