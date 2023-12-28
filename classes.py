import pygame
import sys
from math import pi
from classes_button import Button


class Character():
    def __init__(self, x, y, speed, radius):
        self._x = x
        self.y = y
        self.speed = speed
        self.radius = radius
        self._angle = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    def change_direction(self, new_angle):
        self._angle = new_angle

    @property
    def angle(self):
        return self._angle


class Pacman(Character):
    def __init__(self, x, y, speed, radius, lives=3):
        super().__init__(x, y, speed, radius)
        self.lives = lives

        self.angle_added = 0
        self.mouth_direction = 1

    def draw(self, screen, colors):
        pygame.draw.arc(screen, colors['yellow'], [self.x - self.radius,
                        self.y - self.radius,
                        2 * self.radius, 2 * self.radius],
                        self.angle + self.angle_added,
                        self.angle - self.angle_added, self.radius)

    def animate_mouth(self):
        self.angle_added += 0.03 * pi * self.mouth_direction
        if self.angle_added <= 0 or self.angle_added >= pi*0.3:
            self.mouth_direction *= -1


class Ghost(Character):
    def __init__(self, x, y, speed, radius, name, is_dead=False):
        super().__init__(x, y, speed, radius)
        self.is_dead = is_dead
        self.name = name

    def draw(self, screen):
        width = 2*self.radius
        image = pygame.image.load(f"ghosts/{self.name}.png")
        scaled_image = pygame.transform.scale(image, (width, width))
        rect = [self.x, self.y, width, width]
        screen.blit(scaled_image, rect)


class Board():
    def __init__(self, cells):
        self._cells = cells

    @property
    def cells(self):
        return self._cells

    def is_wall(self, x, y):
        return not (self.cells[x][y] in [0, 1, 2])

    def is_point(self, x, y):
        return self.cells[x][y] == 1

    def is_super_point(self, x, y):
        return self.cells[x][y] == 2

    def set_cell(self, x, y, value):
        self._cells[x][y] = value

    def draw(self, screen, colors):
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
                x += c_x
            y += c_y
        pygame.draw.rect(screen, colors['blue'], (93, 110, 65, 40), width=1)
        pygame.draw.rect(screen, colors['blue'], (97, 114, 57, 32), width=1)


class Game():
    def __init__(self, pacman, board, ghosts, screen, board_surface,
                 pacman_surface, clock, width, height, points=0,
                 points_to_win=242, super_point_left=4, high_score=0):
        self.pacman = pacman
        self.board = board
        self.ghosts = ghosts
        self.screen = screen
        self.board_surface = board_surface
        self.pacman_surface = pacman_surface
        self.clock = clock
        self.width = width
        self.height = height
        self.points = points
        self.points_to_win = points_to_win
        self.super_point_left = super_point_left
        self.high_score = high_score
        self._running = True

    def run(self, colors):
        undone = True
        button = Button("MENU", 400, 5, 25, 100, 30, self.back_to_menu)
        while self.running:

            # Handles keyboard events to change directions of pacman
            eventhandler = EventHandler(self.pacman)
            for event in pygame.event.get():
                eventhandler.handle_event(event)
                # Handles mouse event - exit game to menu if button clicked
                button.handle_event(event)

            # Renders consequences of game logic on surfaces
            renderer = Renderer(self.screen, self.board_surface,
                                self.pacman_surface, colors)
            # Cleans surfaces
            renderer.cleans_surfaces()

            # Draws on surfaces
            renderer.render_board(self.board)
            renderer.render_pacman(self.pacman)
            renderer.render_ghosts(self.ghosts)

            # Scales board surface to bigger one
            scaled_board_surface = pygame.transform.scale(
                self.board_surface, (self.width, self.height))

            # Puts surfaces on screen
            self.screen.blit(scaled_board_surface, (0, 40))
            self.screen.blit(self.pacman_surface, (0, 40))

            # On top of surfaces last renders to draw on screen
            renderer.render_score(self.points)
            renderer.render_lives(self.pacman)
            renderer.render_high_score(self.high_score)
            button.draw(self.screen, colors)

            self.pacman.animate_mouth()

            # Draws on surfaces
            self.moves(self.pacman)
            self.eats(self.pacman, self.board)

            # Checks if player won
            if self.won():
                self.not_running()

            # Collecting 4 super points gives additional life
            if undone is True and self.super_point_left == 0:
                self.pacman.lives += 1
                undone = False

            pygame.display.flip()
            self.clock.tick(30)

    @property
    def running(self):
        return self._running

    def not_running(self):
        self._running = False

    def running_again(self):
        self._running = True

    def eats(self, pacman, board):
        x, y = self.my_cell(pacman)
        if board.is_point(y, x):
            board.set_cell(y, x, 0)
            self.points += 10
            self.points_to_win -= 1
        if board.is_super_point(y, x):
            board.set_cell(y, x, 0)
            self.points += 50
            self.super_point_left -= 1

    def moves(self, pacman):
        if pacman.angle == pi and self.left_space(pacman):
            pacman.x -= pacman.speed
        elif pacman.angle == 0 and self.right_space(pacman):
            pacman.x += pacman.speed
        elif pacman.angle == pi/2 and self.up_space(pacman):
            pacman.y -= pacman.speed
        elif pacman.angle == 1.5*pi and self.down_space(pacman):
            pacman.y += pacman.speed

    def right_space(self, pacman):
        x, y = self.right_cell(pacman)
        pacman.x += pacman.speed
        border_line = pygame.Rect(pacman.x + pacman.radius - 4,
                                  pacman.y - 7, 3, 14)
        if x > 27 and y == 14:
            pacman.x = 0
            return True
        elif self.board.is_wall(y, x):
            wall = pygame.Rect(x*18 + 3, y*18, 18, 18)
            pacman.x -= pacman.speed
            return wall.colliderect(border_line) == 0
        else:
            pacman.x -= pacman.speed
            return True

    def left_space(self, pacman):
        x, y = self.left_cell(pacman)
        pacman.x -= pacman.speed
        border_line = pygame.Rect(pacman.x - pacman.radius + 4,
                                  pacman.y - 7, 3, 14)
        if x < 0 and y == 14:
            pacman.x = 27 * 18
            return True
        elif self.board.is_wall(y, x):
            wall = pygame.Rect(x*18 - 1, y*18, 18, 18)
            pacman.x += pacman.speed
            return wall.colliderect(border_line) == 0
        else:
            pacman.x += pacman.speed
            return True

    def up_space(self, pacman):
        x, y = self.up_cell(pacman)
        pacman.y -= pacman.speed
        border_line = pygame.Rect(pacman.x - 7,
                                  pacman.y - pacman.radius, 14, 3)
        if self.board.is_wall(y, x):
            wall = pygame.Rect(x*18, y*18 - 5, 18, 18)
            pacman.y += pacman.speed
            return wall.colliderect(border_line) == 0
        else:
            pacman.y += pacman.speed
            return True

    def down_space(self, pacman):
        x, y = self.down_cell(pacman)
        pacman.y += pacman.speed
        border_line = pygame.Rect(pacman.x - 7,
                                  pacman.y + pacman.radius, 14, 3)
        if self.board.is_wall(y, x):
            wall = pygame.Rect(x*18, y*18 + 5, 18, 18)
            pacman.y -= pacman.speed
            return wall.colliderect(border_line) == 0
        else:
            pacman.y -= pacman.speed
            return True

    def left_cell(self, player):
        x = (player.x - 2 * player.radius)//18
        y = player.y//18
        return (x, y)

    def right_cell(self, player):
        x = (player.x + 2 * player.radius)//18
        y = player.y//18
        return (x, y)

    def down_cell(self, player):
        x = player.x//18
        y = (player.y + 2 * player.radius)//18
        return (x, y)

    def up_cell(self, player):
        x = player.x//18
        y = (player.y - 2 * player.radius)//18
        return (x, y)

    def my_cell(self, player):
        x = player.x//18
        y = player.y//18
        return (x, y)

    def won(self):
        return self.points_to_win == 0

    def back_to_menu(self):
        print('back to men')
        self.not_running()


class EventHandler:
    def __init__(self, pacman):
        self.pacman = pacman

    def handle_event(self, event):
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


class Renderer:
    def __init__(self, screen, board_surface, pacman_surface, colors):
        self.screen = screen
        self.board_surface = board_surface
        self.pacman_surface = pacman_surface
        self.colors = colors

    def cleans_surfaces(self):
        self.screen.fill((0, 0, 0))
        self.board_surface.fill((0, 0, 0))
        self.pacman_surface.fill((0, 0, 0, 0))

    def render_board(self, board):
        board.draw(self.board_surface, self.colors)

    def render_pacman(self, pacman):
        pacman.draw(self.pacman_surface, self.colors)

    def render_ghosts(self, ghosts):
        for ghost in ghosts:
            ghost.draw(self.pacman_surface)

    def render_score(self, score):
        pygame.font.init()
        myfont = pygame.font.Font('arcade_font.ttf', 22)
        label = myfont.render(f"SCORE:{score}", 1, self.colors['blue'])
        self.screen.blit(label, (10, 600))

    def render_lives(self, pacman):
        for i in range(pacman.lives):
            pygame.draw.arc(self.screen, self.colors['yellow'],
                            [400 + 20 * i, 600,
                            2 * pacman.radius, 2 * pacman.radius],
                            pi/4, 1.75*pi, pacman.radius)

    def render_high_score(self, high_score):
        pygame.font.init()
        myfont = pygame.font.Font('arcade_font.ttf', 22)
        label = myfont.render(f"HIGH SCORE:{high_score}", 1,
                              self.colors['blue'])
        self.screen.blit(label, (10, 10))
