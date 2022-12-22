# A CLI game
~~Flappy~~ Floppy bird in CLI  

Note: due to limitations with the code author's intelligence, you won't be able to resize the terminal once you're in the game. Rip, bozo!  

Credit to earthtraveller1 for contributing one line of code (more specifically, line 74 of main.py) along with a pull request that fixed a lethal error which previously affected 71% of the userbase, we will forever remember him as a hero for that

## How to Play

**Step 1.** Install [Python](https://python.org) if you haven't already. Make sure that it and everything that it includes is added to `PATH`.

**Step 2.** Clone this repository. 

**Step 3.** Install the requirements for this project by running `pip install -r requirements.txt` in this repository's root directory. On Windows platforms you may have to to run `python3 -m pip install -r requirements.txt` for it to work, depending on your installation of Python.

**Step 4.** Run the game by running `python3 main.py`. On some platforms it may be `python main.py`. Make sure that the Python version is 3, though.

## FAQ  

Q: What is this?  
A: A Python cli game.  
Q: About what?  
A: I don't know.  
Q: Why is this game so horrible?  
A: Sorry, I have to go now. See you later.  
Q: Okay, bye.  

## Known Problems
- You can actually go under the pipes and not die (since you only die when you go 5 units below the bottom of the screen)  
- When you are on Mode 1 and die, if you are flying upwards you will fly upwards forever and the program will never exit. However, you can still Ctrl+C.  
