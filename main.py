# lmfao i just realized how sus my imports look
# also im going to put everything in one file until theres too much stuff for me to scroll through
import time
import threading
import sys
import termios
import os
import random
from getch import getch

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
event_queue = []
IS_WIN = os.name == "nt"

def process_keyboard_events(q):
    while True:
        q.append(getch())

def reset_terminal():
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

thread = threading.Thread(target=process_keyboard_events, args=(event_queue,))
thread.daemon = True
thread.start()

SCREENW, SCREENH = os.get_terminal_size() # game scene will be 16 lines long in the terminal
REFRESH_RATE = 0.25

class Scene:
    """Game Scene
    
    Coordinate system:
       _______________________________________x
      |0  1  2  3  4  5  6  7  8  9  10 11 12 ...
      |1
      |2
      |3
      |4
      |5
      |6
      |7
     y...
    """
    def __init__(self) -> None:
        self.pipes = [] # (openingX, openingY)
        self.last_pipe_generated = 0 # in no particular unit, counted per "frame"/refresh
        self.frame = 0
        self.matrix = [[0] * SCREENW] * 16 # this will be used to detect collision & will contain where all the hitboxes are located. update this matrix and then print the screen from it (round when updating player y)
        self.player = Player()
    
    def print(self):
        # first clear the screen
        if IS_WIN:
            # fuck windows fr
            os.system("cls")
        else:
            os.system("clear")
    
    def refresh(self): # note: refresh and check for collision BEFORE printing out the new screen, so that collision (game end) can be detected before it is displayed
        self.frame += 1
        
        if self.frame - self.last_pipe_generated > 6:
            # generate new pipe
            pass
        
        self.pipes = list(filter(lambda a: a[0] >= 0, self.pipes))
        for idx, pipe in self.pipes:
            # move all pipes to the left
            self.pipes[idx][0] -= 1
        


class Player:
    def __init__(self) -> None:
        self.y = 8
        self.y_speed = 0 # y_speed and y are both going to be floats at some point or another so probably just round when drawing the player in Scene

def index(char):
    if char is None or char == " " or len(char) == 0:
        return 32
    else:
        return ord(char)

last_update = time.time()

while True:
    if time.time() - last_update > REFRESH_RATE:
        # refresh objects on the screen
        last_update = time.time()
    
    if event_queue:
        key = event_queue.pop(0)
        
        # process keyboard events here
        if index(key) in (27, 3, 4):
            sys.stdout.flush()
            break
        
        print(index(key), end=" ")
        sys.stdout.flush()

# reset terminal settings when you exit the game
if IS_WIN:
    reset_terminal()