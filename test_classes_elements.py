from classes_elements import Pacman, Board, Ghost, Character, Points
from main import cells
from math import pi
import pytest


def test_character_init():
    character = Character(7.5, 10.5, 3.5, 4)
    assert character.x == 7.5
    assert character.y == 10.5
    assert character.speed == 3.5
    assert character.radius == 4
    assert character.angle == 0.0


def test_change_direction():
    character = Character(7.5, 10.5, 3.5, 4)
    assert character.angle == 0.0
    character.change_direction(pi/2)
    assert character.angle == pi/2


def test_pacman_init():
    pacman = Pacman(50.5, 50.8, 4.2, 5)
    assert pacman.x == 50.5
    assert pacman.y == 50.8
    assert pacman.speed == 4.2
    assert pacman.radius == 5
    assert pacman.lives == 3
    assert pacman.angle == 0.0
    assert pacman.angle_added == 0
    assert pacman.mouth_direction == 1


def test_pacman_animate_mouth():
    pacman = Pacman(50, 50, 4, 5)
    assert pacman.angle_added == 0
    pacman.animate_mouth()
    assert pacman.angle_added == 0.03 * pi


def test_pacman_go_home():
    pacman = Pacman(50, 50, 4, 5)
    assert pacman.x == 50
    assert pacman.y == 50
    pacman.go_home()
    assert pacman.x == 28*9
    assert pacman.y == 315
    assert pacman.angle == 0


def test_ghost_init():
    ghost = Ghost(100, 150, 2.6, 9, "blinky")
    assert ghost.x == 100
    assert ghost.y == 150
    assert ghost.speed == 2.6
    assert ghost.radius == 9
    assert ghost.name == "blinky"
    assert ghost.is_dead is False
    assert ghost.is_frightened is False
    assert ghost.at_home is True
    assert ghost.going_out is False
    assert ghost.next_tile == (5, 8)


def test_ghost_set_cord():
    ghost = Ghost(100, 150, 2.6, 9, "blinky")
    assert ghost.x == 100
    assert ghost.y == 150
    ghost.set_cord(2, 5)
    assert ghost.x == 2
    assert ghost.y == 5


def test_ghost_dead_is_alive():
    ghost = Ghost(100, 150, 2.6, 9, "blinky")
    assert ghost.is_dead is False
    ghost.dead()
    assert ghost.is_dead is True
    ghost.is_alive()
    assert ghost.is_dead is False


def test_ghost_scared_not_frightened():
    ghost = Ghost(100, 150, 2.6, 9, "blinky")
    assert ghost.is_frightened is False
    ghost.frightened()
    assert ghost.is_frightened is True
    ghost.not_frightened()
    assert ghost.is_frightened is False


def test_ghost_out_of_home_back_at_home():
    ghost = Ghost(100, 150, 2.6, 9, "blinky")
    assert ghost.at_home is True
    ghost.out_of_home()
    assert ghost.at_home is False
    ghost.back_at_home()
    assert ghost.at_home is True


def test_ghost_start_going_out_end_going_out():
    ghost = Ghost(100, 150, 2.6, 9, "blinky")
    assert ghost.going_out is False
    ghost.start_going_out()
    assert ghost.going_out is True
    ghost.end_going_out()
    assert ghost.going_out is False


def test_ghost_set_next_tile():
    ghost = Ghost(100, 150, 2.6, 9, "blinky")
    assert ghost.next_tile == (5, 8)
    ghost.set_next_tile(1, 1)
    assert ghost.next_tile == (1, 1)


def test_ghost_reset_next_tile():
    ghost = Ghost(100, 150, 2.6, 9, "blinky")
    assert ghost.next_tile == (5, 8)
    ghost.set_next_tile(1, 1)
    assert ghost.next_tile == (1, 1)
    ghost.reset_next_tile()
    assert ghost.next_tile == (5, 8)


def test_ghost_left():
    ghost = Ghost(100, 150, 2.6, 9, "blinky")
    assert ghost.next_tile == (5, 8)
    assert ghost.angle == 0
    ghost.left()
    assert ghost.next_tile == (4, 8)
    assert ghost.angle == pi


def test_ghost_right():
    ghost = Ghost(100, 150, 2.6, 9, "blinky")
    assert ghost.next_tile == (5, 8)
    assert ghost.angle == 0
    ghost.right()
    assert ghost.next_tile == (6, 8)
    assert ghost.angle == 0


def test_ghost_up():
    ghost = Ghost(100, 150, 2.6, 9, "blinky")
    assert ghost.next_tile == (5, 8)
    assert ghost.angle == 0
    ghost.up()
    assert ghost.next_tile == (5, 7)
    assert ghost.angle == pi/2


def test_ghost_down():
    ghost = Ghost(100, 150, 2.6, 9, "blinky")
    assert ghost.next_tile == (5, 8)
    assert ghost.angle == 0
    ghost.down()
    assert ghost.next_tile == (5, 9)
    assert ghost.angle == 1.5 * pi


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


def test_board_is_door():
    board = Board(cells)
    assert board.is_door(12, 14) == 1
    assert board.is_door(13, 0) == 0


def test_board_set_cell():
    board = Board(cells)
    assert board.cells[1][1] == 1
    board.set_cell(1, 1, 5)
    assert board.cells[1][1] == 5


def test_points_innit():
    points = Points()
    assert points.score == 0
    assert points.points_to_win == 242
    assert points.super_point_left == 4
    assert points.high_score == 0


def test_points_add_to_score_typical():
    points = Points()
    assert points.score == 0
    points.add_to_score(10)
    assert points.score == 10


def test_points_add_to_score_negative_value():
    points = Points()
    with pytest.raises(ValueError):
        points.add_to_score(-10)


def test_one_points_eaten():
    points = Points()
    assert points.points_to_win == 242
    points.one_point_eaten()
    assert points.points_to_win == 241


def test_super_point_eaten():
    points = Points()
    assert points.super_point_left == 4
    points.super_point_eaten()
    assert points.super_point_left == 3
