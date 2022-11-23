# lmfao i just realized how sus my imports look
from getch import getch
import time
import queue
import threading
import sys
import termios
import os

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

event_queue = queue.Queue()

def process_keys(q):
    while True:
        q.put(getch())

def index(char):
    if char is None or char == " " or len(char) == 0:
        return -1
    else:
        return ord(char)

thread = threading.Thread(target=process_keys, args=(event_queue,))
thread.daemon = True
thread.start()

last_update = time.time()

while True:
    if time.time() - last_update > 0.5:
        last_update = time.time()
    
    if not event_queue.empty():
        key = event_queue.get().strip()
        
        if index(key) == 27:
            sys.stdout.flush()
            break
        
        print(index(key), end=" ")
        sys.stdout.flush()
        # print(input_queue.get().strip(), end="")

if os.name != "nt":
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)