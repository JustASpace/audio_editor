import pygame
from input_box import InputBox
from button_box import ButtonBox
from audio_editor_backend import AudioEditorBackEnd
from dropdown import DropDown


class AudioEditorFrontEnd:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.font = "Georgia"
        self.font_size = 20
        self.FPS = 30
        self.backward = (199, 198, 173)
        self.backend = AudioEditorBackEnd()
        self.input_boxes = dict()
        self.texts = dict()
        self.dropdown = None
        self.buttons = dict()

    def start(self):
        pygame.init()
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Аудиоредактор')
        clock = pygame.time.Clock()

        self.create_texts()
        self.create_input_boxes()
        self.create_buttons()
        self.create_dropdown()

        # DropDown

        while True:
            screen.fill(self.backward)

            # DropDown
            events = pygame.event.get()

            self.handle_events(events)

            self.draw_texts(screen)
            # self.draw_input_boxes(screen)
            self.draw_buttons(screen)
            # DropDown
            self.dropdown.draw(screen)
            # print(dropdown.last_option)

            pygame.display.update()
            clock.tick(self.FPS)

    def handle_events(self, events):
        self.dropdown_handle_event(events)
        for event in events:
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.MOUSEMOTION:
                print(f"Position: {event.pos}")
            self.boxes_handle_event(event, keys)
            self.buttons_handle_event(event)

    def dropdown_handle_event(self, events):
        selected_option = self.dropdown.update(events)
        if selected_option > -1:
            self.dropdown.main = self.dropdown.options[selected_option]

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
                    elif button == 'concat_button':
                        song1, song2 = self.input_boxes["song_input"].text.split('+')
                        self.backend.concat(song1, song2)

    def create_texts(self):
        font = pygame.font.SysFont(self.font, self.font_size, bold=True)
        self.texts['input_text'] = font.render('Введите название файла:', True, 'white')
        self.texts['question_text'] = font.render('Что хотим сделать?', True, 'white')
        self.texts['acceleration_text'] = font.render('Ускорить с коэффициентом:', True, 'white')
        self.texts['change_volume_text'] = font.render('Изменить громкость с коэффициентом:', True, 'white')
        self.texts['cut_from_text'] = font.render('Обрезать, начиная с', True, 'white')
        self.texts['cut_to_text'] = font.render('секунды, длительность в', True, 'white')
        self.texts['reverse_text'] = font.render('Обратить', True, 'white')
        self.texts['concat_text'] = font.render('Объединить два файла (В названии: "1.mp3+2.wav")', True, 'white')

    def create_input_boxes(self):
        self.input_boxes["song_input"] = (InputBox(300, 15, 100, 32))
        self.input_boxes["acceleration_input"] = (InputBox(330, 98, 30, 32))
        self.input_boxes["change_volume_input"] = (InputBox(450, 137, 30, 32))
        self.input_boxes["cut_from_input"] = (InputBox(243, 178, 30, 32))
        self.input_boxes["cut_to_input"] = (InputBox(555, 178, 30, 32))

    def create_buttons(self):
        # self.buttons['acceleration_button'] = ButtonBox(370, 98, 30, 30)
        # self.buttons['change_volume_button'] = ButtonBox(490, 137, 30, 30)
        # self.buttons['cut_button'] = ButtonBox(595, 178, 30, 30)
        # self.buttons['reverse_button'] = ButtonBox(128, 222, 30, 30)
        # self.buttons['concat_button'] = ButtonBox(600, 260, 30, 30)
        self.buttons['execute_button'] = ButtonBox(280, 120, 50, 50)

    def create_dropdown(self):
        # DropDown
        COLOR_INACTIVE = (100, 80, 255)
        COLOR_ACTIVE = (100, 200, 255)
        COLOR_LIST_INACTIVE = (255, 100, 100)
        COLOR_LIST_ACTIVE = (255, 150, 150)

        # DropDown
        self.dropdown = DropDown(
            [COLOR_INACTIVE, COLOR_ACTIVE],
            [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
            40, 120, 200, 50,
            pygame.font.SysFont(None, 30),
            "Выберите опцию", ["Ускорение", "Громкость", "Обрезка", "Инвертирование",
                               "Объединение"])

    def draw_texts(self, screen):
        # screen.blit(self.texts['input_text'], (20, 20))
        # screen.blit(self.texts['question_text'], (20, 60))
        if self.dropdown.last_option == -1:
            pass
        elif self.dropdown.last_option == 0:
            screen.blit(self.texts['acceleration_text'], (self.dropdown.rect.x,
                                                          self.dropdown.rect.y + 70))
        elif self.dropdown.last_option == 1:
            screen.blit(self.texts['change_volume_text'], (self.dropdown.rect.x,
                                                          self.dropdown.rect.y + 70))
        elif self.dropdown.last_option == 2:
            screen.blit(self.texts['cut_from_text'], (self.dropdown.rect.x,
                                                          self.dropdown.rect.y + 70))
            screen.blit(self.texts['cut_to_text'], (20 + self.texts['cut_from_text'].get_width() + 40,
                                                    self.dropdown.rect.y + 70))
        elif self.dropdown.last_option == 3:
            pass
        elif self.dropdown.last_option == 4:
            pass
        # screen.blit(self.texts['change_volume_text'], (20, 140))
        # screen.blit(self.texts['cut_from_text'], (20, 180))
        # screen.blit(self.texts['cut_to_text'], (20 + self.texts['cut_from_text'].get_width() + 40, 180))
        # screen.blit(self.texts['reverse_text'], (20, 220))
        # screen.blit(self.texts['concat_text'], (20, 260))

    def draw_input_boxes(self, screen):
        for box in self.input_boxes.keys():
            self.input_boxes[box].update()
            self.input_boxes[box].draw(screen)

    def draw_buttons(self, screen):
        for button in self.buttons.keys():
            self.buttons[button].draw(screen)


