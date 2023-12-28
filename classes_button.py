import pygame
from functools import partial


class Button():

    def __init__(self, text, x, y, size, width, height, command, *args):
        self.text = text
        self.x = x
        self.y = y
        self.size = size
        self.width = width
        self.height = height
        self.command = partial(command, *args)

        self.rect = pygame.Rect(x, y, width, height)
        self.pushed = 0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_x, mouse_y):
                self.pushed = 1
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_x, mouse_y) and self.pushed == 1:
                print("Przycisk został kliknięty!")
                self.pushed = 0
                self.command()

    def draw(self, screen, colors):
        pygame.font.init()
        myfont = pygame.font.Font('arcade_font.ttf', self.size)
        label = myfont.render(self.text, 1, colors['blue'])
        screen.blit(label, (self.x, self.y))
        pygame.draw.rect(screen, colors['blue'],
                         (self.x, self.y, self.width, self.height), 1)
