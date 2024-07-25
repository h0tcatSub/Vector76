import time
import mp3play

clip = mp3play.load("ImagineBreaker.mp3")
clip.play()
time.sleep(min(5, clip.seconds()))
clip.stop()