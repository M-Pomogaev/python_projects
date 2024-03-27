import pygame
import button as bt
import circle_botton as cb

class GameEndScreen:
    def __init__(self, canvas, w, h):
        self.width = w
        self.height = h
        self.canvas = canvas
        x = w / 2
        y = h / 2
        r = 18
        self.indent = 5
        self.buttons = {"Back": bt.Button(5, h - 55, 130, 50, (255, 255, 255), "Back", (0, 0, 0), 24, 5)}
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
    
    def set_scores(self, scores, pl_id):
        self.pl_id = pl_id
        self.scores = scores
        self.endPhrase = ""
        self.winner = scores.index(max(scores))
        if (pl_id == self.winner):
            self.endPhrase += "You Won!"
        else:
            self.endPhrase += "HAHA! You Lost..."
    def draw(self):
        self.canvas.draw_background()
        bt.draw_textbox(self.canvas.get_canvas(), self.endPhrase, self.width, 100, (255, 255, 255), (0, 0, 0), 0, 40)
        for i in range(len(self.scores)):
            text = "Player " + str(i) + ": " + str(self.scores[i])
            font = 20
            if (i == self.winner):
                font = 35
            if (i == self.pl_id):
                bt.draw_textbox(self.canvas.get_canvas(), text, self.width, 200 + i*40, (255, 255, 255), (0, 0, 255), 0, font)
            else:
                bt.draw_textbox(self.canvas.get_canvas(), text, self.width, 200 + i*40, (255, 255, 255), (255, 0, 0), 0, font)
        clicked = "None"
        for name, button in self.buttons.items():
            if (button.draw(self.canvas.get_canvas())):
                clicked = name
        self.canvas.update()
        return clicked