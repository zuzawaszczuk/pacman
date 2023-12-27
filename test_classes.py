from classes import Pacman, Board, Game
from assets import cells
import pygame
from math import pi


def test_pacman_init():
    pacman = Pacman(5, 50, 50, 4, 5)
    assert pacman.screen == 5
    assert pacman.x == 50
    assert pacman.y == 50
    assert pacman.speed == 4
    assert pacman.radius == 5
    assert pacman.lives == 3
    assert pacman.angle == 0
    assert pacman.angle_added == 0
    assert pacman.mouth_direction == 1


def test_board_init():
    board = Board(cells)
    assert board.cells[1][1] == 1
    assert board.cells[0][11] == 11


def test_board_is_wall():
    board = Board(cells)
    assert board.is_wall(2, 9) == 1
    assert board.is_wall(13, 13) == 0


def test_board_is_point():
    board = Board(cells)
    assert board.is_point(1, 1) == 1
    assert board.is_point(13, 13) == 0


def test_board_is_super_point():
    board = Board(cells)
    assert board.is_super_point(3, 1) == 1
    assert board.is_super_point(13, 13) == 0


def test_board_set_cell():
    board = Board(cells)
    assert board.cells[1][1] == 1
    board.set_cell(1, 1, 5)
    assert board.cells[1][1] == 5


def test_game_init():
    pacman = Pacman(5, 50, 50, 4, 5)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    assert game.pacman == pacman
    assert game.board == board
    assert game.screen == 10
    assert game.board_surface == 10
    assert game.pacman_surface == 10
    assert game.clock == clock
    assert game.width == 50
    assert game.height == 50
    assert game.points == 0
    assert game.points_to_win == 242
    assert game.super_point_left == 4


def test_eats():
    pacman = Pacman(5, 20, 20, 4, 5)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    x, y = game.my_cell(pacman)
    assert board.is_point(y, x) == 1
    assert game.points == 0
    assert game.points_to_win == 242
    game.eats(pacman, board)
    assert board.is_point(y, x) == 0
    assert game.points == 10
    assert game.points_to_win == 241


def test_rigth_space_true():
    pacman = Pacman(5, 100, 30, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    assert game.right_space(pacman) == 1


def test_rigth_space_false():
    pacman = Pacman(5, 100, 10, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    assert game.right_space(pacman) == 0


def test_rigth_space_tunnel():
    pacman = Pacman(5, 14*9, 28*9, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    assert game.right_space(pacman) == 1


def test_left_space_true():
    pacman = Pacman(5, 100, 30, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    assert game.left_space(pacman) == 1


def test_left_space_false():
    pacman = Pacman(5, 20, 70, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    assert game.left_space(pacman) == 0


def test_left_space_tunnel():
    pacman = Pacman(5, 0, 28*9, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    assert game.right_space(pacman) == 1


def test_down_space_true():
    pacman = Pacman(5, 20, 20, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    assert game.down_space(pacman) == 1


def test_down_space_false():
    pacman = Pacman(5, 60, 30, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    assert game.down_space(pacman) == 0


def test_up_space_true():
    pacman = Pacman(5, 20, 70, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    assert game.up_space(pacman) == 1


def test_up_space_false():
    pacman = Pacman(5, 30, 20, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    assert game.up_space(pacman) == 0


def test_moves_right_typical():
    pacman = Pacman(5, 100, 30, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    assert game.right_space(pacman) == 1
    assert pacman.x == 100
    game.moves(pacman)
    assert pacman.x == 103


def test_moves_right_collison():
    pacman = Pacman(5, 100, 10, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    assert game.right_space(pacman) == 0
    assert pacman.x == 100
    game.moves(pacman)
    assert pacman.x == 100


def test_moves_left_typical():
    pacman = Pacman(5, 100, 30, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    pacman.angle = pi
    assert game.left_space(pacman) == 1
    assert pacman.x == 100
    game.moves(pacman)
    assert pacman.x == 97


def test_moves_left_collison():
    pacman = Pacman(5, 20, 10, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    pacman.angle = pi
    assert game.left_space(pacman) == 0
    assert pacman.x == 20
    game.moves(pacman)
    assert pacman.x == 20


def test_moves_up_typical():
    pacman = Pacman(5, 100, 30, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    pacman.angle = pi/2
    assert game.up_space(pacman) == 1
    assert pacman.y == 30
    game.moves(pacman)
    assert pacman.y == 27


def test_moves_up_collison():
    pacman = Pacman(5, 20, 20, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    pacman.angle = pi/2
    assert game.up_space(pacman) == 0
    assert pacman.y == 20
    game.moves(pacman)
    assert pacman.y == 20


def test_moves_down_typical():
    pacman = Pacman(5, 30, 30, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    pacman.angle = 1.5*pi
    assert game.down_space(pacman) == 1
    assert pacman.y == 30
    game.moves(pacman)
    assert pacman.y == 33


def test_moves_down_collison():
    pacman = Pacman(5, 60, 30, 3, 10)
    clock = pygame.time.Clock()
    board = Board(cells)
    game = Game(pacman, board, 10, 10, 10, clock, 50, 50)
    pacman.angle = 1.5*pi
    assert game.down_space(pacman) == 0
    assert pacman.y == 30
    game.moves(pacman)
    assert pacman.y == 30
