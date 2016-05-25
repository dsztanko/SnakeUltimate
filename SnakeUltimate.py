import curses
import time
import random


def zeroStage(snakeX=[], snakeY=[], direction=""):
    """ Starting stage of the snake """
    snakeX = [20, 19, 18, 17, 16, 15]
    snakeY = [20, 20, 20, 20, 20, 20]
    direction = "right"
    return (snakeX, snakeY, direction)


def amIDeadYet(snakeX, snakeY, maxCols, maxRows):
    """ Checks if the death conditions are true """
    for i in range(len(snakeX) - 1):
        if snakeX[0] == snakeX[i + 1] and snakeY[0] == snakeY[i + 1]:
            return True

    return False


def moveTheSnake(snakeX, snakeY, direction):
    """ Calculates and returns the next X and Y position for each snake part"""
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
        foodY = random.randint(2, maxRows - 2)
        foodX = random.randint(2, maxCols - 2)
        snakeX.insert(1, tempX)
        snakeY.insert(1, tempY)

    # right wall
    if snakeX[0] == maxCols - 1:
        snakeX[0] = 1
    # left wall
    elif snakeX[0] == 1:
        snakeX[0] = maxCols - 2
    # upper wall
    elif snakeY[0] == 1:
        snakeY[0] = maxRows - 2
    # bottom wall
    elif snakeY[0] == maxRows - 1:
        snakeY[0] = 1

    for i in range(len(snakeX)):
        if foodX == snakeX[i] and foodY == snakeY[i]:
            foodY = random.randint(2, maxRows - 2)
            foodX = random.randint(2, maxCols - 2)

    return snakeX, snakeY, direction


def drawGameField():
    """ Draws the static parts of the game field and the scoreboard"""
    if (len(snakeX) - 4) // 6 == 0:
        gameSpeed = 200
    elif (len(snakeX) - 4) // 6 == 1:
        gameSpeed = 150
    elif (len(snakeX) - 4) // 6 == 2:
        gameSpeed = 100
    elif (len(snakeX) - 4) // 6 >= 3:
        gameSpeed = 50

    screen.timeout(gameSpeed)
    screen.border(0)
    box1 = curses.newwin(2, 2, 0, 0)
    # Automatically refreshes the box if window size is changed
    box1.immedok(True)
    screen.addstr(1, 1, "SCORE:" + str(len(snakeX) - 4))
    pressq = "Presss 'q' to quit"
    screen.addstr(maxRows - 2, maxCols - 2 - len(pressq), pressq)
    title = "SnakeUltimate"
    screen.addstr(0, int((maxCols - len(title)) / 2), title)


def drawSnake(snakeY, snakeX):
    """ Draws all segments of the snake at given coordinates and in color"""
    for i in range(len(snakeX)):
        if i == 0:
            screen.addstr(snakeY[i], snakeX[i], "█", curses.color_pair(1))
        else:
            screen.addstr(snakeY[i], snakeX[i], "█", curses.color_pair(2))


def drawFood(y, x):
    """ Draws the food at given coordinates"""
    screen.addstr(y, x, "⦁")


def shiftRight(l):
    """ Takes a list as an input and shifts every element to the right"""
    return l[-1:] + l[:-1]


def gameOver(score):
    """ Game over text at the end """
    user_name = ""
    pressed_enter = False
    while True:
        screen.addstr(15, 28, "You've reached {0} score.".format(score))
        screen.addstr(17, 10, "Enter your name to become a member of the SnakeUltimate family: ")
        counter = 1
        with open('gameOver.txt') as f:
            for line in f:
                screen.addstr(counter, 18, line)
                counter += 1
        screen.nodelay(0)
        letter = str(chr(int(screen.getch())))
        if pressed_enter:
            read_high_score(user_name)
            if screen.getch() == ord(" "):
                break
        else:
            if letter != "ć":
                user_name = user_name + letter
            else:
                if len(user_name) > 0:
                    user_name = user_name[:-1]

            if len(user_name) >= 15:
                user_name = user_name[:14]
            if len(user_name) > 1:
                if user_name[-1] == "\n":
                    user_name = user_name[:-1]
                    write_high_score(user_name, score)
                    pressed_enter = True
            screen.erase()
            screen.addstr(19, 28, user_name)


def sorting_method(list1, list2):
    """ Orders list1 and list2 based on values in list1 """
    new_list1 = []
    new_list2 = []
    for i in range(len(list1)):
        order = list1.index(max(list1))
        new_list1.append(list1[order])
        new_list2.append(list2[order])
        list1.remove(list1[order])
        list2.remove(list2[order])

    return new_list1, new_list2


def write_high_score(user_name, score):
    """ Writes the user name and the highscore into the highscore.txt file """
    f = open("highscore.txt", "a")
    f.write(user_name + ", " + str(score) + "\n")
    f.close()


def read_high_score(user_name):
    """ Reads in the highscore table from the highscore.txt file """
    f = open("highscore.txt")
    screen.erase()
    scores_list = f.readlines()
    names = []
    scores = []
    for item in scores_list:
        (x, y) = item.split(", ")
        names.append(x.replace("\n", ""))
        scores.append(y.replace("\n", ""))
    scores, names = sorting_method(scores, names)
    f.close()

    screen.addstr(2, 24, "HIGHSCORE")
    counter = 0
    for row in scores_list:
        screen.addstr(5 + counter, 28, str(counter + 1) + ".: " + names[counter] + " " + scores[counter])
        if names[counter] == user_name:
            screen.addstr(5 + counter, 28, str(counter + 1) + ".: " + names[counter] + " " + scores[counter], curses.color_pair(2))
        counter += 1

    screen.addstr(5 + counter + 2, 24, "Press 'SPACE' to try again!")
    f.close()


# -------------------Initialisation starts--------------------

# Curses module initialisation
screen = curses.initscr()
maxRows, maxCols = screen.getmaxyx()
curses.noecho()
curses.curs_set(0)
screen.keypad(1)
screen.nodelay(1)
curses.start_color()
stage = "Game"

# Used color pairs initialisation
curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

# Starting position of the food
foodY = random.randint(2, maxRows - 2)
foodX = random.randint(2, maxCols - 2)

# X and Y coordinates of the starting position and direction of the snake
snakeX, snakeY, direction = zeroStage()

# Speed of the game
gameSpeed = 0.1  # the lower the value, the faster the game, but must be > 0
# --------------------Initialisation ends---------------------


# ---------------------Main loop starts-----------------------
while True:
    screen.erase()

    if stage == "Game":
        drawGameField()
        drawFood(foodY, foodX)
        (snakeX, snakeY, direction) = moveTheSnake(snakeX, snakeY, direction)
        drawSnake(snakeY, snakeX)
        # stage = "GameOver" # EZT SZEGGYED KIIIIIIII!!!!!

        if amIDeadYet(snakeX, snakeY, maxCols, maxRows):
            stage = "GameOver"

    elif stage == "GameOver":
        gameOver(len(snakeX)-4)
        stage = "Game"
        snakeX, snakeY, direction = zeroStage(snakeX, snakeY, direction)
        screen.timeout(1)

    event = screen.getch()

    if event == ord("q"):
        break
    elif event == curses.KEY_UP and direction != "down":
        direction = "up"
    elif event == curses.KEY_DOWN and direction != "up":
        direction = "down"
    elif event == curses.KEY_LEFT and direction != "right":
        direction = "left"
    elif event == curses.KEY_RIGHT and direction != "left":
        direction = "right"


curses.endwin()
# ---------------------Main loop ends-------------------------
