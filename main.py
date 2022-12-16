import subprocess


def cut(song="bb.mp3"):
    subprocess.Popen(f'ffmpeg -ss 60 -i {song} -t 15 -c copy out_cut.mp3')

def accelerate(song="bb.mp3", coef=2):
    subprocess.Popen(f'ffmpeg -i {song} -af atempo={coef} out_accelerated.mp3')

def reverse(song="bb.mp3"):
    subprocess.Popen(f'ffmpeg -i {song} -af areverse out_reversed.mp3')

def concat():
    pass

cut()
accelerate(coef=4)
reverse()