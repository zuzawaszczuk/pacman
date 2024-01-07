import pygame
from math import pi
import math
import random
from typing import List, Tuple
from classes_elements import Pacman, Board, Ghost, Points, Character


class CellLogic():
    def __init__(self, board: Board) -> None:
        self.board = board

    def left_cell(self, player: Character) -> Tuple[int, int]:
        x = int((player.x - 2 * player.radius)//18)
        y = int(player.y//18)
        return (x, y)

    def right_cell(self, player: Character) -> Tuple[int, int]:
        x = int((player.x + 2 * player.radius)//18)
        y = int(player.y//18)
        return (x, y)

    def down_cell(self, player: Character) -> Tuple[int, int]:
        x = int(player.x//18)
        y = int((player.y + 2 * player.radius)//18)
        return (x, y)

    def up_cell(self, player: Character) -> Tuple[int, int]:
        x = int(player.x//18)
        y = int((player.y - 2 * player.radius)//18)
        return (x, y)

    def my_cell(self, player: Character) -> Tuple[int, int]:
        x = int(player.x//18)
        y = int(player.y//18)
        return (x, y)


class ElementMover(CellLogic):
    def moves(self, player: Character) -> None:
        if player.angle == pi and self.left_space(player):
            player.x -= player.speed
        elif player.angle == 0 and self.right_space(player):
            player.x += player.speed
        elif player.angle == pi/2 and self.up_space(player):
            player.y -= player.speed
        elif player.angle == 1.5*pi and self.down_space(player):
            player.y += player.speed

    def right_space(self, player: Character) -> bool:
        x, y = self.right_cell(player)
        player.x += player.speed
        border_line = pygame.Rect(player.x + player.radius - 4,
                                  player.y - 7, 3, 14)
        if x > 27 and y == 14:
            player.x = 0
            return True
        elif self.board.is_wall(y, x):
            wall = pygame.Rect(x*18 + 3, y*18, 18, 18)
            player.x -= player.speed
            return wall.colliderect(border_line) == 0
        else:
            player.x -= player.speed
            return True

    def left_space(self, player: Character) -> bool:
        x, y = self.left_cell(player)
        player.x -= player.speed
        border_line = pygame.Rect(player.x - player.radius + 4,
                                  player.y - 7, 3, 14)
        if x < 0 and y == 14:
            player.x = 27 * 18
            return True
        elif self.board.is_wall(y, x):
            wall = pygame.Rect(x*18 - 1, y*18, 18, 18)
            player.x += player.speed
            return wall.colliderect(border_line) == 0
        else:
            player.x += player.speed
            return True

    def up_space(self, player: Character) -> bool:
        x, y = self.up_cell(player)
        player.y -= player.speed
        border_line = pygame.Rect(player.x - 7,
                                  player.y - player.radius, 14, 3)
        if self.board.is_wall(y, x):
            wall = pygame.Rect(x*18, y*18 - 5, 18, 18)
            player.y += player.speed
            return wall.colliderect(border_line) == 0
        else:
            player.y += player.speed
            return True

    def down_space(self, player: Character) -> bool:
        x, y = self.down_cell(player)
        player.y += player.speed
        border_line = pygame.Rect(player.x - 7,
                                  player.y + player.radius, 14, 3)
        if self.board.is_wall(y, x):
            wall = pygame.Rect(x*18, y*18 + 5, 18, 18)
            player.y -= player.speed
            return wall.colliderect(border_line) == 0
        else:
            player.y -= player.speed
            return True


class GhostDetectingWalls(CellLogic):
    def left_wall(self, player: Ghost) -> bool:
        x, y = self.left_cell(player)
        return not self.board.is_wall(y, x)

    def right_wall(self, player: Ghost) -> bool:
        x, y = self.right_cell(player)
        return not self.board.is_wall(y, x)

    def down_wall(self, player: Ghost) -> bool:
        x, y = self.down_cell(player)
        return not self.board.is_wall(y, x)

    def up_wall(self, player: Ghost) -> bool:
        x, y = self.up_cell(player)
        return not self.board.is_wall(y, x)

    def compute_current_tile(self, ghost: Ghost) -> Tuple[int, int]:
        if ghost.angle == pi:
            ghost.x += ghost.radius
            x, y = self.my_cell(ghost)
            ghost.x -= ghost.radius
        elif ghost.angle == 0:
            ghost.x -= ghost.radius
            x, y = self.my_cell(ghost)
            ghost.x += ghost.radius
        elif ghost.angle == pi/2:
            ghost.y += ghost.radius
            x, y = self.my_cell(ghost)
            ghost.y -= ghost.radius
        elif ghost.angle == 1.5*pi:
            ghost.y -= ghost.radius
            x, y = self.my_cell(ghost)
            ghost.y += ghost.radius
        return (x, y)

    def distance(self, ax: float, ay: float, bx: float, by: float) -> float:
        return math.sqrt((bx - ax) ** 2 + (by - ay) ** 2)

    def collision(self, player1: Character, player2: Character) -> bool:
        return ((self.compute_current_tile(player1) ==
                self.compute_current_tile(player2)) or
                (self.my_cell(player1) ==
                self.my_cell(player2)))


class PacmanLogic(CellLogic):
    def eats_points(self, pacman: Pacman, points: Points) -> bool:
        x, y = self.my_cell(pacman)
        if self.board.is_point(y, x):
            self.board.set_cell(y, x, 0)
            points.add_to_score(10)
            points.one_point_eaten()
            return True
        return False

    def eats_super_points(self, pacman: Pacman, points: Points) -> bool:
        x, y = self.my_cell(pacman)
        if self.board.is_super_point(y, x):
            self.board.set_cell(y, x, 0)
            points.add_to_score(50)
            points.super_point_eaten()
            return True
        return False


class NormalGhostAction():
    def __init__(self, ghosts: List[Ghost], ghostlogic: GhostDetectingWalls,
                 pacman: Pacman, dot_counter: int) -> None:
        self.ghosts = ghosts
        self.ghostlogic = ghostlogic
        self.pacman = pacman
        self.dot_counter = dot_counter

        self.blinky = ghosts[0]
        self.inky = ghosts[1]
        self.pinky = ghosts[2]
        self.clyde = ghosts[3]
        self.one = True
        self.two = True
        self.three = True
        self.is_frightened = False
        self.frightened_timer = 0.0

    def run(self, timer) -> None:
        self.activate_ghost_to_go_out()
        if timer < 7:
            self.scatter()
        elif int(timer) == 7 and self.one is True:
            for ghost in self.ghosts:
                self.reverse_direction(ghost)
            self.one = False
        elif timer < 27:
            self.chase()
        elif timer < 34:
            self.scatter()
        elif int(timer) == 34 and self.two:
            for ghost in self.ghosts:
                self.reverse_direction(ghost)
            self.two = False
        elif timer < 54:
            self.chase()
        elif timer < 59:
            self.scatter()
        elif int(timer) == 59 and self.three:
            for ghost in self.ghosts:
                self.reverse_direction(ghost)
            self.three = False
        elif timer < 79:
            self.chase()
        elif timer < 85:
            self.scatter()
        else:
            self.chase()

    def activate_ghost_to_go_out(self):
        if self.blinky.at_home and not self.blinky.is_dead:
            self.blinky.set_next_tile(14, 11)
            self.blinky.right()
            self.blinky.out_of_home()

        if (self.pinky.at_home or self.pinky.going_out) \
                and not self.pinky.is_dead:
            self.go_out(self.pinky)

        if (self.inky.at_home or self.inky.going_out) \
                and self.dot_counter > 17 \
                and not self.inky.is_dead:
            self.go_out(self.inky)

        if (self.clyde.at_home or self.clyde.going_out) \
                and self.dot_counter > 32 \
                and not self.clyde.is_dead:
            self.go_out(self.clyde)

    def go_home(self) -> None:
        self.blinky.set_cord(28*9, 205)
        self.inky.set_cord(28*9 - 30, 260)
        self.pinky.set_cord(28*9, 260)
        self.clyde.set_cord(28*9 + 30, 260)
        for ghost in self.ghosts:
            ghost.speed = 2.3
            ghost.end_going_out()
            ghost.back_at_home()
            ghost.is_alive()
            ghost.not_frightened()
            ghost.reset_next_tile()

    def go_out(self, ghost: Ghost) -> None:
        x, y = self.ghostlogic.compute_current_tile(ghost)
        if x != 14 and ghost.at_home:
            if ghost.going_out is False:
                ghost.set_next_tile(x, y)
            ghost.start_going_out()
            self.go_to_tile(ghost, 14, 14, self.ghostlogic)
        elif y > 11:
            if ghost.going_out is False:
                ghost.set_next_tile(x, y)
            ghost.start_going_out()
            if ghost.at_home:
                ghost.up()
                ghost.out_of_home()
            ghost.y -= ghost.speed
        elif ghost.going_out:
            ghost.set_next_tile(14, 11)
            ghost.right()
            ghost.end_going_out()

    def reverse_direction(self, ghost: Ghost) -> None:
        if ghost.is_dead:
            return 0
        change = {
            0: pi,
            pi/2: 1.5*pi,
            pi: 0,
            1.5*pi: pi/2
        }
        x, y = self.ghostlogic.compute_current_tile(ghost)
        ghost.set_next_tile(x, y)
        ghost.change_direction(change[ghost.angle])

    def go_to_tile(self, ghost: Ghost, tile_x: int, tile_y: int,
                   ghostlogic: GhostDetectingWalls):
        if ghost.next_tile != ghostlogic.compute_current_tile(ghost):
            return 0
        x, y = ghostlogic.compute_current_tile(ghost)
        # up > left > down
        left_dist = self.ghostlogic.distance(x-1, y, tile_x, tile_y)
        right_dist = self.ghostlogic.distance(x+1, y, tile_x, tile_y)
        up_dist = self.ghostlogic.distance(x, y-1, tile_x, tile_y)
        down_dist = self.ghostlogic.distance(x, y+1, tile_x, tile_y)
        if ghost.angle == pi:
            self.tile_left(ghostlogic, ghost, left_dist, up_dist, down_dist)
        elif ghost.angle == 0:
            self.tile_right(ghostlogic, ghost, right_dist, up_dist, down_dist)
        elif ghost.angle == pi/2:
            self.tile_up(ghostlogic, ghost, left_dist, up_dist, right_dist)
        elif ghost.angle == 1.5*pi:
            self.tile_down(ghostlogic, ghost, left_dist, right_dist, down_dist)

    def normal(self, ghost: Ghost) -> bool:
        return not (ghost.at_home or ghost.going_out
                    or ghost.is_dead)

    def scatter(self) -> None:
        if self.normal(self.blinky):
            self.go_to_tile(self.blinky, 27, 0, self.ghostlogic)
        if self.normal(self.pinky):
            self.go_to_tile(self.pinky, 2, 0, self.ghostlogic)
        if self.normal(self.inky):
            self.go_to_tile(self.inky, 27, 31, self.ghostlogic)
        if self.normal(self.clyde):
            self.go_to_tile(self.clyde, 2, 31, self.ghostlogic)

    def chase(self) -> None:
        if self.normal(self.blinky):
            self.chase_blinky()
        if self.normal(self.pinky):
            self.chase_pinky()
        if self.normal(self.inky):
            self.chase_inky()
        if self.normal(self.clyde):
            self.chase_clyde()

    def chase_blinky(self) -> None:
        x, y = self.ghostlogic.my_cell(self.pacman)
        # Blinky targets pacman positions
        self.go_to_tile(self.blinky, x, y, self.ghostlogic)

    def chase_pinky(self) -> None:
        x, y = self.ghostlogic.my_cell(self.pacman)
        # Pinky targets a tile 4 cells before pacman actual direction
        if self.pacman.angle == pi:
            self.go_to_tile(self.pinky, x - 4, y, self.ghostlogic)
        elif self.pacman.angle == 0:
            self.go_to_tile(self.pinky, x + 4, y, self.ghostlogic)
        elif self.pacman.angle == pi/2:
            self.go_to_tile(self.pinky, x, y - 4, self.ghostlogic)
        elif self.pacman.angle == 1.5*pi:
            self.go_to_tile(self.pinky, x, y + 4, self.ghostlogic)

    def chase_inky(self) -> None:
        x, y = self.ghostlogic.my_cell(self.pacman)
        # Inky is more complicated, their goal is to be two times futher
        # than distance from blinky to tile 2 cells before pacman
        blinky_x, blinky_y = self.ghostlogic.my_cell(self.blinky)
        if self.pacman.angle == pi:
            self.go_to_tile(self.inky, 2*(x-2) - blinky_x, 2*y - blinky_y,
                            self.ghostlogic)
        elif self.pacman.angle == 0:
            self.go_to_tile(self.inky, 2*(x+2) - blinky_x, 2*y - blinky_y,
                            self.ghostlogic)
        elif self.pacman.angle == pi/2:
            self.go_to_tile(self.inky, 2*x - blinky_x, 2*(y-2) - blinky_y,
                            self.ghostlogic)
        elif self.pacman.angle == 1.5*pi:
            self.go_to_tile(self.inky, 2*x - blinky_x, 2*(y+2) - blinky_y,
                            self.ghostlogic)

    def chase_clyde(self) -> None:
        x, y = self.ghostlogic.my_cell(self.pacman)
        blinky_x, blinky_y = self.ghostlogic.my_cell(self.blinky)
        # Clyde has two targets, if he is far from pacman he behaves
        # like Blinky, but when he is closer than 8 cells he goes to his
        # "corner"
        if self.ghostlogic.distance(x, y, blinky_x, blinky_y) > 8:
            self.go_to_tile(self.clyde, x, y, self.ghostlogic)
        else:
            self.go_to_tile(self.clyde, 2, 31, self.ghostlogic)

    def tile_left(self, ghostlogic: GhostDetectingWalls, ghost: Ghost,
                  left_dist: float,
                  up_dist: float, down_dist: float) -> None:
        min_dist = min(left_dist, up_dist, down_dist)
        if (ghostlogic.up_wall(ghost) or ghostlogic.down_wall(ghost)) is False:
            # Case 1 only one step is possible so we do it
            ghost.left()
        elif ghostlogic.left_wall(ghost):
            if ghostlogic.up_wall(ghost) and ghostlogic.down_wall(ghost):
                # LEFT or DOWN or UP
                if up_dist == min_dist:
                    ghost.up()
                elif left_dist == min_dist:
                    ghost.left()
                elif down_dist == min_dist:
                    ghost.down()
            elif ghostlogic.up_wall(ghost):
                # UP or LEFT
                if up_dist < left_dist:
                    ghost.up()
                else:
                    ghost.left()
            elif ghostlogic.down_wall(ghost):
                # DOWN OR LEfT
                if left_dist < down_dist:
                    ghost.left()
                else:
                    ghost.down()
        else:
            if ghostlogic.up_wall(ghost) and ghostlogic.down_wall(ghost):
                # UP or DOWN
                if up_dist < down_dist:
                    ghost.up()
                else:
                    ghost.down()
            elif ghostlogic.up_wall(ghost):
                # UP
                ghost.up()
            elif ghostlogic.down_wall(ghost):
                # DOWN
                ghost.down()

    def tile_right(self, ghostlogic: GhostDetectingWalls, ghost: Ghost,
                   right_dist: float, up_dist: float,
                   down_dist: float) -> None:
        min_dist = min(right_dist, up_dist, down_dist)
        if (ghostlogic.up_wall(ghost) or ghostlogic.down_wall(ghost)) is False:
            # RIGHT
            ghost.right()
        elif ghostlogic.right_wall(ghost):
            if ghostlogic.up_wall(ghost) and ghostlogic.down_wall(ghost):
                # RIGHT or DOWN or UP
                if up_dist == min_dist:
                    ghost.up()
                elif down_dist == min_dist:
                    ghost.down()
                else:
                    ghost.right()
            elif ghostlogic.up_wall(ghost):
                # UP or RIGHT
                if up_dist < right_dist:
                    ghost.up()
                else:
                    ghost.right()
            elif ghostlogic.down_wall(ghost):
                # DOWN OR RIGHT
                if down_dist < right_dist:
                    ghost.down()
                else:
                    ghost.right()
        else:
            if ghostlogic.up_wall(ghost) and ghostlogic.down_wall(ghost):
                # UP or DOWN
                if up_dist < down_dist:
                    ghost.up()
                else:
                    ghost.down()
            elif ghostlogic.up_wall(ghost):
                # UP
                ghost.up()
            elif ghostlogic.down_wall(ghost):
                # DOWN
                ghost.down()

    def tile_up(self, ghostlogic: GhostDetectingWalls, ghost: Ghost,
                left_dist: float, up_dist: float, right_dist: float) -> None:
        min_dist = min(left_dist, up_dist, right_dist)
        if (ghostlogic.left_wall(ghost) or ghostlogic.right_wall(ghost)) \
                is False:
            # UP
            ghost.up()
        elif ghostlogic.up_wall(ghost):
            if ghostlogic.right_wall(ghost) and ghostlogic.left_wall(ghost):
                # LEFT or RIGHT or UP
                if up_dist == min_dist:
                    ghost.up()
                elif left_dist == min_dist:
                    ghost.down()
                elif right_dist == min_dist:
                    ghost.right()
            elif ghostlogic.left_wall(ghost):
                # UP or LEFT
                if up_dist < left_dist:
                    ghost.up()
                else:
                    ghost.left()
            elif ghostlogic.right_wall(ghost):
                # UP OR RIGHT
                if up_dist < right_dist:
                    ghost.up()
                else:
                    ghost.right()
        else:
            if ghostlogic.left_wall(ghost) and ghostlogic.right_wall(ghost):
                # LEFT or RIGHT
                if left_dist < right_dist:
                    ghost.left()
                else:
                    ghost.right()
            elif ghostlogic.left_wall(ghost):
                # LEFT
                ghost.left()
            elif ghostlogic.right_wall(ghost):
                # RIGHT
                ghost.right()

    def tile_down(self, ghostlogic: GhostDetectingWalls, ghost: Ghost,
                  left_dist: float, right_dist: float,
                  down_dist: float) -> None:
        min_dist = min(left_dist, down_dist, right_dist)
        if (ghostlogic.right_wall(ghost) or ghostlogic.left_wall(ghost))\
                is False:
            # DOWN
            ghost.down()
        elif ghostlogic.down_wall(ghost):
            if ghostlogic.right_wall(ghost) and ghostlogic.left_wall(ghost):
                # LEFT or RIGHT or DOWN
                if left_dist == min_dist:
                    ghost.left()
                elif down_dist == min_dist:
                    ghost.down()
                elif right_dist == min_dist:
                    ghost.right()
            elif ghostlogic.left_wall(ghost):
                # DOWN or LEFT
                if left_dist < down_dist:
                    ghost.left()
                else:
                    ghost.down()
            elif ghostlogic.right_wall(ghost):
                # DOWN OR RIGHT
                if down_dist < right_dist:
                    ghost.down()
                else:
                    ghost.right()
        else:
            if ghostlogic.left_wall(ghost) and ghostlogic.right_wall(ghost):
                # LEFT or RIGHT
                if left_dist < right_dist:
                    ghost.left()
                else:
                    ghost.right()
            elif ghostlogic.left_wall(ghost):
                # LEFT
                ghost.left()
            else:
                # RIGHT
                ghost.right()

    def correct_next_tile(self, ghostlogic: GhostDetectingWalls,
                          ghost: Ghost) -> None:
        x, y = ghostlogic.compute_current_tile(ghost)
        next_x, next_y = ghost.next_tile
        if ghost.angle == pi and (x - next_x > 1 or x - next_x > 0):
            ghost.set_next_tile(x-1, y)
        elif ghost.angle == 0 and (next_x - x > 1 or next_x - x > 0):
            ghost.set_next_tile(x+1, y)
        elif ghost.angle == pi/2 and (y - next_y > 1 or y - next_y > 0):
            ghost.set_next_tile(x, y-1)
        elif ghost.angle == 1.5*pi and (next_y - y > 1 or next_y - y > 0):
            ghost.set_next_tile(x, y+1)


class FrightenedGhostAction():
    def __init__(self, ghosts: List[Ghost], ghostlogic: GhostDetectingWalls,
                 pacman: Pacman) -> None:
        self.ghosts = ghosts
        self.ghostlogic = ghostlogic
        self.pacman = pacman

    def run(self) -> None:
        for ghost in self.ghosts:
            if not ghost.is_frightened and not ghost.is_dead:
                ghost.reset_next_tile()
                ghost.speed = 1.5
                ghost.frightened()
            if not ghost.is_dead:
                self.random_moves(ghost)

    def random_moves(self, ghost: Ghost) -> None:
        if ghost.next_tile != self.ghostlogic.compute_current_tile(ghost):
            return 0
        possible_moves = self.compute_possible_moves(ghost)
        reverse = {
            0: pi,
            pi/2: 1.5*pi,
            pi: 0,
            1.5*pi: pi/2
        }
        if reverse[ghost.angle] in possible_moves:
            possible_moves.remove(reverse[ghost.angle])
        if len(possible_moves) == 0:
            return 0
        move = random.choice(possible_moves)
        if move == pi:
            ghost.left()
        elif move == 0:
            ghost.right()
        elif move == pi/2:
            ghost.up()
        elif move == 1.5*pi:
            ghost.down()

    def compute_possible_moves(self, ghost: Ghost) -> List[float]:
        possible_moves = []
        if self.ghostlogic.left_wall(ghost):
            possible_moves.append(pi)
        if self.ghostlogic.right_wall(ghost):
            possible_moves.append(0)
        if self.ghostlogic.down_wall(ghost):
            possible_moves.append(1.5*pi)
        if self.ghostlogic.up_wall(ghost):
            possible_moves.append(pi/2)
        return possible_moves

    def back_to_normal(self) -> None:
        for ghost in self.ghosts:
            if not ghost.is_dead:
                ghost.reset_next_tile()
                ghost.speed = 2.3
                ghost.not_frightened()


class DeadGhostAction(NormalGhostAction):
    def __init__(self, ghosts: List[Ghost],
                 ghostlogic: GhostDetectingWalls) -> None:
        self.ghosts = ghosts
        self.ghostlogic = ghostlogic

    def dead_ghosts_go_back(self):
        for ghost in self.ghosts:
            if ghost.is_dead:
                ghost.speed = 4
                self.dead_go_home(ghost)

    def dead_go_home(self, ghost) -> None:
        x, y = self.ghostlogic.compute_current_tile(ghost)
        if not ghost.going_out:
            self.go_to_tile(ghost, 14, 11, self.ghostlogic)
            if (14, 11) == (x, y):
                ghost.start_going_out()
                ghost.change_direction(1.5*pi)
        elif y < 14 and ghost.name != "blinky":
            ghost.y += ghost.speed
        else:
            ghost.speed = 2.3
            ghost.back_at_home()
            ghost.end_going_out()
            ghost.is_alive()
