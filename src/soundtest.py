import time
import mp3play
import subprocess

sound_name = "ImagineBreaker.mp3"
try:
    clip = mp3play.load(sound_name)
    clip.play()
    time.sleep(min(5, clip.seconds()))
    clip.stop()
except:
    # Termux Only
    imagine_breaker_cmd = ["cvlc", "--play-and-exit", sound_name]
    subprocess.run(imagine_breaker_cmd)
print("Done.")
