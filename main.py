# TODO: make the game get progressively more difficult
# TODO: make more variation, like different width pipes, different size opening pipes, etc

import time
import threading
import sys
import termios
import os
import random
import math
from getch import getch

TESTING = False # for my own use because i am lazy

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)
event_queue = []
IS_WIN = os.name == "nt" # fuck windows fr

def process_keyboard_events(q, dead):
    while not dead[0]:
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

def fwrite(s):
    with open("test.txt", "w") as f:
        f.write("\n\n")
        f.write(s)

SCREENW, SCREENH = os.get_terminal_size()
REFRESH_RATE = 0.05
PLAYER_REFRESH_RATE = 0.02
SCENE_HEIGHT = 20
PIPE_OPENING_SIZE = 6
MODE = 1

class Player:
    def __init__(self, mode) -> None:
        self.dead = [False] # simply using a bool doesnt work because the thread would just take the initial state of the bool and keep running
        self.x = 10 # shouldnt ever change but just putting it here
        self.y = 8
        # positive number when going downwards. dont ask why
        self.y_speed = -2  # slight jump when the game begins so you dont immediately die
        self.y_speed = -0.3  # slight jump when the game begins so you dont immediately die
        self.y_acceleration = 0.05

        """
        0 = classical flappy bird
        1 = wave
        """
        self.mode = mode
    
    def jump(self):
        if self.mode == 1:
            self.y_speed = -self.y_speed
        elif self.mode == 0:
            self.y_speed = -0.5
    
    def update(self):
        self.y += self.y_speed
        if self.mode == 0:
            self.y_speed += self.y_acceleration

class Scene:
    def __init__(self, mode) -> None:
        self.pipes = []
        self.last_pipe_generated = 0
        self.frame = 0
        self.matrix = [[0 for i in range(SCREENW)] for i in range(SCENE_HEIGHT)] # collision/hitboxes
        self.player = Player(mode)
        
        if mode == 0:
            self.ansi = "\033[31m"
        elif mode == 1:
            self.ansi = "\033[34m"
        
        self.objcode = {0: " ", 1: "#", 2: f"{self.ansi}>\033[0m"}
        self.score = 0
        self.player_coordinates = (self.player.y, self.player.x)
    
    def print(self, clear_screen=True):
        # clear_screen is for debugging purposes
        if clear_screen:
            print("\033[H")
        print("\r", end="")
        
        score = list(str(self.score))
        buffer = str()
        
        for row in self.matrix:
            for cell in row:
                if score:
                    buffer += score.pop(0)
                else:
                    buffer += self.objcode[cell]
            buffer += "\n\r"
        
        print(buffer, end="")
    
    def refresh(self, player_coordinates=None):
        global REFRESH_RATE
        
        if self.score >= 2:
            REFRESH_RATE = 0.05
        elif self.score >= 4:
            REFRESH_RATE = 0.01
        
        self.frame += 1
        self.pipes = list(filter(lambda a: a[0] >= 0, self.pipes)) # filter out pipes that are no longer on the screen
        
        # move all pipes to the left
        if not self.player.dead[0]:
            for idx, pipe in enumerate(self.pipes):
                self.pipes[idx][0] -= 1
        
        self.load_matrix(player_coordinates)
    
    def add_new_pipe(self):
        self.last_pipe_generated = self.frame
        self.pipes.append([SCREENW-2, random.randrange(PIPE_OPENING_SIZE, SCENE_HEIGHT - PIPE_OPENING_SIZE)])

    def load_matrix(self, player_coordinates=None):
        # loading the pipes
        queue = self.pipes[:]
        blank_matrix = [[0 for i in range(SCREENW)] for i in range(SCENE_HEIGHT)]
        while queue:
            px, py = queue.pop(0)
            
            # check for collision
            if self.player.x in range(px, px + 2) and (math.ceil(self.player.y) in range(py+PIPE_OPENING_SIZE, SCENE_HEIGHT) or math.ceil(self.player.y) in range(-100000, py)):
                self.die() # note to self: you can probably check for the precise cell in the matrix
            elif self.player.x == px + 2:
                self.score += 1

            for mx in range(px, px + 2):
                for my in range(0, py):
                    blank_matrix[my][mx] = 1
                
                for my in range(py+PIPE_OPENING_SIZE, SCENE_HEIGHT):
                    blank_matrix[my][mx] = 1
        
        self.matrix = blank_matrix
        self.player_coordinates = self.load_player(player_coordinates)
    
    def load_player(self, coords=None):
        # load the player
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):
                if cell == 2:
                    self.matrix[y][x] = 0
        
        if coords:
            py, px = coords
        else:
            py, px = math.ceil(self.player.y), self.player.x
        
        if 0<=py and SCENE_HEIGHT-1>py: # do not render the player if it is out of bounds, upwards
            self.matrix[py][px] = 2
        elif self.player.y > SCENE_HEIGHT + 5: # kill if player is 5 units below the scene bottom
            self.die()
            print(f"\nScore: {self.score}", end="\n\r")
            # since the main game loop doesnt detect player death, this is the only actual death condition within the game
            #print("\007", end="") # this character makes a strange noise
            raise SystemExit
        
        return py, px
    
    def die(self):
        self.player.dead[0] = True
        self.player.x -= 1
        self.player.y_acceleration = 0.1
        print("\rSUDDEN DEATH", end="\n\r")

last_refresh = time.time()
last_player_refresh = time.time()

if __name__ == "__main__":
    try:
        os.system("cls" if IS_WIN else "clear")
        # initing
        scene = Scene(MODE)
        scene.add_new_pipe()
        scene.refresh()
        scene.print()
        
        print("\rPRESS ANY KEY TO BEGIN (YOU SHOULD PROBABLY PRESS SPACE THOUGH)")
        
        if index(getch()) in (27, 3, 4):
            raise SystemExit # i have to stop using exceptions to hack together code lmao
        
        os.system("cls" if IS_WIN else "clear")

        # game loop
        thread = threading.Thread(target=process_keyboard_events, args=(event_queue, scene.player.dead))
        thread.daemon = True
        thread.start()

        while True:
            # refresh objects
            has_refreshed_player = False

            if event_queue:
                key = event_queue.pop(0)
                
                # process keyboard events
                
                if index(key) in (27, 3, 4): # press ESC, CTRL+C, or CTRL+D to exit
                    sys.stdout.flush()
                    break
                elif index(key) == 32:
                    scene.player.jump()

                sys.stdout.flush()
            
            if time.time() - last_player_refresh > PLAYER_REFRESH_RATE:
                last_player_refresh = time.time()
                scene.player.update()
                py, px = scene.player_coordinates
                scene.load_player() # load player separately now (so that pipes dont update)
                scene.print() # re-print scene
                has_refreshed_player = True
            
            if time.time() - last_refresh > REFRESH_RATE:
                last_refresh = time.time()
                   
                # new pipe every 20 units. later on, as the game progresses, the pipes will become more frequent
                if scene.frame - scene.last_pipe_generated >= 20:
                    scene.add_new_pipe()
                
                if has_refreshed_player:
                    scene.refresh(scene.player_coordinates)
                else:
                    scene.refresh()
                scene.print()
            
    # if i dont include the `except` clause the game will fail silently without showing the exeception`
    except Exception as e:
        raise e
    # so that the terminal doesnt stay fucked up when the player closes the game
    finally:
        reset_terminal()
