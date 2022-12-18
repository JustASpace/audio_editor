import pygame
from input_box import InputBox
from audio_editor_backend import AudioEditorBackEnd


class AudioEditorFrontEnd:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.font = "Georgia"
        self.font_size = 20
        self.FPS = 15
        self.backward = (189, 155, 207)
        self.backend = AudioEditorBackEnd

    def start(self):
        pygame.init()

        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Аудиоредактор')
        clock = pygame.time.Clock()

        font = pygame.font.SysFont(self.font, self.font_size, bold=True)
        quit_text = font.render('Выход', True, 'white')
        input_text = font.render('Введите название файла:', True, 'white')
        question_text = font.render('Что хотим сделать?', True, 'white')
        acceleration_text = font.render('Ускорить в', True, 'white')
        change_volume_text = font.render('Изменить громкость в', True, 'white')
        cut_from_text = font.render('Обрезать, начиная с', True, 'white')
        cut_to_text = font.render('секунды, длительность в', True, 'white')
        reverse_text = font.render('Обратить', True, 'white')

        button = pygame.Rect(100, 500, 73, 42)

        input_boxes = []
        input_boxes.append(InputBox(300, 10, 10, 32))
        input_boxes.append(InputBox(input_boxes[0].rect.x - 150, input_boxes[0].rect.y + 110, 10, 32))

        reverse_button = pygame.Rect(400, 400, 72, 42)

        while True:
            screen.fill(self.backward)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if button.collidepoint(event.pos):
                        pygame.quit()
                    elif reverse_button.collidepoint(event.pos):
                        self.backend.reverse(input_boxes[0].text)
                elif event.type == pygame.MOUSEMOTION:
                    print(f"Position: {event.pos}")
                for box in input_boxes:
                    box.handle_event(event)
            for box in input_boxes:
                box.update()
                box.draw(screen)
            a, b = pygame.mouse.get_pos()
            if button.x <= a <= button.x + 73 and button.y <= b <= button.y + 42:
                pygame.draw.rect(screen, (180, 180, 180), button)
            else:
                pygame.draw.rect(screen, (110, 110, 110), button)

            pygame.draw.rect(screen, (110, 110, 110), reverse_button)

            screen.blit(quit_text, (button.x + 5, button.y + 5))
            screen.blit(input_text, (input_boxes[0].rect.x - 280, input_boxes[0].rect.y + 5))
            screen.blit(question_text, (input_boxes[0].rect.x - 280, input_boxes[0].rect.y + 55))
            screen.blit(acceleration_text, (input_boxes[0].rect.x - 280, input_boxes[0].rect.y + 110))
            screen.blit(change_volume_text, (input_boxes[0].rect.x - 280, input_boxes[0].rect.y + 165))
            screen.blit(cut_from_text, (input_boxes[0].rect.x - 280, input_boxes[0].rect.y + 220))
            screen.blit(cut_to_text, (input_boxes[0].rect.x - 20, input_boxes[0].rect.y + 220))
            screen.blit(reverse_text, (input_boxes[0].rect.x - 280, input_boxes[0].rect.y + 275))



            pygame.display.update()
            clock.tick(self.FPS)

    def create_buttons(self):
        pygame.display.update()
        pass
