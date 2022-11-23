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

def process_keyboard_events(q):
    while True:
        q.put(getch())

thread = threading.Thread(target=process_keyboard_events, args=(event_queue,))
thread.daemon = True
thread.start()

def index(char):
    if char is None or char == " " or len(char) == 0:
        return 32
    else:
        return ord(char)

last_update = time.time()

while True:
    if time.time() - last_update > 0.5:
        last_update = time.time()
    
    if not event_queue.empty():
        key = event_queue.get().strip()
        
        if index(key) in (27, 3, 4):
            #sys.stdout.flush()
            break
        
        print(index(key), end=" ")
        #sys.stdout.flush()

# reset terminal settings when you exit the game
if os.name != "nt":
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)