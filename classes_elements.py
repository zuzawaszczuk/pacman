import pygame
from math import pi
from typing import List, Tuple, Dict, Union
from pygame.surface import Surface
TColor = Tuple[int, int, int]


class Character():
    def __init__(self, x: float, y: float, speed: float, radius: int) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius
        self._angle = 0.0

    def change_direction(self, new_angle: float) -> None:
        self._angle = new_angle

    @property
    def angle(self) -> float:
        return self._angle


class Pacman(Character):
    def __init__(self, x: float, y: float, speed: float,
                 radius: int, lives: int = 3) -> None:
        super().__init__(x, y, speed, radius)
        self.lives = lives

        self.angle_added = 0.0
        self.mouth_direction = 1

    def animate_mouth(self) -> None:
        self.angle_added += 0.03 * pi * self.mouth_direction
        if self.angle_added <= 0 or self.angle_added >= pi*0.3:
            self.mouth_direction *= -1

    def go_home(self) -> None:
        self.x = 28*9
        self.y = 315
        self.change_direction(0)
        self.animate_mouth()

    def draw(self, screen: Surface, colors: Dict[str, TColor]) -> None:
        pygame.draw.arc(screen, colors['yellow'],
                        [self.x - self.radius,
                        self.y - self.radius,
                        2 * self.radius, 2 * self.radius],
                        self.angle + self.angle_added,
                        self.angle - self.angle_added, self.radius)


class Ghost(Character):
    def __init__(self, x: float, y: float, speed: float, radius: int,
                 name: str, is_dead: bool = False, is_frightened: bool = False,
                 at_home: bool = True, going_out: bool = False,
                 next_tile: Union[Tuple[int, int], None] = None) -> None:
        super().__init__(x, y, speed, radius)
        self.name = name
        self._is_dead = is_dead
        self._is_frightened = is_frightened
        self._at_home = at_home
        self._going_out = going_out
        if next_tile is None:
            self._next_tile = (int(x // 18), int(y // 18))
        else:
            self._next_tile = next_tile

    def set_cord(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    @property
    def is_dead(self) -> bool:
        return self._is_dead

    def dead(self) -> None:
        self._is_dead = True

    def is_alive(self) -> None:
        self._is_dead = False

    @property
    def is_frightened(self) -> bool:
        return self._is_frightened

    def frightened(self) -> None:
        self._is_frightened = True

    def not_frightened(self) -> None:
        self._is_frightened = False

    @property
    def at_home(self) -> bool:
        return self._at_home

    def out_of_home(self) -> None:
        self._at_home = False

    def back_at_home(self) -> None:
        self._at_home = True

    @property
    def going_out(self) -> bool:
        return self._going_out

    def start_going_out(self) -> None:
        self._going_out = True

    def end_going_out(self) -> None:
        self._going_out = False

    @property
    def next_tile(self) -> Tuple[int, int]:
        return self._next_tile

    def reset_next_tile(self) -> None:
        self._next_tile = (int(self.x // 18), int(self.y // 18))

    def set_next_tile(self, x: int, y: int) -> None:
        self._next_tile = (x, y)

    def left(self) -> None:
        self.change_direction(pi)
        x, y = self.next_tile
        self.set_next_tile(x-1, y)

    def right(self) -> None:
        self.change_direction(0)
        x, y = self.next_tile
        self.set_next_tile(x+1, y)

    def up(self) -> None:
        self.change_direction(pi/2)
        x, y = self.next_tile
        self.set_next_tile(x, y-1)

    def down(self) -> None:
        self.change_direction(1.5*pi)
        x, y = self.next_tile
        self.set_next_tile(x, y+1)


class Board():
    def __init__(self, cells: List[List[int]]) -> None:
        self._cells = cells

    @property
    def cells(self) -> List[List[int]]:
        return self._cells

    def is_wall(self, x: int, y: int) -> bool:
        return not (self.cells[x][y] in [0, 1, 2])

    def is_point(self, x: int, y: int) -> bool:
        return self.cells[x][y] == 1

    def is_super_point(self, x: int, y: int) -> bool:
        return self.cells[x][y] == 2

    def is_door(self, x: int, y: int) -> bool:
        return self.cells[x][y] == 16

    def set_cell(self, x: int, y: int, value: int) -> None:
        self._cells[x][y] = value

    def draw(self, screen: Surface, colors: dict[str, TColor],
             door: bool) -> None:
        c_x = 9  # cell width
        c_y = 9  # cell height
        x = 0
        y = 0
        for row in self.cells:
            x = 0
            for cell in row:
                if cell == 1:
                    pygame.draw.circle(screen, colors['pink'],
                                       (x + (0.5 * c_x), y + (0.5 * c_y)), 1)
                if cell == 2:
                    pygame.draw.circle(screen, colors['pink'],
                                       (x + (0.5 * c_x), y + (0.5 * c_y)), 3)
                if cell == 3:
                    pygame.draw.arc(screen, colors['blue'],
                                    [x + (0.5 * c_x) + 2, y - (0.5 * c_y) - 2,
                                    c_x, 1.2*c_y], pi, 1.45*pi, 1)
                    pygame.draw.arc(screen, colors['blue'],
                                    [x + 2, y - c_y - 2, 2*c_x, 2.1*c_y],
                                    0.95*pi, 1.45*pi, 1)
                if cell == 4:
                    pygame.draw.arc(screen, colors['blue'],
                                    [x - (0.5 * c_x), y - (0.5 * c_y) - 1,
                                    c_x, c_y], 1.5*pi, 1.95*pi, 1)
                    pygame.draw.arc(screen, colors['blue'],
                                    [x - c_x - 2, y - c_y, 2*c_x, 1.9*c_y],
                                    1.55*pi, 1.95*pi, 1)
                if cell == 5:
                    pygame.draw.arc(screen, colors['blue'],
                                    [x - (0.5 * c_x), y + (0.5 * c_y) + 2,
                                    c_x, c_y], 1.9*pi, 0.6*pi, 1)
                    pygame.draw.arc(screen, colors['blue'],
                                    [x - c_x - 4, y + (0.4 * c_y) - 2,
                                    2.3*c_x, 2.3*c_y], 0.05*pi, 0.35*pi, 1)
                if cell == 6:
                    pygame.draw.arc(screen, colors['blue'],
                                    [x + (0.5 * c_x) + 2, y + (0.5 * c_y) + 2,
                                    c_x, c_y], 0.5*pi, pi, 1)
                    pygame.draw.arc(screen, colors['blue'],
                                    [x + 2, y + 2, 2*c_x, 2.2*c_y],
                                    0.5*pi, 0.95*pi, 1)
                if cell == 7:
                    pygame.draw.arc(screen, colors['blue'],
                                    [x + (0.5 * c_x) - 1, y - (0.5 * c_y) - 1,
                                    c_x, 1.2*c_y], pi, 1.45*pi, 1)
                if cell == 8:
                    pygame.draw.rect(screen, colors['blue'],
                                     (x - 2, y + 3, 2, 1))
                    pygame.draw.arc(screen, colors['blue'],
                                    [x - (0.5 * c_x) + 1, y - (0.5 * c_y),
                                    c_x, c_y], 1.5*pi, 1.95*pi, 1)
                if cell == 9:
                    pygame.draw.arc(screen, colors['blue'],
                                    [x + (0.5 * c_x) - 1, y + (0.5 * c_y) - 1,
                                    c_x, c_y], 0.5*pi, pi, 1)
                if cell == 10:
                    pygame.draw.arc(screen, colors['blue'],
                                    [x - (0.5 * c_x) + 1, y + (0.5 * c_y) - 1,
                                    c_x, c_y], 1.9*pi, 0.6*pi, 1)
                if cell == 11:
                    pygame.draw.line(screen, colors['blue'],
                                     (x, y + (0.3 * c_y)),
                                     (x + c_x, y + (0.3 * c_y)), 1)
                    pygame.draw.line(screen, colors['blue'],
                                     (x, y + (0.7 * c_y)),
                                     (x + c_x, y + (0.7 * c_y)), 1)
                if cell == 12:
                    pygame.draw.line(screen, colors['blue'],
                                     (x - 2, y + (0.4 * c_y)),
                                     (x + c_x - 2, y + (0.4 * c_y)), 1)
                if cell == 13:
                    pygame.draw.line(screen, colors['blue'],
                                     (x + (0.3 * c_x), y),
                                     (x + (0.3 * c_x), y + c_y), 1)
                    pygame.draw.line(screen, colors['blue'],
                                     (x + (0.7 * c_x), y),
                                     (x + (0.7 * c_x), y + c_y), 1)
                if cell == 14:
                    pygame.draw.line(screen, colors['blue'],
                                     (x + (0.5 * c_x) - 1, y - 1),
                                     (x + (0.5 * c_x) - 1, y + c_y - 1), 1)
                if cell == 16 and not door:
                    pygame.draw.line(screen, colors['pink'],
                                     (x, y + 3),
                                     (x + c_x, y + 3), 4)
                x += c_x
            y += c_y
        pygame.draw.rect(screen, colors['blue'], (93, 110, 65, 40), width=1)
        pygame.draw.rect(screen, colors['blue'], (97, 114, 57, 32), width=1)
        if door:
            pygame.draw.line(screen, colors['black'], (120, 111),
                             (140, 111), width=6)
            pygame.draw.line(screen, colors['pink'], (120, 115),
                             (120, 97), width=3)
            pygame.draw.line(screen, colors['blue'], (140, 114),
                             (140, 110), width=1)


class Points():
    def __init__(self, score: int = 0, points_to_win: int = 242,
                 super_point_left: int = 4, high_score: int = 0) -> None:
        self._score = score
        self._points_to_win = points_to_win
        self._super_point_left = super_point_left
        self._high_score = high_score

    @property
    def score(self) -> int:
        return self._score

    def add_to_score(self, value: int) -> None:
        if value < 0:
            raise ValueError("Value must be positive!")
        self._score += value

    @property
    def points_to_win(self) -> int:
        return self._points_to_win

    def one_point_eaten(self) -> None:
        self._points_to_win -= 1

    @property
    def super_point_left(self) -> int:
        return self._super_point_left

    def super_point_eaten(self) -> None:
        self._super_point_left -= 1

    @property
    def high_score(self) -> int:
        self._high_score = max(self._high_score, self.score)
        return self._high_score
