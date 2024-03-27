import pygame

class CountDownNumber:
    def __init__(self, x, y, color, number, font_size):
        self.x = x
        self.y = y
        self.color = color
        self.number = str(number)
        self.font_size = font_size

    def draw(self, screen):
        font = pygame.font.SysFont("comicsans", self.font_size)
        text = font.render(self.number, True, self.color)
        screen.blit(text, (self.x - text.get_width()/2, self.y - text.get_height()/2))
    