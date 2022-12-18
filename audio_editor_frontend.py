import pygame
from input_box import InputBox
from button_box import ButtonBox
from audio_editor_backend import AudioEditorBackEnd


class AudioEditorFrontEnd:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.font = "Georgia"
        self.font_size = 20
        self.FPS = 60
        self.backward = (189, 155, 207)
        self.backend = AudioEditorBackEnd()
        self.input_boxes = dict()
        self.texts = dict()
        self.buttons = dict()

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Аудиоредактор')
        clock = pygame.time.Clock()

        self.create_texts()
        self.create_input_boxes()
        self.create_buttons()

        while True:
            screen.fill(self.backward)
            self.handle_events()

            self.draw_texts(screen)
            self.draw_input_boxes(screen)
            self.draw_buttons(screen)

            pygame.display.update()
            clock.tick(self.FPS)

    def handle_events(self):
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEMOTION:
                print(f"Position: {event.pos}")
            self.boxes_handle_event(event, keys)
            self.buttons_handle_event(event)

    def boxes_handle_event(self, event, keys):
        for box in self.input_boxes.keys():
            self.input_boxes[box].handle_event(event, keys)

    def buttons_handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons.keys():
                if self.buttons[button].rect.collidepoint(event.pos):
                    if button == 'acceleration_button':
                        self.backend.accelerate(self.input_boxes["song_input"].text,
                                                float(self.input_boxes["acceleration_input"].text))
                    elif button == 'change_volume_button':
                        self.backend.change_volume(self.input_boxes["song_input"].text,
                                                   self.input_boxes["change_volume_input"].text)
                    elif button == 'cut_button':
                        self.backend.cut(self.input_boxes["song_input"].text,
                                         int(self.input_boxes["cut_from_input"].text),
                                         int(self.input_boxes["cut_to_input"].text))
                    elif button == 'reverse_button':
                        self.backend.reverse(self.input_boxes["song_input"].text)
    def create_texts(self):
        font = pygame.font.SysFont(self.font, self.font_size, bold=True)
        self.texts['input_text'] = font.render('Введите название файла:', True, 'white')
        self.texts['question_text'] = font.render('Что хотим сделать?', True, 'white')
        self.texts['acceleration_text'] = font.render('Ускорить с коэффициентом', True, 'white')
        self.texts['change_volume_text'] = font.render('Изменить громкость с коэффициентом', True, 'white')
        self.texts['cut_from_text'] = font.render('Обрезать, начиная с', True, 'white')
        self.texts['cut_to_text'] = font.render('секунды, длительность в', True, 'white')
        self.texts['reverse_text'] = font.render('Обратить', True, 'white')

    def create_input_boxes(self):
        self.input_boxes["song_input"] = (InputBox(300, 15, 100, 32))
        self.input_boxes["acceleration_input"] = (InputBox(330, 98, 30, 32))
        self.input_boxes["change_volume_input"] = (InputBox(450, 137, 30, 32))
        self.input_boxes["cut_from_input"] = (InputBox(243, 178, 30, 32))
        self.input_boxes["cut_to_input"] = (InputBox(555, 178, 30, 32))

    def create_buttons(self):
        self.buttons['acceleration_button'] = ButtonBox(370, 98, 30, 30)
        self.buttons['change_volume_button'] = ButtonBox(490, 137, 30, 30)
        self.buttons['cut_button'] = ButtonBox(595, 178, 30, 30)
        self.buttons['reverse_button'] = ButtonBox(128, 222, 30, 30)

    def draw_texts(self, screen):
        screen.blit(self.texts['input_text'], (20, 20))
        screen.blit(self.texts['question_text'], (20, 60))
        screen.blit(self.texts['acceleration_text'], (20, 100))
        screen.blit(self.texts['change_volume_text'], (20, 140))
        screen.blit(self.texts['cut_from_text'], (20, 180))
        screen.blit(self.texts['cut_to_text'], (20 + self.texts['cut_from_text'].get_width() + 40, 180))
        screen.blit(self.texts['reverse_text'], (20, 220))

    def draw_input_boxes(self, screen):
        for box in self.input_boxes.keys():
            self.input_boxes[box].update()
            self.input_boxes[box].draw(screen)

    def draw_buttons(self, screen):
        for button in self.buttons.keys():
            self.buttons[button].draw(screen)

