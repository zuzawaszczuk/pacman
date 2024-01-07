from classes_elements import Pacman, Board, Ghost
from main import cells, colors
import pygame.time
from classes_game import Game, EventHandler, Renderer, Serializer, Deserializer
import pytest
from math import pi


def test_game_init():
    pacman = Pacman(50, 50, 4, 5)
    clock = pygame.time.Clock()
    board = Board(cells)
    ghost = Ghost(5, 100, 150, 4, 9, False, "blinky")
    ghosts = [ghost]
    game = Game(pacman, board, ghosts, clock, colors, 50, 50)
    assert game.pacman == pacman
    assert game.board == board
    assert game.ghosts == ghosts
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
    game = Game(pacman, board, ghosts, clock, colors, 50, 50)
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
    game = Game(pacman, board, ghosts, clock, colors, 50, 50)
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


def test_renderer_init():
    renderer = Renderer('screen', 'board_surface', 'pacman_surface', colors)
    renderer.screen = 'screen'
    renderer.board_surface = 'board_surface'
    renderer.pacman_surface = 'pacman_surface'
    renderer.colors = colors


def test_serailizer_init():
    pacman = Pacman(50, 50, 4, 5)
    clock = pygame.time.Clock()
    board = Board(cells)
    ghost = Ghost(5, 100, 150, 4, 9, False, "blinky")
    ghosts = [ghost]
    game = Game(pacman, board, ghosts, 10, 10, 10, clock, colors, 50, 50)
    serializer = Serializer(game)
    assert serializer.game == game


def test_serailizer_serialize_pacman():
    pacman = Pacman(50, 50, 4, 5)
    clock = pygame.time.Clock()
    board = Board(cells)
    ghost = Ghost(5, 100, 150, 4, 9, False, "blinky")
    ghosts = [ghost]
    game = Game(pacman, board, ghosts, 10, 10, 10, clock, colors, 50, 50)
    serializer = Serializer(game)
    assert serializer.serialize_pacman() == {
            'x': 50,
            'y': 50,
            'speed': 4,
            'radius': 5,
            'lives': 3
        }


def test_serailizer_serialize_board():
    pacman = Pacman(50, 50, 4, 5)
    clock = pygame.time.Clock()
    board = Board(cells)
    ghost = Ghost(5, 100, 150, 4, 9, False, "blinky")
    ghosts = [ghost]
    game = Game(pacman, board, ghosts, 10, 10, 10, clock, colors, 50, 50)
    serializer = Serializer(game)
    assert serializer.serialize_board() == {
            'cells': cells
        }


def test_serailizer_serialize_ghost():
    pacman = Pacman(50, 50, 4, 5)
    clock = pygame.time.Clock()
    board = Board(cells)
    ghost = Ghost(5, 100, 150, 4, "blinky")
    ghosts = [ghost]
    game = Game(pacman, board, ghosts, 10, 10, 10, clock, colors, 50, 50)
    serializer = Serializer(game)
    assert serializer.serialize_ghost(ghost) == {
            "x": 5,
            "y": 100,
            "speed": 150,
            "radius": 4,
            "is_dead": False,
            "is_frightened": False,
            "at_home": True,
            "going_out": False,
            "next_tile": (0, 5)
        }


def test_deserailizer_deserialize_pacman():
    pacman = Pacman(50, 50, 4, 5)
    clock = pygame.time.Clock()
    board = Board(cells)
    ghost = Ghost(5, 100, 150, 4, 9, False, "blinky")
    ghosts = [ghost]
    game = Game(pacman, board, ghosts, 10, 10, 10, clock, colors, 50, 50)
    serializer = Serializer(game)
    assert serializer.serialize_pacman() == {
            'x': 50,
            'y': 50,
            'speed': 4,
            'radius': 5,
            'lives': 3
        }
    data = serializer.serialize_pacman()
    deserializer = Deserializer()
    pacman2 = deserializer.deserialize_pacman(data)
    assert pacman.x == pacman2.x
    assert pacman.y == pacman2.y
    assert pacman.speed == pacman2.speed
    assert pacman.radius == pacman2.radius
    assert pacman.lives == pacman2.lives


def test_deserailizer_deserialize_board():
    pacman = Pacman(50, 50, 4, 5)
    clock = pygame.time.Clock()
    board = Board(cells)
    ghost = Ghost(5, 100, 150, 4, 9, False, "blinky")
    ghosts = [ghost]
    game = Game(pacman, board, ghosts, 10, 10, 10, clock, colors, 50, 50)
    serializer = Serializer(game)
    assert serializer.serialize_board() == {
            'cells': cells
        }
    data = serializer.serialize_board()
    deserializer = Deserializer()
    board2 = deserializer.deserialize_board(data)
    assert board.cells == board2.cells


def test_deserailizer_deserialize_ghost():
    pacman = Pacman(50, 50, 4, 5)
    clock = pygame.time.Clock()
    board = Board(cells)
    ghost = Ghost(5, 100, 150, 4, "blinky")
    ghosts = [ghost]
    game = Game(pacman, board, ghosts, 10, 10, 10, clock, colors, 50, 50)
    serializer = Serializer(game)
    assert serializer.serialize_ghost(ghost) == {
            "x": 5,
            "y": 100,
            "speed": 150,
            "radius": 4,
            "is_dead": False,
            "is_frightened": False,
            "at_home": True,
            "going_out": False,
            "next_tile": (0, 5)
        }
    data = serializer.serialize_ghost(ghost)
    deserializer = Deserializer()
    ghost2 = deserializer.deserialize_ghost(data, "blinky")
    assert ghost.x == ghost2.x
    assert ghost.y == ghost2.y
    assert ghost.speed == ghost2.speed
    assert ghost.radius == ghost2.radius
    assert ghost.is_dead == ghost2.is_dead
    assert ghost.is_frightened == ghost2.is_frightened
    assert ghost.at_home == ghost2.at_home
    assert ghost.going_out == ghost2.going_out
    assert ghost.next_tile == ghost2.next_tile
