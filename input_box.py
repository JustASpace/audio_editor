import pygame


pygame.init()

COLOR_INACTIVE = pygame.Color(145, 118, 116)
COLOR_ACTIVE = pygame.Color(0, 0, 0)
FONT = pygame.font.Font(None, 26)


class InputBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event, keys):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                # elif event.key == pygame.K_BACKSPACE:
                elif keys[pygame.K_BACKSPACE]:
                    self.text = self.text[:-1]
                # elif (event.key == pygame.K_v) and (event.mod & pygame.KMOD_CTRL):
                #     text = pygame.scrap.get(pygame.SCRAP_TEXT)
                #     print(text)
                #     if text:
                #         self.text = text
                #     else:
                #         pass
                else:
                    self.text += event.unicode
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        if self.rect.w > self.txt_surface.get_width() + 10 and self.text != '':
            self.rect.w = self.txt_surface.get_width() + 10
            return
        width = max(self.rect.w, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)
