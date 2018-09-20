from subprocess import call
import time
# ffmpeg -i video.mp4 -i audio.wav -c copy output.mkv
def merge():
    time.sleep(5)

    audio_stream = 'cwQgjq0mCdE_251.webm'
    video_stream = 'cwQgjq0mCdE_248.webm'
    output = 'output.mkv'

    call(['ffmpeg','-i',audio_stream,'-i',video_stream,'-c','copy',output])

def fib(n):
    if n == 1:
        return 1
    elif n == 0:
        return 0
    return fib(n-1)+fib(n-2)
