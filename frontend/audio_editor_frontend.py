import os
import tkinter.filedialog
import pygame

from pygame import mixer
from backend.audio_editor_backend import AudioEditorBackEnd
from frontend.GUI_elements.button_box import ButtonBox
from frontend.GUI_elements.dropdown import DropDown
from frontend.GUI_elements.input_box import InputBox


def prompt_file(start_directory=os.getcwd()):
    top = tkinter.Tk()
    top.withdraw()
    file_name = tkinter.filedialog.askopenfilename(initialdir=start_directory,
                                                   filetypes=(("Audio Files", ".mp3 .wav"),))
    top.destroy()
    return file_name


class AudioEditorFrontEnd:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.font = "comicsansms"
        self.font_size = 20
        self.FPS = 60
        self.backward = (30, 46, 71)
        self.backend = AudioEditorBackEnd()
        self.dropdown = None
        self.input_boxes = dict()
        self.texts = dict()
        self.buttons = dict()
        self.current_audio_file = ''
        self.current_audio_file_path = ''
        self.audio_to_concat = ''
        self.audio_to_concat_path = ''
        self.option_to_command = {-1: None,
                                  0: self.backend.accelerate,
                                  1: self.backend.change_volume,
                                  2: self.backend.cut,
                                  3: self.backend.reverse,
                                  4: self.backend.concat}
        self.full_play_time = -1
        self.current_time = -1
        self.is_reversed = False

    def start(self):
        pygame.init()
        mixer.init()
        self.backend.create_temp_directory()

        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Аудиоредактор')
        clock = pygame.time.Clock()

        self.create_dropdown()
        self.create_texts()
        self.create_input_boxes()
        self.create_buttons()
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

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
                mixer.music.unload()
                self.backend.remove_temp_directory()
                pygame.quit()
            if event.type == pygame.USEREVENT:
                if self.is_reversed:
                    self.is_reversed = False
                    self.current_time = 0
                    mixer.music.unload()
                    mixer.music.load(self.current_audio_file_path)
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
                    font = pygame.font.SysFont(self.font, self.font_size, bold=True)

                    if button == 'choose_file_button' or button == 'created_files_button':
                        if button == 'created_files_button':
                            file = prompt_file(self.backend.working_dir)
                        else:
                            file = prompt_file()
                        if file == '':
                            continue
                        self.current_audio_file_path = file
                        self.full_play_time = round(mixer.Sound(file).get_length(), 3)
                        self.current_audio_file = file[file.rfind("/") + 1:]
                        self.option_to_command[3](self.current_audio_file_path, self.backend.prog_dir)
                        self.texts['current_audio_file'] = font.render(self.current_audio_file, True, 'green')
                        mixer.music.load(file)

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
                        elif self.dropdown.last_option == 4 and self.current_audio_file != ''\
                                and self.audio_to_concat != '':
                            self.option_to_command[self.dropdown.last_option](self.current_audio_file_path,
                                                                              self.audio_to_concat_path)

                    elif button == 'choose_file_to_concat_button' and self.dropdown.last_option == 4:
                        file = prompt_file()
                        if file == '':
                            continue
                        self.audio_to_concat = file[file.rfind("/") + 1:]
                        self.audio_to_concat_path = file
                        font = pygame.font.SysFont(self.font, 14, bold=True)
                        self.texts['audio_to_concat'] = font.render(self.audio_to_concat, True, 'green')

                    elif button == 'save_result_button':
                        mixer.music.unload()
                        self.current_audio_file = ''
                        self.current_audio_file_path = ''
                        self.texts['current_audio_file'] = font.render(self.current_audio_file, True, 'green')
                        self.backend.move_to_working_directory(os.getcwd())

                    if self.current_audio_file != '':
                        if button == 'play_button':
                            if mixer.music.get_pos() == -1:
                                mixer.music.play(0)
                            else:
                                if not self.is_reversed:
                                    mixer.music.unpause()
                                else:
                                    self.is_reversed = False
                                    self.current_time = self.current_time - mixer.music.get_pos() / 1000
                                    mixer.music.load(self.current_audio_file_path)
                                    mixer.music.play(0, self.current_time)
                        elif button == 'pause_button':
                            mixer.music.pause()
                        elif button == 'stop_button':
                            mixer.music.stop()
                            mixer.music.play(0, -1)
                            mixer.music.pause()
                        elif button == 'reverse_play_button':
                            if self.is_reversed:
                                mixer.music.unpause()
                            else:
                                self.is_reversed = True
                                self.current_time = mixer.music.get_pos() / 1000
                                song = self.current_audio_file[:self.current_audio_file.rfind('.')]
                                mixer.music.load(rf'{self.backend.prog_dir}\{song}_reversed.mp3')
                                mixer.music.play(0, self.full_play_time - self.current_time)

    def create_texts(self):
        font = pygame.font.SysFont(self.font, self.font_size, bold=True)
        self.texts['current_audio_file'] = font.render('', True, 'green')
        self.texts['audio_to_concat'] = font.render('', True, 'green')
        self.texts['play'] = font.render('Play', True, 'green')
        self.texts['pause'] = font.render('Pause', True, 'green')
        self.texts['stop'] = font.render('Stop', True, 'green')
        self.texts['reverse_play'] = font.render('Reverse play', True, 'green')
        self.texts['choose_file'] = font.render('Выберите файл', True, 'green')
        self.texts['created_files'] = font.render('Посмотреть измененные файлы', True, 'green')
        self.texts['created_files_description'] = font.render('(Так же можно выбрать для редактирования или удалить)', True, 'green')
        self.texts['save_current_files_to'] = font.render('Сохранить результат', True, 'green')

        self.texts['coefficient'] = font.render('Коэффициент:', True, 'green')
        self.texts['coefficient_accelerate'] = font.render('(Должен быть в пределах [0.5, 100])', True, 'green')
        self.texts['cut_1'] = font.render('C', True, 'green')
        self.texts['cut_2'] = font.render('секунды, длительность в', True, 'green')
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
        self.buttons['reverse_play_button'] = ButtonBox(430, 40, self.texts['reverse_play'].get_width(),
                                                        self.texts['reverse_play'].get_height())
        self.buttons['choose_file_to_concat_button'] = ButtonBox(250, 130, self.texts['concat_text'].get_width(),
                                                                 self.texts['concat_text'].get_height())
        self.buttons['created_files_button'] = ButtonBox(420, 530, self.texts['created_files'].get_width(),
                                                                 self.texts['created_files'].get_height())
        self.buttons['save_result_button'] = ButtonBox(420, 490, self.texts['save_current_files_to'].get_width(),
                                                                 self.texts['save_current_files_to'].get_height())

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
        screen.blit(self.texts['reverse_play'], (430, 40))
        screen.blit(self.texts['execute'], (self.dropdown.rect.x + 620, self.dropdown.rect.y + 10))
        screen.blit(self.texts['created_files'], (self.dropdown.rect.x + 380, self.dropdown.rect.y + 410))
        screen.blit(self.texts['created_files_description'], (self.dropdown.rect.x + 145, self.dropdown.rect.y + 440))
        screen.blit(self.texts['save_current_files_to'], (self.dropdown.rect.x + 380, self.dropdown.rect.y + 370))

        text_location = (self.dropdown.rect.x + 210, self.dropdown.rect.y + 10)

        if self.dropdown.last_option == -1:
            pass
        elif self.dropdown.last_option == 0 or self.dropdown.last_option == 1:
            if self.dropdown.last_option == 0:
                screen.blit(self.texts['coefficient_accelerate'], (250, 160))
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
