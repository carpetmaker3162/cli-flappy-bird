from getch import getch
import time
import queue
import threading

event_queue = queue.Queue()

def process_keys(q):
    while True:
        q.put(getch())

thread = threading.Thread(target=process_keys, args=(event_queue,))
thread.daemon = True
thread.start()

last_update = time.time()

while True:
    if time.time() - last_update > 0.5:
        last_update = time.time()

    if not event_queue.empty():
        key = event_queue.get().strip()
        # print(input_queue.get().strip(), end="")