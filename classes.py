import pygame


class Pacman():
    def __init__(self, screen, x, y, size, speed):
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed

    def draw(self):
        pygame.draw.circle(self.screen, (255, 255, 0),
                           (self.x, self.y), self.size)
