import pygame

class Point():
    min_radius = 9
    max_radius = 20
    max_cost = 5

    def __init__(self, leftCornerX, leftCornerY, ind, cost, color=(255,0,0), font_size=20):
        self.velocity = 2
        self.color = color
        self.ind = str(ind)
        self.cost = cost
        self.radius = self.min_radius + cost * (self.max_radius - self.min_radius) / self.max_cost
        self.x = leftCornerX + self.radius
        self.y = leftCornerY + self.radius
        self.font_size = font_size

    def draw(self, screen, player):
        circle = pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)
        font = pygame.font.SysFont("comicsans", self.font_size)
        text = font.render(str(self.cost), True, (255, 255, 255))
        screen.blit(text, (self.x - text.get_width()/2, self.y - text.get_height()/2 - 2))
        if circle.colliderect(player.rect):
            return True
        return False
    