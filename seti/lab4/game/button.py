import pygame

def draw_textbox(screen, text, x, y, in_color, text_color, indent, font_size, width=-1, height=-1):
    if text != "":
        font = pygame.font.SysFont("comicsans", font_size)
        text = font.render(text, True, text_color)
        if width == -1:
            width = text.get_width()
            x = x/2 - width/2
        if height == -1:
            height = text.get_height()
            y = y - height/2
    pygame.draw.rect(screen, text_color, (x - indent, y - indent, width + 2*indent, height + 2*indent))
    box = pygame.draw.rect(screen, in_color, (x, y, width, height))
    screen.blit(text, (x + (width/2 - text.get_width()/2), y + (height/2 - text.get_height()/2)))
    return box

class Button:
    def __init__(self, x, y, width, height, color, text="", text_color=(0,255,0), font_size=24, indent=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.indent = indent
    
    def draw(self, screen):
        button = draw_textbox(screen, self.text, self.x, self.y, self.color, self.text_color, self.indent, self.font_size, self.width, self.height)
        pos = pygame.mouse.get_pos()
        clicked = False
        if button.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
        return clicked