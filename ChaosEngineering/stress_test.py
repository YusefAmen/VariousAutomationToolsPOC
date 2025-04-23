import time
import threading

def burn(duration):
    end = time.time() + duration
    while time.time() < end:
        pass

for _ in range(2):  # Use 1–2 threads max
    t = threading.Thread(target=burn, args=(20,))  # 10 seconds
    t.start()

