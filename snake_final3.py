import curses
import time
import random

d,íscjhfkscjhfcuksdcfk sdfkvf hsvk fhc


def amIDeadYet(snakeX,snakeY,maxCols,maxRows):
    """ Checks if the death conditions are true """
    # if snakeX[0] >= maxCols-1 or snakeX[0] <= 0:
    #     return True
    #
    # elif snakeY[0] >= maxRows-1 or snakeY[0] <=0:
    #     return True

    for i in range(len(snakeX)-1):
        if snakeX[0] == snakeX[i+1] and snakeY[0] == snakeY[i+1]:
            return True

    return False

def moveTheSnake(snakeX,snakeY,direction):
    """ Calculates and returns the next X and Y position for each snake part """
    global foodY
    global foodX

    tempX = snakeX[0]
    tempY = snakeY[0]
    snakeX = shiftRight(snakeX)
    snakeY = shiftRight(snakeY)

    if direction == "down":
        snakeY[0] = tempY + 1
        snakeX[0] = tempX
    elif direction == "up":
        snakeY[0] = tempY - 1
        snakeX[0] = tempX
    elif direction == "right":
        snakeX[0] = tempX + 1
        snakeY[0] = tempY
    elif direction == "left":
        snakeX[0] = tempX - 1
        snakeY[0] = tempY

    if snakeY[0] == foodY and snakeX[0] == foodX:
        foodY = random.randint(2,maxRows-2)
        foodX = random.randint(2,maxCols-2)
        snakeX.insert(1,tempX)
        snakeY.insert(1,tempY)

    #right wall
    if snakeX[0] == maxCols-1:
        snakeX[0] = 1
    #left wall
    elif snakeX[0] == 1:
        snakeX[0] = maxCols-2
    #upper wall
    elif snakeY[0] == 1:
        snakeY[0] = maxRows-2
    #bottom wall
    elif snakeY[0] == maxRows-1:
        snakeY[0] = 1

    for i in range(len(snakeX)):
       if foodX == snakeX[i] and foodY == snakeY[i]:
               foodY = random.randint(2,maxRows-2)
               foodX = random.randint(2,maxCols-2)

    return snakeX, snakeY, direction

def drawGameField():
    """ Draws the static parts of the game field and the scoreboard"""
    screen.timeout(200)
    screen.border(0)
    box1 = curses.newwin(2, 2, 0, 0)
    box1.immedok(True) # Automatically refreshes the box if window size is changed
    screen.addstr(1,1,"SCORE:" + str(len(snakeX) - 4))
    pressq = "Presss 'q' to quit"
    screen.addstr(maxRows-2, maxCols-2-len(pressq),pressq)
    title = "Snake Ultimate"
    screen.addstr(0,int((maxCols - len(title)) / 2), title)

def drawSnake(snakeY,snakeX):
    """ Draws all segments of the snake at given coordinates and in color"""

    for i in range(len(snakeX)):
        if i == 0:
            screen.addstr(snakeY[i], snakeX[i],"█",curses.color_pair(1))
        else:
            screen.addstr(snakeY[i], snakeX[i],"█",curses.color_pair(2))

def drawFood(y,x):
    """ Draws the food at given coordinates"""
    screen.addstr(y,x,"⦁")

def shiftRight(l):
    """ Takes a list as an input and shifts every element to the right"""
    return l[-1:] + l[:-1]

def death():
    """ Handles events if the game is over """
    screen.erase()
    #screen.addstr("GAME OVER")
    curses.endwin()
    exit()

def gameOver():
    counter=1
    with open('gameOver.txt') as f:
        for line in f:
            screen.addstr(counter, 17,line)
            counter += 1

    screen.addstr(15,28, "Do you want to try again?")
    screen.addstr(17,38, "Y / N")

def drawStartingScreen():
    counter=1
    with open('startingscreen.txt') as f:
        for line in f:
            screen.addstr(counter,int((maxCols - len(line)) / 2),line)
            counter += 1
    pressSpace = "Press 'Space' to continue..."
    screen.addstr(17,int((maxCols - len(pressSpace)) / 2), pressSpace)



#-------------------Initialisation starts--------------------

# Curses module initialisation
screen = curses.initscr()
maxRows, maxCols = screen.getmaxyx()
curses.noecho()
curses.curs_set(0)
screen.keypad(1)
screen.nodelay(1)
curses.start_color()

stage = "StartingScreen"



# Used color pairs initialisation
curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

# Starting position of the food
foodY = random.randint(2,maxRows-2)
foodX = random.randint(2,maxCols-2)

# X and Y coordinates of the starting position of the snake
snakeX = [20,19,18,17]
snakeY = [20,20,20,20]

# Starting direction of the snake
direction = "right"

# Speed of the game
gameSpeed = 0.1 # it must be greater than 0, the lower the value, the faster the game
#--------------------Initialisation ends---------------------


#---------------------Main loop starts-----------------------
while True:
    screen.erase()
    # gameOver()
    # drawGameField()
    # drawFood(foodY,foodX)
    # (snakeX, snakeY, direction) = moveTheSnake(snakeX,snakeY,direction)
    # drawSnake(snakeY,snakeX)
    drawStartingScreen()


    if amIDeadYet(snakeX,snakeY,maxCols,maxRows): death()

    event = screen.getch()
    if event == ord("q"): break
    elif event == curses.KEY_UP and direction != "down":
        direction = "up"
    elif event == curses.KEY_DOWN and direction != "up":
        direction = "down"
    elif event == curses.KEY_LEFT and direction != "right":
        direction = "left"
    elif event == curses.KEY_RIGHT and direction != "left":
        direction = "right"

    elif event == chr(36) and stage == "StartingScreen":
        stage = "MainMenu"



curses.endwin()

#---------------------Main loop ends-------------------------