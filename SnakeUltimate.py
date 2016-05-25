import curses
import time
import random


def zero_stage(snake_x=[], snake_y=[], direction=""):
    """ Starting stage of the snake """
    snake_x = [20, 19, 18, 17]
    snake_y = [20, 20, 20, 20]
    direction = "right"
    return (snake_x, snake_y, direction)


def am_i_dead_yet(snake_x, snake_y, max_cols, max_rows):
    """ Checks if the death conditions are true """
    for i in range(len(snake_x) - 1):
        if snake_x[0] == snake_x[i + 1] and snake_y[0] == snake_y[i + 1]:
            return True

    return False


def move_the_snake(snake_x, snake_y, direction, food_type, head_color, body_color):
    """ Calculates and returns the next X and Y position for each snake part"""
    global food_y
    global food_x
    global score

    temp_x = snake_x[0]
    temp_y = snake_y[0]
    snake_x = shift_right(snake_x)
    snake_y = shift_right(snake_y)

    if direction == "down":
        snake_y[0] = temp_y + 1
        snake_x[0] = temp_x
    elif direction == "up":
        snake_y[0] = temp_y - 1
        snake_x[0] = temp_x
    elif direction == "right":
        snake_x[0] = temp_x + 1
        snake_y[0] = temp_y
    elif direction == "left":
        snake_x[0] = temp_x - 1
        snake_y[0] = temp_y

    if snake_y[0] == food_y and snake_x[0] == food_x:
        food_y = random.randint(2, max_rows - 3)
        food_x = random.randint(2, max_cols - 3)
        snake_x.insert(1, temp_x)
        snake_y.insert(1, temp_y)
        head_color = random.randint(1, 5)
        if head_color == 5:
            body_color = 1
        else:
            body_color = head_color + 1
        if food_type == 5:
            score += 5
        else:
            score += 1
        food_type = random.randint(1, 5)

    # right wall
    if snake_x[0] == max_cols - 2:
        snake_x[0] = 1
    # left wall
    elif snake_x[0] == 0:
        snake_x[0] = max_cols - 3
    # upper wall
    elif snake_y[0] == 0:
        snake_y[0] = max_rows - 3
    # bottom wall
    elif snake_y[0] == max_rows - 2:
        snake_y[0] = 1

    for i in range(len(snake_x)):
        if food_x == snake_x[i] and food_y == snake_y[i]:

            food_y = random.randint(2, max_rows - 2)
            food_x = random.randint(2, max_cols - 2)

    return snake_x, snake_y, direction, food_type, head_color, body_color


def draw_game_field():
    """ Draws the static parts of the game field and the scoreboard"""
    if score // 12 == 0:
        game_speed = 200
    elif score // 12 == 1:
        game_speed = 150
    elif score // 12 == 2:
        game_speed = 100
    elif score // 12 >= 3:
        game_speed = 75

    screen.timeout(game_speed)
    # screen.border(0)
    # box1 = curses.newwin(2, 2, 0, 0)
    # Automatically refreshes the box if window size is changed
    # box1.immedok(True)
    counter = 0
    with open('map.txt') as f:
        for line in f:
            screen.addstr(counter, 0, line)
            counter += 1
    screen.addstr(1, 1, "SCORE:" + str(score))
    pressq = "Press 'q' to quit"
    screen.addstr(max_rows - 2, max_cols - 2 - len(pressq), pressq)
    title = "SnakeUltimate"
    screen.addstr(0, int((max_cols - len(title)) / 2), title)


def draw_snake(snake_y, snake_x, head_color, body_color):
    """ Draws all segments of the snake at given coordinates and in color"""
    for i in range(len(snake_x)):
        if i == 0:
            screen.addstr(snake_y[i], snake_x[i], "█", curses.color_pair(head_color))
        else:
            screen.addstr(snake_y[i], snake_x[i], "█", curses.color_pair(body_color))


def draw_food(y, x, draw_this, color):
    """ Draws the food at given coordinates"""
    screen.addstr(y, x, draw_this, color)


def shift_right(l):
    """ Takes a list as an input and shifts every element to the right"""
    return l[-1:] + l[:-1]


def game_over(score):
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

    for i in range(10):
        if i >= len(names):
            break
        screen.addstr(5 + i, 28, str(i + 1) +
                      ".: " + names[i] + " " + scores[i])
        if names[i] == user_name:
            screen.addstr(5 + i, 28, str(i + 1) + ".: " +
                          names[i] + " " +
                          scores[i], curses.color_pair(2))

    screen.addstr(22, 24, "Press 'SPACE' to try again!")
    screen.addstr(23, 24, "Press 'q' to quit!")
    if screen.getch() == ord("q"):
        curses.endwin()
        quit()
    f.close()


# -------------------Initialisation starts--------------------

# Curses module initialisation
screen = curses.initscr()
max_rows, max_cols = 24, 80
curses.noecho()
curses.curs_set(0)
screen.keypad(1)
screen.nodelay(1)
curses.start_color()
stage = "Game"
score = 0

# Used color pairs initialisation
curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLACK)
head_color = 2
body_color = 3


# Starting position of the food
food_y = random.randint(2, max_rows - 3)
food_x = random.randint(2, max_cols - 3)
food_type = 5

# X and Y coordinates of the starting position and direction of the snake
snake_x, snake_y, direction = zero_stage()

# Speed of the game
game_speed = 0.1  # the lower the value, the faster the game, but must be > 0
# --------------------Initialisation ends---------------------


# ---------------------Main loop starts-----------------------
while True:
    screen.erase()

    if stage == "Game":
        draw_game_field()

        if food_type == 5:
            draw_food(food_y, food_x, "✯", curses.color_pair(3))
        else:
            draw_food(food_y, food_x, "⦁", curses.color_pair(5))

        (snake_x, snake_y, direction, food_type, head_color, body_color) = move_the_snake(snake_x, snake_y, direction, food_type, head_color, body_color)
        draw_snake(snake_y, snake_x, head_color, body_color)

        if am_i_dead_yet(snake_x, snake_y, max_cols, max_rows):
            stage = "game_over"

    elif stage == "game_over":
        game_over(score)
        stage = "Game"
        snake_x, snake_y, direction = zero_stage(snake_x, snake_y, direction)
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
