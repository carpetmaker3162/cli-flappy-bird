# lmfao i just realized how sus my imports look
# also im going to put everything in one file until theres too much stuff for me to scroll through
TESTING = True

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
    if not IS_WIN:
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
      |   0  1  2  3  4  5  6  7  8  9  10 11 ...
      |0
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
        self.pipes = [] # [openingX, openingY]
        self.last_pipe_generated = 0 # in no particular unit, counted per "frame"/refresh
        self.frame = 0
        self.matrix = [[0] * SCREENW] * 16 # this will be used to detect collision & will contain where all the hitboxes are located. update this matrix and then print the screen from it (round when updating player y)
        self.player = Player()
        self.objcode = {0: " ", 1: "#", 2: "O"}
    
    def print(self, clear_screen=True):
        # clear_screen is for debugging purposes
        if clear_screen:
            os.system("cls" if IS_WIN else "clear")
        print("\r", end="")
        
        for row in self.matrix:
            for cell in row:
                print(self.objcode[cell], end="")
            print("\n\r", end="") # newline without breaking everything
    
    def refresh(self): # note: refresh and check for collision BEFORE printing out the new screen, so that collision (game end) can be detected before it is displayed
        self.frame += 1
        
        if self.frame - self.last_pipe_generated > 6:
            # generate new pipe
            pass
        
        self.pipes = list(filter(lambda a: a[0] >= 0, self.pipes))
        for idx, pipe in enumerate(self.pipes):
            # move all pipes to the left
            self.pipes[idx][0] -= 1
        
        self.load_matrix()
    
    def new_pipe(self):
        self.pipes.append([SCREENW-1, random.randrange(2, 14)])

    def load_matrix(self): # at this point im probably overcomplicating things but ehh this is easier for me
        """
        Loading pipes:
         ____________________x
        | 0 1 2 3 4 5 6 7 8 9
        |0    # #
        |1    # #
        |2    # #
        |3
        |4
        |5    # #
        |6    # #
        |7    # #
        y...

        openingX: 2
        openingY: 3
        """
        queue = self.pipes[:]
        blank_matrix = [[0] * SCREENW] * 16
        while queue: # uhh terrible time complexity but we'll see
            px, py = queue.pop(0)
            print("sz", (px, py))
            for mx in range(px, px + 2):
                for my in range(0, py):
                    blank_matrix[my][mx-1] = 1
                
                for my in range(py+3, 16):
                    blank_matrix[my][mx-1] = 1
        self.matrix = blank_matrix

class Player:
    def __init__(self) -> None:
        # y_speed and y are both going to be floats at some point or another so probably just round when drawing the player in Scene
        self.y = 8
        self.y_speed = 0 # positive number when going upwards. me when i suddenly realize why PyGame's coordinate system works like it does: 😔
        self.y_acceleration = 0 # positive number when going upwards
    
    def jump(self):
        # reminder to check how i made jumping in Poopland
        pass

def index(char):
    if char is None or char == " " or len(char) == 0:
        return 32
    else:
        return ord(char)

last_update = time.time()

if __name__ == "__main__":
    try:
        if TESTING:
                # test here
                scene = Scene()
                scene.new_pipe()
                scene.refresh()
                scene.print(clear_screen=False)
        else:
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
    except Exception as e:
        raise e
    finally:
        reset_terminal()