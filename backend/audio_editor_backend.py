import os.path
import shutil
import subprocess
import tempfile


class AudioEditorBackEnd:
    def __init__(self):
        self.working_dir = ''
        self.prog_dir = ''
        pass

    def create_temp_directory(self):
        self.working_dir = tempfile.mkdtemp()
        self.prog_dir = tempfile.mkdtemp()

    def remove_temp_directory(self):
        shutil.rmtree(self.working_dir)
        shutil.rmtree(self.prog_dir)

    def cut(self, song: str, start: int, cut_seconds: int):
        song, format = song[:song.rfind('.')], song[song.rfind('.') + 1:]
        song_only = song[song.rfind('/') + 1:]
        subprocess.Popen(rf'ffmpeg -ss {start} -i "{song}.{format}" -t {cut_seconds} -c copy "{self.working_dir}\{song_only}_cut.{format}"')

    def accelerate(self, song: str, coef: float):
        song, format = song[:song.rfind('.')], song[song.rfind('.') + 1:]
        song_only = song[song.rfind('/') + 1:]
        subprocess.Popen(rf'ffmpeg -i "{song}.{format}" -af atempo={coef} "{self.working_dir}\{song_only}_accelerated_by_{coef}.{format}"')

    def reverse(self, song: str, directory=''):
        if directory == '':
            directory = self.working_dir
        song, format = song[:song.rfind('.')], song[song.rfind('.') + 1:]
        song_only = song[song.rfind('/') + 1:]
        if directory == self.prog_dir:
            subprocess.Popen(rf'ffmpeg -i "{song}.{format}" -af areverse "{directory}\{song_only}_reversed.mp3"')
            return
        subprocess.Popen(rf'ffmpeg -i "{song}.{format}" -af areverse "{directory}\{song_only}_reversed.{format}"')

    def concat(self, song1: str, song2: str):
        song1, format1 = song1[:song1.rfind('.')], song1[song1.rfind('.') + 1:]
        song2, format2 = song2[:song2.rfind('.')], song2[song2.rfind('.') + 1:]
        song_only1 = song1[song1.rfind('/') + 1:]
        song_only2 = song2[song2.rfind('/') + 1:]
        if format2 != format1:
            subprocess.Popen(rf'ffmpeg -i "{song1}.{format1}" -i "{song2}.{format2}" -filter_complex "concat=n=2:v=0:a=1[a]" -map "[a]" '
                             rf'-codec:a libmp3lame -b:a 256k "{self.working_dir}\{song_only1}+{song_only2}.mp3"')
            return
        subprocess.Popen(rf'ffmpeg -i "{song1}.{format1}" -i "{song2}.{format2}" -filter_complex '
                         rf'"[0:0][1:0]concat=n=2:v=0:a=1[out]" -map "[out]" "{self.working_dir}\{song_only1}+{song_only2}.{format1}"')

    def change_volume(self, song: str, coef: float):
        song, format = song[:song.rfind('.')], song[song.rfind('.') + 1:]
        song_only = song[song.rfind('/') + 1:]
        subprocess.Popen(rf'ffmpeg -i "{song}.{format}" -af "volume={coef}" "{self.working_dir}\{song_only}_volume_changed_by_{coef}.{format}"')

    def move_to_working_directory(self, work_dir: str):
        for file in os.listdir(self.working_dir):
            scr_path = os.path.join(self.working_dir, file)
            dst_path = os.path.join(work_dir, file)
            os.rename(scr_path, dst_path)
