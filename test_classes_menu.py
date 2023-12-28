from classes_menu import Menu
from classes_button import Button
import pygame
from unittest.mock import Mock


def test_button_init():
    def command():
        return Mock()
    button = Button("Text", 0, 0, 5, 100, 100, command, 5)
    assert button.text == "Text"
    assert button.x == 0
    assert button.y == 0
    assert button.size == 5
    assert button.width == 100
    assert button.height == 100
    assert button.command.func == command
    assert button.command.args == (5,)
    assert button.rect == pygame.Rect(0, 0, 100, 100)


def test_menu_init():
    def command():
        return Mock()
    button = Button("Text", 0, 0, 2, 100, 100, command, 5)
    buttons = [button]
    menu = Menu(5, buttons)
    assert menu.colors == 5
    assert menu.buttons == buttons


def test_menu_set_buttons():
    def command():
        return Mock()
    button = Button("Text", 0, 0, 2, 100, 100, command, 5)
    buttons = [button]
    menu = Menu(5)
    assert menu.colors == 5
    assert menu.buttons == []
    menu.set_buttons(buttons)
    assert menu.buttons == buttons


def test_menu_init_current_game():
    def command():
        return Mock()
    button = Button("Text", 0, 0, 2, 100, 100, command, 5)
    buttons = [button]
    menu = Menu(5, buttons)
    assert menu.current_game is None
