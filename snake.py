from tkinter import *
import random

#GAME_WIDTH = 1300 orignal settings
#GAME_HEIGHT = 550
GAME_WIDTH = 500 #highscore: 96
GAME_HEIGHT = 500 #MAXscore: 97
SPEED = 75 #250 orignal speed 75 javascript
SPACE_SIZE = 25 #50 oringal size
BODY_PARTS = 5 #3 orignal parts
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#808080" #"#000000" black
WINNING_NUMBER = 100
paused = False  # Flag to pause the animation

#photo = PhotoImage("C:/Users/13238/Pictures/Saved Pictures/smile.png")

class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)
        #if not paused:
        #    window.after(SPEED, Snake)


class Food:

    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, outline=FOOD_COLOR, tag="food") #oval
        #canvas.create_image(x, y, x + SPACE_SIZE, y + SPACE_SIZE,image=photo, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]
    
    if score >= WINNING_NUMBER:
        you_win()

    elif check_collisions(snake):
        game_over()
    
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def reset():
    global score
    score = 0
    label.config(text="Score:{}".format(score), font=('consolas', 40))

    global direction

    canvas.delete(ALL)
    
    direction = 'down'
    
    snake = Snake()
    food = Food()
    
    next_turn(snake, food)
    
    #button1.pack_forget()
    button1.place_forget()


def pause_animation(event):
    global paused, direction
    paused = not paused
    if not paused:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

def play():
    global direction
    Snake(change_direction)


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       text="GAME OVER", font=('consolas', 70), fill="red", tag="gameover")
    print("your score:", score)
    #button1.pack(anchor=NE) #side=RIGHT)
    button1.place(x=404.5, y=0)

def you_win():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       text="YOU WIN", font=('consolas', 70), fill="green", tag="youwin")
    print("the max score was:", score,"\nTHANKS FOR PLAYING :)")
    #button1.pack(anchor=NE) #side=RIGHT)
    button1.place(x=404.5, y=0)



window = Tk()
window.title("Snake game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, background="#656565", text="Score:{}".format(score), font=('consolas', 40), fg="#FFFFFF")
label.pack(side=TOP)

button = Button(window, text="Exit", font=('consolas', 20), background="#bebfa1", command=window.destroy)
#button.pack(anchor=NW) #side=LEFT)
button.place(x=1, y=0)

button1 = Button(window, text="Reset", font=('consolas', 20), background="#bebfa1", command=reset)#bebfa1
#button1.pack(side=RIGHT)
#button1.place(x=404.5, y=0)

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack(side=BOTTOM)

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")
#window.attributes('-fullscreen',True)
window.config(background="#656565")#"#f9fade" orignal

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
#window.bind("p", pause_animation)

snake = Snake()
food = Food()

next_turn(snake, food)
 
window.mainloop()
