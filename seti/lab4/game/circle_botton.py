import pygame

class CircleButton:
    def __init__(self, x, y, radius, color, text, text_color, font_size, indent):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.indent = indent

    def draw(self, screen):
        button = pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, self.indent)
        font = pygame.font.SysFont("comicsans", self.font_size)
        text = font.render(self.text, True, self.text_color)
        screen.blit(text, (self.x - text.get_width()/2, self.y - text.get_height()/2))
        pos = pygame.mouse.get_pos()
        clicked = False
        if button.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
        return clicked
    
    def change_color(self, color, text_color, indent):
        self.color = color
        self.text_color = text_color
        self.indent = indent