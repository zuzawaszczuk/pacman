import pygame
import sys
from assets import colors
from math import pi


class Pacman():
    def __init__(self, screen, x, y, speed, radius):
        self.screen = screen
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = radius
        self.angle = 0
        self.angle_added = 0
        self.mouth_direction = 1

    def draw(self, screen):
        pygame.draw.arc(screen, colors['yellow'], [self.x - self.radius,
                        self.y - self.radius,
                        2 * self.radius, 2 * self.radius],
                        self.angle + self.angle_added,
                        self.angle - self.angle_added, self.radius)

    def animate_mouth(self):
        self.angle_added += 0.03 * pi * self.mouth_direction
        if self.angle_added <= 0 or self.angle_added >= pi*0.3:
            self.mouth_direction *= -1

    def change_direction(self, new_angle):
        self.angle = new_angle


class Board():
    def __init__(self, cells):
        self.cells = cells

    def is_wall(self, x, y):
        if (self.cells[x][y] in [0, 1, 2]):
            return False
        else:
            return True

    def is_point(self, x, y):
        return self.cells[x][y] == 1

    def is_super_point(self, x, y):
        return self.cells[x][y] == 2

    def draw(self, screen):
        c_y = (224 // 31)  # cell height
        c_x = (248 // 28)  # cell width
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
                                    [x + (0.5 * c_x) + 1, y - (0.5 * c_y) + 1,
                                    c_x, c_y], pi, 1.45*pi, 1)
                    pygame.draw.arc(screen, colors['blue'],
                                    [x + 2, y - c_x, 2*c_x, 2*c_y],
                                    pi, 1.45*pi, 1)
                if cell == 4:
                    pygame.draw.arc(screen, colors['blue'],
                                    [x - (0.5 * c_x) + 1, y - (0.5 * c_y) + 1,
                                    0.8*c_x, c_y], 1.55*pi, 0.05*pi, 1)
                    pygame.draw.arc(screen, colors['blue'],
                                    [x - c_x - 2, y - c_y + 1, 2*c_x, 1.9*c_y],
                                    1.55*pi, 1.95*pi, 1)
                if cell == 5:
                    pygame.draw.arc(screen, colors['blue'],
                                    [x - (0.5 * c_x) + 1, y + (0.5 * c_y) + 2,
                                    0.9*c_x, c_y], 1.9*pi, 0.6*pi, 1)
                    pygame.draw.arc(screen, colors['blue'],
                                    [x - c_x - 2, y + (0.4 * c_y),
                                    2*c_x, 2.3*c_y], 0.05*pi, 0.5*pi, 1)
                if cell == 6:
                    pygame.draw.arc(screen, colors['blue'],
                                    [x + (0.5 * c_x) + 1, y + (0.5 * c_y) + 2,
                                    0.8*c_x, c_y], 0.4*pi, 1.05*pi, 1)
                    pygame.draw.arc(screen, colors['blue'],
                                    [x + 2, y + (0.4 * c_y), 2*c_x, 2*c_y],
                                    0.5*pi, pi, 1)
                if cell == 7:
                    pygame.draw.rect(screen, colors['blue'],
                                     (x + (0.5 * c_x) - 1, y - 1, 1, 1))
                    pygame.draw.arc(screen, colors['blue'],
                                    [x + (0.5 * c_x) - 1, y - (0.5 * c_y) + 1,
                                    c_x, c_y], pi, 1.45*pi, 1)
                if cell == 8:
                    pygame.draw.rect(screen, colors['blue'],
                                     (x - 1, y + 2, 2, 1))
                    pygame.draw.arc(screen, colors['blue'],
                                    [x - (0.5 * c_x) + 2, y - (0.5 * c_y) + 1,
                                    0.8*c_x, c_y], 1.55*pi, 0.05*pi, 1)
                if cell == 9:
                    pygame.draw.arc(screen, colors['blue'],
                                    [x + (0.5 * c_x) - 1, y + (0.5 * c_y) - 1,
                                    0.8*c_x, c_y], 0.4*pi, 1.05*pi, 1)
                if cell == 10:
                    pygame.draw.rect(screen, colors['blue'],
                                     (x - 1, y + 2, 1, 1))
                    pygame.draw.arc(screen, colors['blue'],
                                    [x - (0.5 * c_x) + 2, y + (0.5 * c_y) - 1,
                                    0.9*c_x, c_y], 1.9*pi, 0.6*pi, 1)
                if cell == 11:
                    pygame.draw.line(screen, colors['blue'],
                                     (x, y + (0.3 * c_y)),
                                     (x + c_x, y + (0.3 * c_y)), 1)
                    pygame.draw.line(screen, colors['blue'],
                                     (x, y + (0.7 * c_y) + 1),
                                     (x + c_x, y + (0.7 * c_y) + 1), 1)
                if cell == 12:
                    pygame.draw.rect(screen, colors['blue'],
                                     (x - 2, y + (0.3 * c_y), 3, 1))
                    pygame.draw.line(screen, colors['blue'],
                                     (x + 1, y + (0.3 * c_y)),
                                     (x + c_x + 2, y + (0.3 * c_y)), 1)
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
                x += c_x
            y += c_y
        pygame.draw.rect(screen, colors['blue'], (82, 86, 60, 32), width=1)
        pygame.draw.rect(screen, colors['blue'], (85, 89, 54, 26), width=1)


class Game():
    def __init__(self, pacman, board, screen, board_surface, pacman_surface,
                 clock, width, height):
        self.pacman = pacman
        self.board = board
        self.screen = screen
        self.board_surface = board_surface
        self.pacman_surface = pacman_surface
        self.clock = clock
        self.width = width
        self.height = height

    def run(self):
        while True:
            for event in pygame.event.get():
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
            # Cleans surfaces
            self.screen.fill((0, 0, 0))
            self.board_surface.fill((0, 0, 0))
            self.pacman_surface.fill((0, 0, 0, 0))

            self.moves(self.pacman)
            self.pacman.animate_mouth()

            # Draws on surfaces
            self.pacman.draw(self.pacman_surface)
            self.board.draw(self.board_surface)

            # Scales board surface to bigger one
            scaled_board_surface = pygame.transform.scale(
                self.board_surface, (self.width, self.height))
            # Puts surfaces on screen
            self.screen.blit(scaled_board_surface, (0, 0))
            self.screen.blit(self.pacman_surface, (0, 0))

            pygame.display.flip()
            self.clock.tick(30)

    def moves(self, pacman):
        if pacman.angle == pi:
            pacman.x -= pacman.speed
        elif pacman.angle == 0:
            pacman.x += pacman.speed
        elif pacman.angle == pi/2:
            pacman.y -= pacman.speed
        elif pacman.angle == 1.5*pi:
            pacman.y += pacman.speed
