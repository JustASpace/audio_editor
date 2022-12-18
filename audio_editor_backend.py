import subprocess


class AudioEditorBackEnd:
    def __init__(self):
        pass

    def cut(song="bb.mp3", start=60, cut_seconds=15):
        subprocess.Popen(f'ffmpeg -ss {start} -i {song} -t {cut_seconds} -c copy out_cut.mp3')

    def accelerate(song="bb.mp3", coef=2):
        subprocess.Popen(f'ffmpeg -i {song} -af atempo={coef} {song}_out_accelerated_by_{coef}.mp3')

    def reverse(song="bb.mp3"):
        subprocess.Popen(f'ffmpeg -i {song} -af areverse {song}_reversed.mp3')

    def concat(song="bb.mp3"):
        pass

    def change_volume(song="bb.mp3", coef=0.5):
        subprocess.Popen(f'ffmpeg -i {song} -af "volume={coef}" {song}_volume_changed_by_{coef}.mp3')