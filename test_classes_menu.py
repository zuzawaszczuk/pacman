from classes_menu import Button, Menu


def test_button_init():
    button = Button("Text", 0, 0, 100, 100, 1)
    assert button.text == "Text"
    assert button.x == 0
    assert button.y == 0
    assert button.width == 100
    assert button.height == 100
    assert button.command == 1


def test_menu_init():
    button = Button("Text", 0, 0, 100, 100, 1)
    buttons = [button]
    menu = Menu(buttons)
    assert menu.buttons == buttons
