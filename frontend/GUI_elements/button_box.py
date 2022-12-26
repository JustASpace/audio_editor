import pygame


pygame.init()


class ButtonBox:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        a, b = pygame.mouse.get_pos()
        if self.rect.x <= a <= self.rect.x + self.rect.width and self.rect.y <= b <= self.rect.y + self.rect.height:
            pygame.draw.rect(screen, (180, 180, 180), self)
        else:
            pygame.draw.rect(screen, (0, 0, 0), self)
