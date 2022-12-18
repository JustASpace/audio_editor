import subprocess


class AudioEditorBackEnd:
    def __init__(self):
        pass

    def cut(self, song: str, start: int, cut_seconds: int):
        song, format = song[:song.rfind('.')], song[song.rfind('.') + 1:]
        subprocess.Popen(f'ffmpeg -ss {start} -i {song}.{format} -t {cut_seconds} -c copy {song}_cut.{format}')

    def accelerate(self, song: str, coef: float):
        song, format = song[:song.rfind('.')], song[song.rfind('.') + 1:]
        subprocess.Popen(f'ffmpeg -i {song}.{format} -af atempo={coef} {song}_accelerated_by_{coef}.{format}')

    def reverse(self, song: str):
        song, format = song[:song.rfind('.')], song[song.rfind('.') + 1:]
        subprocess.Popen(f'ffmpeg -i {song}.{format} -af areverse {song}_reversed.{format}')

    def concat(self, song1: str, song2: str):
        song1, format1 = song1[:song1.rfind('.')], song1[song1.rfind('.') + 1:]
        song2, format2 = song2[:song2.rfind('.')], song2[song2.rfind('.') + 1:]
        if format2 != format1:
            subprocess.Popen(f'ffmpeg -i {song1}.{format1} -i {song2}.{format2} -filter_complex "concat=n=2:v=0:a=1[a]" -map "[a]" '
                             f'-codec:a libmp3lame -b:a 256k {song1}+{song2}.mp3')
            return
        subprocess.Popen(f'ffmpeg -i {song1}.{format1} -i {song2}.{format2} -filter_complex '
                         f'"[0:0][1:0]concat=n=2:v=0:a=1[out]" -map "[out]" {song1}+{song2}.{format1}')

    def change_volume(self, song: str, coef: float):
        song, format = song[:song.rfind('.')], song[song.rfind('.') + 1:]
        subprocess.Popen(f'ffmpeg -i {song}.{format} -af "volume={coef}" {song}_volume_changed_by_{coef}.{format}')

au = AudioEditorBackEnd()
au.concat("test.mp3", "test.wav")