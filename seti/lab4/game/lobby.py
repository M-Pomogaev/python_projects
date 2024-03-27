import pygame
import button as bt
import circle_botton as cb

class Lobby:
    def __init__(self, canvas, w, h):
        self.width = w
        self.height = h
        self.canvas = canvas
        x = w / 2
        y = h / 2
        r = 18
        self.indent = 5
        self.options ={"2": cb.CircleButton(x - 3.5 * r, y, r, (0, 0, 0), "2", (0, 0, 0), 25, self.indent),
                        "3": cb.CircleButton(x, y, r, (0, 0, 0), "3", (0, 0, 0), 25, self.indent),
                        "4": cb.CircleButton(x + 3.5 * r, y, r, (0, 0, 0), "4", (0, 0, 0), 25, self.indent),}
        self.buttons = {"Back": bt.Button(5, h - 55, 130, 50, (255, 255, 255), "Back", (0, 0, 0), 24, 5),
                        "Start": bt.Button(w-5-130, h - 55, 130, 50, (255, 255, 255), "Start", (0, 0, 0), 24, 5)}
        pygame.init()
    
    def draw_creating(self):
        self.canvas.draw_background()
        bt.draw_textbox(self.canvas.get_canvas(), "Lobby", self.width, 100, (255, 255, 255), (0, 0, 0), 0, 40)
        bt.draw_textbox(self.canvas.get_canvas(), "Choose number of players...", self.width, 200, (255, 255, 255), (0, 0, 0), 0, 20)
        clicked = "None"
        for name, button in self.options.items():
            if (button.draw(self.canvas.get_canvas())):
                button.change_color((0, 0, 0), (255, 255, 255), 0)
                for name2, button2 in self.options.items():
                    if (name2 != name):
                        button2.change_color((0, 0, 0), (0, 0, 0), self.indent)
                clicked = name
        
        for name, button in self.buttons.items():
            if (button.draw(self.canvas.get_canvas())):
                clicked = name
        self.canvas.update()
        return clicked
    
    def draw_waiting(self):
        self.canvas.draw_background()
        screen = self.canvas.get_canvas()
        bt.draw_textbox(screen, "Lobby", self.width, 100, (255, 255, 255), (0, 0, 0), 0, 40)
        bt.draw_textbox(screen, "Waiting for players to connect...", self.width, 200, (255, 255, 255), (0, 0, 0), 0, 20)
        font = pygame.font.SysFont("comicsans", 20)
        text1 = font.render("Tip of the day: this        is you", True, (0,0,0))
        text2 = font.render("and these        are your enemies...", True, (0,0,0))
        screen.blit(text1, (40, 250))
        pygame.draw.rect(screen, (0, 0, 255), (233, 253, 30, 30))
        screen.blit(text2, (160, 285))
        pygame.draw.rect(screen, (255, 0, 0), (261, 288, 30, 30))
        clicked = "None"
        if (self.buttons["Back"].draw(self.canvas.get_canvas())):
            clicked = "Back"
        self.canvas.update()
        return clicked