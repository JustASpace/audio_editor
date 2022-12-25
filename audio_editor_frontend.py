import tkinter.filedialog
import pygame
from pygame import mixer
from input_box import InputBox
from button_box import ButtonBox
from audio_editor_backend import AudioEditorBackEnd
from dropdown import DropDown


def prompt_file():
    top = tkinter.Tk()
    top.withdraw()
    file_name = tkinter.filedialog.askopenfilename(filetypes=(("Audio Files", ".mp3 .wav"),))
    top.destroy()
    return file_name


class AudioEditorFrontEnd:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.font = "comicsansms"
        self.font_size = 20
        self.FPS = 30
        self.backward = (30, 46, 71)
        self.backend = AudioEditorBackEnd()
        self.input_boxes = dict()
        self.texts = dict()
        self.dropdown = None
        self.buttons = dict()
        self.current_audio_file = ''
        self.current_audio_file_path = ''
        self.audio_to_concat = ''
        self.audio_to_concat_path = ''
        self.is_paused = False
        self.option_to_command = {-1: None,
                                  0: self.backend.accelerate,
                                  1: self.backend.change_volume,
                                  2: self.backend.cut,
                                  3: self.backend.reverse,
                                  4: self.backend.concat}

    def start(self):
        pygame.init()
        mixer.init()

        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Аудиоредактор')
        clock = pygame.time.Clock()

        self.create_dropdown()
        self.create_texts()
        self.create_input_boxes()
        self.create_buttons()

        while True:
            screen.fill(self.backward)
            events = pygame.event.get()

            self.handle_events(events)
            self.dropdown.draw(screen)
            self.draw_buttons(screen)
            self.draw_texts_and_input_boxes(screen)

            pygame.display.update()
            clock.tick(self.FPS)

    def handle_events(self, events):
        self.dropdown_handle_event(events)
        for event in events:
            keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
            # elif event.type == pygame.MOUSEMOTION:
            #     print(f"Position: {event.pos}")
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
                    if button == 'choose_file_button':
                        file = prompt_file()
                        if file == '':
                            continue
                        self.current_audio_file_path = file
                        mixer.music.load(file)
                        self.current_audio_file = file[file.rfind("/") + 1:]
                        font = pygame.font.SysFont(self.font, self.font_size, bold=True)
                        self.texts['current_audio_file'] = font.render(self.current_audio_file, True, 'green')
                    elif button == 'execute_button':
                        if self.dropdown.last_option == 0 or self.dropdown.last_option == 1:
                            self.option_to_command[self.dropdown.last_option](self.current_audio_file_path,
                                                                              self.input_boxes['coefficient'].text)
                        elif self.dropdown.last_option == 2:
                            self.option_to_command[self.dropdown.last_option](self.current_audio_file_path,
                                                                              self.input_boxes['cut_1'].text,
                                                                              self.input_boxes['cut_2'].text)
                        elif self.dropdown.last_option == 3:
                            self.option_to_command[self.dropdown.last_option](self.current_audio_file_path)
                        elif self.dropdown.last_option == 4:
                            print(self.current_audio_file_path)
                            print(self.audio_to_concat_path)
                            self.option_to_command[self.dropdown.last_option](self.current_audio_file_path,
                                                                              self.audio_to_concat_path)
                    elif button == 'choose_file_to_concat_button':
                        file = prompt_file()
                        if file == '':
                            continue
                        self.audio_to_concat = file[file.rfind("/") + 1:]
                        self.audio_to_concat_path = file
                        font = pygame.font.SysFont(self.font, 14, bold=True)
                        self.texts['audio_to_concat'] = font.render(self.audio_to_concat, True, 'green')
                    if self.current_audio_file != '':
                        if button == 'play_button':
                            mixer.music.play()
                        elif button == 'pause_button':
                            if self.is_paused:
                                mixer.music.unpause()
                                self.is_paused = False
                            else:
                                mixer.music.pause()
                                self.is_paused = True
                        elif button == 'stop_button':
                            mixer.music.stop()

    def create_texts(self):
        font = pygame.font.SysFont(self.font, self.font_size, bold=True)
        self.texts['current_audio_file'] = font.render('', True, 'green')
        self.texts['audio_to_concat'] = font.render('', True, 'green')
        self.texts['play'] = font.render('Play', True, 'green')
        self.texts['pause'] = font.render('Pause', True, 'green')
        self.texts['stop'] = font.render('Stop', True, 'green')
        self.texts['choose_file'] = font.render('Выберите файл', True, 'green')

        self.texts['coefficient'] = font.render('Коэффициент:', True, 'green')
        self.texts['cut_1'] = font.render('C', True, 'green')
        self.texts['cut_2'] = font.render('секунды, длительность в', True, 'green')
        self.texts['reverse_text'] = font.render('Обратить', True, 'green')
        self.texts['concat_text'] = font.render('Выберите файл для объединения', True, 'green')
        self.texts['execute'] = font.render('Выполнить', True, 'green')

    def create_input_boxes(self):
        self.input_boxes["coefficient"] = (InputBox(self.dropdown.rect.x + 360, self.dropdown.rect.y + 10, 30, 32))
        self.input_boxes["cut_1"] = (InputBox(self.dropdown.rect.x + 225, self.dropdown.rect.y + 15,
                                              self.texts["cut_1"].get_width(), self.texts["cut_1"].get_height()))
        self.input_boxes["cut_2"] = (InputBox(self.dropdown.rect.x + 540, self.dropdown.rect.y + 15,
                                              self.texts["cut_1"].get_width(), self.texts["cut_1"].get_height()))

    def create_buttons(self):
        self.buttons['execute_button'] = ButtonBox(660, 130, self.texts['execute'].get_width(),
                                                   self.texts['execute'].get_height())
        self.buttons['choose_file_button'] = ButtonBox(40, 40, self.texts['choose_file'].get_width(),
                                                       self.texts['choose_file'].get_height())
        self.buttons['play_button'] = ButtonBox(240, 40, self.texts['play'].get_width(),
                                                self.texts['play'].get_height())
        self.buttons['pause_button'] = ButtonBox(300, 40, self.texts['pause'].get_width(),
                                                 self.texts['pause'].get_height())
        self.buttons['stop_button'] = ButtonBox(370, 40, self.texts['stop'].get_width(),
                                                self.texts['stop'].get_height())
        self.buttons['choose_file_to_concat_button'] = ButtonBox(250, 130, self.texts['concat_text'].get_width(),
                                                                 self.texts['concat_text'].get_height())

    def create_dropdown(self):
        COLOR_INACTIVE = (0, 0, 0)
        COLOR_ACTIVE = (180, 180, 180)
        COLOR_LIST_INACTIVE = (180, 180, 180)
        COLOR_LIST_ACTIVE = (90, 90, 180)

        self.dropdown = DropDown(
            [COLOR_INACTIVE, COLOR_ACTIVE],
            [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
            40, 120, 200, 50,
            pygame.font.SysFont(self.font, self.font_size),
            "Выберите опцию", ["Ускорение", "Громкость", "Обрезка", "Инвертирование",
                               "Объединение"])

    def draw_texts_and_input_boxes(self, screen):
        screen.blit(self.texts['current_audio_file'], (300, 5))
        screen.blit(self.texts['choose_file'], (40, 40))
        screen.blit(self.texts['play'], (240, 40))
        screen.blit(self.texts['pause'], (300, 40))
        screen.blit(self.texts['stop'], (370, 40))
        screen.blit(self.texts['execute'], (self.dropdown.rect.x + 620, self.dropdown.rect.y + 10))

        text_location = (self.dropdown.rect.x + 210, self.dropdown.rect.y + 10)

        if self.dropdown.last_option == -1:
            pass
        elif self.dropdown.last_option == 0 or self.dropdown.last_option == 1:
            screen.blit(self.texts['coefficient'], text_location)
            self.input_boxes["coefficient"].update()
            self.input_boxes["coefficient"].draw(screen)
        elif self.dropdown.last_option == 2:
            screen.blit(self.texts['cut_1'], text_location)
            screen.blit(self.texts['cut_2'], (self.dropdown.rect.x + 285,
                                              self.dropdown.rect.y + 10))
            self.input_boxes["cut_1"].update()
            self.input_boxes["cut_1"].draw(screen)
            self.input_boxes["cut_2"].update()
            self.input_boxes["cut_2"].draw(screen)
        elif self.dropdown.last_option == 3:
            pass
        elif self.dropdown.last_option == 4:
            screen.blit(self.texts['audio_to_concat'], (self.dropdown.rect.x + 285,
                                                        self.dropdown.rect.y - 10))
            screen.blit(self.texts['concat_text'], text_location)

    def draw_buttons(self, screen):
        for button in self.buttons.keys():
            if button == 'choose_file_to_concat_button':
                if self.dropdown.last_option != 4:
                    continue
            self.buttons[button].draw(screen)
