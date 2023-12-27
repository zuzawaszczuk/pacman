from classes import Pacman, Board, Game
from assets import cells
import pygame


def test_pacman_init():
    pacman = Pacman(5, 50, 50, 4, 5)
    assert pacman.screen == 5
    assert pacman.x == 50
    assert pacman.y == 50
    assert pacman.speed == 4
    assert pacman.radius == 5
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
