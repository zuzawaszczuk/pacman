from classes_logic import CellLogic, ElementMover, GhostDetectingWalls
from classes_logic import PacmanLogic
from classes_elements import Ghost, Board, Pacman, Points
from main import cells
from math import pi


def test_cell_logic_innit():
    celllogic = CellLogic(cells)
    assert celllogic.board == cells


def test_cell_logic_left_cell():
    celllogic = CellLogic(cells)
    pacman = Pacman(40, 20, 2, 10)
    assert celllogic.left_cell(pacman) == (1, 1)


def test_cell_logic_right_cell():
    celllogic = CellLogic(cells)
    pacman = Pacman(40, 20, 2, 10)
    assert celllogic.right_cell(pacman) == (3, 1)


def test_cell_logic_down_cell():
    celllogic = CellLogic(cells)
    pacman = Pacman(40, 20, 2, 10)
    assert celllogic.down_cell(pacman) == (2, 2)


def test_cell_logic_up_cell():
    celllogic = CellLogic(cells)
    pacman = Pacman(40, 20, 2, 10)
    assert celllogic.up_cell(pacman) == (2, 0)


def test_cell_logic_my_cell():
    celllogic = CellLogic(cells)
    pacman = Pacman(40, 20, 2, 10)
    assert celllogic.my_cell(pacman) == (2, 1)


def test_cell_logic_collision():
    celllogic = CellLogic(cells)
    pacman = Pacman(40, 20, 2, 10)
    ghost = Pacman(40, 20, 2, 10)
    assert celllogic.collision(pacman, ghost) is True
    ghost.x = 100
    assert celllogic.collision(pacman, ghost) is False


def test_rigth_space_true():
    pacman = Pacman(100, 30, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    assert elementmover.right_space(pacman) is True


def test_rigth_space_false():
    pacman = Pacman(100, 10, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    assert elementmover.right_space(pacman) is False


def test_rigth_space_tunnel():
    pacman = Pacman(14*9, 28*9, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    assert elementmover.right_space(pacman) is True


def test_left_space_true():
    pacman = Pacman(100, 30, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    assert elementmover.left_space(pacman) is True


def test_left_space_false():
    pacman = Pacman(20, 70, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    assert elementmover.left_space(pacman) is False


def test_left_space_tunnel():
    pacman = Pacman(5, 0, 28*9, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    assert elementmover.right_space(pacman) is True


def test_down_space_true():
    pacman = Pacman(5, 20, 20, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    assert elementmover.down_space(pacman) is True


def test_down_space_false():
    pacman = Pacman(60, 30, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    assert elementmover.down_space(pacman) is False


def test_up_space_true():
    pacman = Pacman(20, 70, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    assert elementmover.up_space(pacman) is True


def test_up_space_false():
    pacman = Pacman(30, 20, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    assert elementmover.up_space(pacman) is False


def test_moves_right_typical():
    pacman = Pacman(100, 30, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    assert elementmover.right_space(pacman) is True
    assert pacman.x == 100
    elementmover.moves(pacman)
    assert pacman.x == 103


def test_moves_right_collison():
    pacman = Pacman(100, 10, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    assert elementmover.right_space(pacman) is False
    assert pacman.x == 100
    elementmover.moves(pacman)
    assert pacman.x == 100


def test_moves_left_typical():
    pacman = Pacman(100, 30, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    pacman.change_direction(pi)
    assert elementmover.left_space(pacman) is True
    assert pacman.x == 100
    elementmover.moves(pacman)
    assert pacman.x == 97


def test_moves_left_collison():
    pacman = Pacman(20, 10, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    pacman.change_direction(pi)
    assert elementmover.left_space(pacman) is False
    assert pacman.x == 20
    elementmover.moves(pacman)
    assert pacman.x == 20


def test_moves_up_typical():
    pacman = Pacman(100, 30, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    pacman.change_direction(pi/2)
    assert elementmover.up_space(pacman) is True
    assert pacman.y == 30
    elementmover.moves(pacman)
    assert pacman.y == 27


def test_moves_up_collison():
    pacman = Pacman(20, 20, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    pacman.change_direction(pi/2)
    assert elementmover.up_space(pacman) is False
    assert pacman.y == 20
    elementmover.moves(pacman)
    assert pacman.y == 20


def test_moves_down_typical():
    pacman = Pacman(30, 30, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    pacman.change_direction(1.5*pi)
    assert elementmover.down_space(pacman) is True
    assert pacman.y == 30
    elementmover.moves(pacman)
    assert pacman.y == 33


def test_moves_down_collison():
    pacman = Pacman(60, 30, 3, 10)
    board = Board(cells)
    elementmover = ElementMover(board)
    pacman.change_direction(1.5*pi)
    assert elementmover.down_space(pacman) is False
    assert pacman.y == 30
    elementmover.moves(pacman)
    assert pacman.y == 30


def test_ghost_detects_left_wall_true():
    ghost = Ghost(60, 30, 3, 10, "blinky")
    board = Board(cells)
    ghostdetects = GhostDetectingWalls(board)
    assert ghostdetects.left_wall(ghost) is True


def test_ghost_detects_left_wall_false():
    ghost = Ghost(20, 30, 3, 10, "blinky")
    board = Board(cells)
    ghostdetects = GhostDetectingWalls(board)
    assert ghostdetects.left_wall(ghost) is False


def test_ghost_detects_right_wall_true():
    ghost = Ghost(60, 30, 3, 10, "blinky")
    board = Board(cells)
    ghostdetects = GhostDetectingWalls(board)
    assert ghostdetects.right_wall(ghost) is True


def test_ghost_detects_right_wall_false():
    ghost = Ghost(26*9*2, 30, 3, 10, "blinky")
    board = Board(cells)
    ghostdetects = GhostDetectingWalls(board)
    assert ghostdetects.right_wall(ghost) is False


def test_ghost_detects_up_wall_true():
    ghost = Ghost(30, 60, 3, 10, "blinky")
    board = Board(cells)
    ghostdetects = GhostDetectingWalls(board)
    assert ghostdetects.up_wall(ghost) is True


def test_ghost_detects_up_wall_false():
    ghost = Ghost(20, 30, 3, 10, "blinky")
    board = Board(cells)
    ghostdetects = GhostDetectingWalls(board)
    assert ghostdetects.up_wall(ghost) is False


def test_ghost_detects_down_wall_true():
    ghost = Ghost(30, 30, 3, 10, "blinky")
    board = Board(cells)
    ghostdetects = GhostDetectingWalls(board)
    assert ghostdetects.down_wall(ghost) is True


def test_ghost_detects_down_wall_false():
    ghost = Ghost(60, 30, 3, 10, "blinky")
    board = Board(cells)
    ghostdetects = GhostDetectingWalls(board)
    assert ghostdetects.down_wall(ghost) is False


def test_ghost_detects_compute_curent_tile():
    ghost = Ghost(27, 27, 3, 8, "blinky")
    board = Board(cells)
    ghostdetects = GhostDetectingWalls(board)
    assert ghostdetects.compute_current_tile(ghost) == (1, 1)
    ghost.change_direction(pi/2)
    assert ghostdetects.compute_current_tile(ghost) == (1, 1)
    ghost.change_direction(pi)
    assert ghostdetects.compute_current_tile(ghost) == (1, 1)
    ghost.change_direction(pi*1.5)
    assert ghostdetects.compute_current_tile(ghost) == (1, 1)


def test_ghost_detects_distance():
    board = Board(cells)
    ghostdetects = GhostDetectingWalls(board)
    assert ghostdetects.distance(1, 1, 4, 5) == 5


def test_pacman_logic_eats():
    pacman = Pacman(40, 20, 2, 10)
    board = Board(cells)
    pacmanlogic = PacmanLogic(board)
    points = Points()
    x, y = pacmanlogic.my_cell(pacman)
    assert board.is_point(y, x) == 1
    assert points.score == 0
    assert points.points_to_win == 242
    pacmanlogic.eats_points(pacman, points)
    assert board.is_point(y, x) == 0
    assert points.score == 10
    assert points.points_to_win == 241


def test_pacman_logic_eats_super_point():
    pacman = Pacman(30, 70, 2, 10)
    board = Board(cells)
    pacmanlogic = PacmanLogic(board)
    points = Points()
    x, y = pacmanlogic.my_cell(pacman)
    assert board.is_super_point(y, x) is True
    assert points.score == 0
    assert points.super_point_left == 4
    pacmanlogic.eats_super_points(pacman, points)
    assert board.is_super_point(y, x) is False
    assert points.score == 50
    assert points.super_point_left == 3
