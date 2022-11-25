# TODO: make the game get progressively more difficult
# TODO: instead of refreshing based on in-game "frames", refresh based on real-life time, to allow the player to move more smoothly
# TODO: after the above task is done, maybe make the physics a wee bit better
# TODO: keep track of score

import time
import threading
import sys
import termios
import os
import random
from getch import getch

TESTING = False # for my own use because i am lazy

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
event_queue = []
IS_WIN = os.name == "nt" # fuck windows fr

def process_keyboard_events(q):
    while True:
        q.append(getch())

def reset_terminal():
    # i need to get someone to test the game on windows to make sure it works.
    # ...if it doesnt its not like i can fix it myself since im on a mac but whatevs
    if not IS_WIN:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def index(char):
    # alternative to ord() that doesnt break when user presses space
    if char is None or char == " " or len(char) == 0:
        return 32
    else:
        return ord(char)

thread = threading.Thread(target=process_keyboard_events, args=(event_queue,))
thread.daemon = True
thread.start()

SCREENW, SCREENH = os.get_terminal_size()
REFRESH_RATE = 0.04 # in seconds
SCENE_HEIGHT = 20

class Player:
    def __init__(self) -> None:
        self.x = 10 # shouldnt ever change but just putting it here
        self.y = 8
        # positive number when going downwards. dont ask why
        self.y_speed = 1
        self.y_acceleration = 0.2
    
    def jump(self):
        self.y_speed = -1

class Scene:
    def __init__(self) -> None:
        self.pipes = []
        self.last_pipe_generated = 0
        self.frame = 0
        self.matrix = [[0 for i in range(SCREENW)] for i in range(SCENE_HEIGHT)] # collision/hitboxes
        self.player = Player()
        self.objcode = {0: " ", 1: "#", 2: "O"}
        self.dead = False
    
    def print(self, clear_screen=True):
        # clear_screen is for debugging purposes
        if clear_screen:
            print("\033[H")
        print("\r", end="")
        
        for row in self.matrix:
            for cell in row:
                print(self.objcode[cell], end="")
            print("\n\r", end="")
    
    def refresh(self):
        self.frame += 1
        self.pipes = list(filter(lambda a: a[0] >= 0, self.pipes)) # filter out pipes that are no longer on the screen
        
        # move all pipes to the left
        for idx, pipe in enumerate(self.pipes):
            self.pipes[idx][0] -= 1
        
        self.player.y_speed += self.player.y_acceleration
        self.player.y += self.player.y_speed
        self.load_matrix()
    
    def add_new_pipe(self):
        self.last_pipe_generated = self.frame
        self.pipes.append([SCREENW-2, random.randrange(2, 14)])

    def load_matrix(self):
        # loading the pipes
        queue = self.pipes[:]
        blank_matrix = [[0 for i in range(SCREENW)] for i in range(SCENE_HEIGHT)]
        while queue:
            px, py = queue.pop(0)
            
            # check for collision
            if self.player.x in range(px, px + 2) and (int(self.player.y) in range(py+3, SCENE_HEIGHT) or int(self.player.y) in range(0, py)):
                # raising an exception so that the `finally` clause is triggered. will change later
                raise SystemExit

            for mx in range(px, px + 2):
                for my in range(0, py):
                    blank_matrix[my][mx] = 1
                
                for my in range(py+3, SCENE_HEIGHT):
                    blank_matrix[my][mx] = 1
        
        self.matrix = blank_matrix
        
        # load the player
        self.matrix[int(self.player.y)][self.player.x] = 2

last_update = time.time()

if __name__ == "__main__":
    try:
        if TESTING:
            # when i need to test stuff
            pass
        else:
            os.system("cls" if IS_WIN else "clear")
            # initing
            scene = Scene()
            scene.add_new_pipe()
            scene.refresh()
            scene.print()
            # game loop
            while True:
                # refresh objects on the screen
                if time.time() - last_update > REFRESH_RATE:
                    last_update = time.time()
                    
                    # new pipe every 20 units. later on, as the game progresses, the pipes will become more frequent
                    if scene.frame - scene.last_pipe_generated >= 20:
                        scene.add_new_pipe()
                    
                    scene.refresh()
                    scene.print()
                
                if event_queue:
                    key = event_queue.pop(0)
                    
                    # process keyboard events
                    
                    if index(key) in (27, 3, 4): # press ESC, CTRL+C, or CTRL+D to exit
                        sys.stdout.flush()
                        break
                    elif index(key) == 32:
                        scene.player.jump()

                    sys.stdout.flush()
    # if i dont include the `except` clause the game will fail silently without showing the exeception`
    except Exception as e:
        raise e
    # so that the terminal doesnt stay fucked up when the player closes the game
    finally:
        reset_terminal()