import subprocess


class AudioEditorBackEnd:
    def __init__(self):
        pass

    def cut(song, start, cut_seconds):
        subprocess.Popen(f'ffmpeg -ss {start} -i {song} -t {cut_seconds} -c copy out_cut.mp3')

    def accelerate(song, coef):
        subprocess.Popen(f'ffmpeg -i {song} -af atempo={coef} {song}_out_accelerated_by_{coef}.mp3')

    def reverse(song):
        subprocess.Popen(f'ffmpeg -i {song} -af areverse {song}_reversed.mp3')

    def concat(song):
        pass

    def change_volume(song, coef):
        subprocess.Popen(f'ffmpeg -i {song} -af "volume={coef}" {song}_volume_changed_by_{coef}.mp3')