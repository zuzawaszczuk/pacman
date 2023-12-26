import pygame
from math import pi

# flake8: noqa
cells = [
[6, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 5],
[13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 14, 14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 13],
[13, 1, 9, 12, 12, 10, 1, 9, 12, 12, 12, 10, 1, 14, 14, 1, 9, 12, 12, 12, 10, 1, 9, 12, 12, 10, 1, 13],
[13, 2, 14, 0, 0, 14, 1, 14, 0, 0, 0, 14, 1, 14, 14, 1, 14, 0, 0, 0, 14, 1, 14, 0, 0, 14, 2, 13],
[13, 1, 7, 12, 12, 8, 1, 7, 12, 12, 12, 8, 1, 7, 8, 1, 7, 12, 12, 12, 8, 1, 7, 12, 12, 8, 1, 13],
[13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 13],
[13, 1, 9, 12, 12, 10, 1, 9, 10, 1, 9, 12, 12, 12, 12, 12, 12, 10, 1, 9, 10, 1, 9, 12, 12, 10, 1, 13],
[13, 1, 7, 12, 12, 8, 1, 14, 14, 1, 7, 12, 12, 10, 9, 12, 12, 8, 1, 14, 14, 1, 7, 12, 12, 8, 1, 13],
[13, 1, 1, 1, 1, 1, 1, 14, 14, 1, 1, 1, 1, 14, 14, 1, 1, 1, 1, 14, 14, 1, 1, 1, 1, 1, 1, 13],
[3, 11, 11, 11, 11, 5, 1, 14, 7, 12, 12, 10, 0, 14, 14, 0, 9, 12, 12, 8, 14, 1, 6, 11, 11, 11, 11, 4],
[0, 0, 0, 0, 0, 13, 1, 14, 9, 12, 12, 8, 0, 7, 8, 0, 7, 12, 12, 10, 14, 1, 13, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 13, 1, 14, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 14, 1, 13, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 13, 1, 14, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 14, 1, 13, 0, 0, 0, 0, 0],
[11, 11, 11, 11, 11, 4, 1, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 8, 1, 3, 11, 11, 11, 11, 11],
[0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
[11, 11, 11, 11, 11, 5, 1, 9, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 10, 1, 6, 11, 11, 11, 11, 11],
[0, 0, 0, 0, 0, 13, 1, 14, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 14, 1, 13, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 13, 1, 14, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 14, 1, 13, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 13, 1, 14, 14, 0, 9, 12, 12, 12, 12, 12, 12, 10, 0, 14, 14, 1, 13, 0, 0, 0, 0, 0],
[6, 11, 11, 11, 11, 4, 1, 7, 8, 0, 7, 12, 12, 10, 9, 12, 12, 8, 0, 7, 8, 1, 3, 11, 11, 11, 11, 5],
[13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 14, 14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 13],
[13, 1, 9, 12, 12, 10, 1, 9, 12, 12, 12, 10, 1, 14, 14, 1, 9, 12, 12, 12, 10, 1, 9, 12, 12, 10, 1, 13],
[13, 1, 7, 12, 10, 14, 1, 7, 12, 12, 12, 8, 1, 7, 8, 1, 7, 12, 12, 12, 8, 1, 14, 9, 12, 8, 1, 13],
[13, 2, 1, 1, 14, 14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 14, 14, 1, 1, 2, 13],
[13, 12, 10, 1, 14, 14, 1, 9, 10, 1, 9, 12, 12, 12, 12, 12, 12, 10, 1, 9, 10, 1, 14, 14, 1, 9, 12, 13],
[13, 12, 8, 1, 7, 8, 1, 14, 14, 1, 7, 12, 12, 10, 9, 12, 12, 8, 1, 14, 14, 1, 7, 8, 1, 7, 12, 13],
[13, 1, 1, 1, 1, 1, 1, 14, 14, 1, 1, 1, 1, 14, 14, 1, 1, 1, 1, 14, 14, 1, 1, 1, 1, 1, 1, 13],
[13, 1, 9, 12, 12, 12, 12, 8, 7, 12, 12, 10, 1, 14, 14, 1, 9, 12, 12, 8, 7, 12, 12, 12, 12, 10, 1, 13],
[13, 1, 7, 12, 12, 12, 12, 12, 12, 12, 12, 8, 1, 7, 8, 1, 7, 12, 12, 12, 12, 12, 12, 12, 12, 8, 1, 13],
[13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 13],
[3, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 4]
]

colors = {
    'blue': (33, 33, 222),
    'pink': (222, 161, 133),
    'yellow': (255, 255, 0)
}


def draw_board(screen):
    c_y = (224 // 31)  # cell height
    c_x = (248 // 28)  # cell width
    x = 0
    y = 0
    for row in cells:
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
                                [x + 2, y - c_x, 2*c_x, 2*c_y], pi, 1.45*pi, 1)
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
                                [x - c_x - 2, y + (0.4 * c_y), 2*c_x, 2.3*c_y],
                                0.05*pi, 0.5*pi, 1)
            if cell == 6:
                pygame.draw.arc(screen, colors['blue'],
                                [x + (0.5 * c_x) + 1, y + (0.5 * c_y) + 2,
                                0.8*c_x, c_y], 0.4*pi, 1.05*pi, 1)
                pygame.draw.arc(screen, colors['blue'], [x + 2, y + (0.4 * c_y),
                                2*c_x, 2*c_y], 0.5*pi, pi, 1)
            if cell == 7:
                pygame.draw.rect(screen, colors['blue'], (x + (0.5 * c_x) - 1, y - 1, 1, 1))
                pygame.draw.arc(screen, colors['blue'],
                                [x + (0.5 * c_x) - 1, y - (0.5 * c_y) + 1,
                                c_x, c_y], pi, 1.45*pi, 1)
            if cell == 8:
                pygame.draw.rect(screen, colors['blue'], (x - 1, y + 2, 2, 1))
                pygame.draw.arc(screen, colors['blue'],
                                [x - (0.5 * c_x) + 2, y - (0.5 * c_y) + 1,
                                0.8*c_x, c_y], 1.55*pi, 0.05*pi, 1)
            if cell == 9:
                pygame.draw.arc(screen, colors['blue'],
                                [x + (0.5 * c_x) - 1, y + (0.5 * c_y) - 1,
                                0.8*c_x, c_y], 0.4*pi, 1.05*pi, 1)
            if cell == 10:
                pygame.draw.rect(screen, colors['blue'], (x - 1, y + 2, 1, 1))
                pygame.draw.arc(screen, colors['blue'],
                                [x - (0.5 * c_x) + 2, y + (0.5 * c_y) - 1,
                                0.9*c_x, c_y], 1.9*pi, 0.6*pi, 1)
            if cell == 11:
                pygame.draw.line(screen, colors['blue'], (x, y + (0.3 * c_y)),
                                 (x + c_x, y + (0.3 * c_y)), 1)
                pygame.draw.line(screen, colors['blue'], (x, y + (0.7 * c_y) + 1),
                                 (x + c_x, y + (0.7 * c_y) + 1), 1)
            if cell == 12:
                pygame.draw.rect(screen, colors['blue'], (x - 2, y + (0.3 * c_y), 3, 1))
                pygame.draw.line(screen, colors['blue'],
                                 (x + 1, y + (0.3 * c_y)),
                                 (x + c_x + 2, y + (0.3 * c_y)), 1)
            if cell == 13:
                pygame.draw.line(screen, colors['blue'], (x + (0.3 * c_x), y),
                                 (x + (0.3 * c_x), y + c_y), 1)
                pygame.draw.line(screen, colors['blue'], (x + (0.7 * c_x), y),
                                 (x + (0.7 * c_x), y + c_y), 1)
            if cell == 14:
                pygame.draw.line(screen, colors['blue'],
                                (x + (0.5 * c_x) - 1, y - 1),
                                (x + (0.5 * c_x) - 1, y + c_y - 1), 1)
            x += c_x
        y += c_y
    pygame.draw.rect(screen, colors['blue'], (82, 86, 60, 32), width=1)
    pygame.draw.rect(screen, colors['blue'], (85, 89, 54, 26), width=1)
