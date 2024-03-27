import pygame
import button as bt
from point import *

class Menu:

    def __init__(self, x, y, width, height, canvas, button_w, button_h, intend):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.canvas = canvas
        self.button_w = button_w
        self.button_h = button_h
        self.intend = intend
        self.buttons = {"Start": bt.Button(x, y, button_w, button_h, (255, 255, 255), "Start", (0, 0, 0), 24, intend),
                        "Join game": bt.Button(x, y+button_h+3 * intend, button_w, button_h, (255, 255, 255), "Join game", (0, 0, 0), 24, intend),
                        "Exit": bt.Button(x, y+button_h*2+6 * intend, button_w, button_h, (255, 255, 255), "Exit", (0, 0, 0), 24, intend),}
    
    def draw(self):
        self.canvas.draw_background()
        bt.draw_textbox(self.canvas.get_canvas(), "Menu", self.width, 100, (255, 255, 255), (0, 0, 0), 0, 40)
        clicked = "None"
        for name, button in self.buttons.items():
            if (button.draw(self.canvas.get_canvas())):
                clicked = name
        self.canvas.update()
        return clicked