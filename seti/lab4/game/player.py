import pygame

class Player():
    width = height = 50

    def __init__(self, startx, starty, ind, color=(255,0,0)):
        self.x = startx
        self.y = starty
        self.velocity = 2
        self.color = color
        self.ind = str(ind)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, g):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(g, self.color , self.rect, 0)
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.ind, True, (255,255,255))
        g.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y - 3 + (self.height/2 - text.get_height()/2)))
        

    def move(self, dirn):
        """
        :param dirn: 0 - 3 (right, left, up, down)
        :return: None
        """

        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity