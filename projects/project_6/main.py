import turtle
import random

# Set up the screen
wn = turtle.Screen()
wn.title("Breakout Game")
wn.bgcolor("black")
wn.setup(width=1000, height=800)
wn.tracer(0)  # Turn off screen updates

# Paddle
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=0.75, stretch_len=10)
paddle.penup()
paddle.goto(0, -350)

paddle.move_left = False
paddle.move_right = False

# Ball
ball = turtle.Turtle()
ball.speed(40)
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = random.randint(-4,4)
ball.dy = -4


# Define the Block class
class Block(turtle.Turtle):
    def __init__(self, color, x, y, size, padding):
        super().__init__()
        self.speed(0)
        self.shape("square")
        self.color(color)
        self.shapesize(stretch_wid=(size + 2*padding)/25, stretch_len=(size + 2*padding)/25)  # Adjust the size as needed
        self.penup()
        self.goto(x, y)


# Create a list to store the blocks
blocks = []
lives = 3

block_size = 25
padding = 5

speed_multiplier = 1.0

# Create a lives display Turtle
lives_display = turtle.Turtle()
lives_display.speed(0)
lives_display.color("white")
lives_display.penup()
lives_display.hideturtle()
lives_display.goto(-480, 365)  # Adjust the position as needed

score = 0

score_display = turtle.Turtle()
score_display.speed(0)
score_display.color("white")
score_display.penup()
score_display.hideturtle()
score_display.goto(480, 365)  # Adjust the position as needed
score_display.write("Score: " + str(score), align="right", font=("Courier", 24, "normal"))

# Create a game over display Turtle
game_over_display = turtle.Turtle()
game_over_display.speed(0)
game_over_display.color("white")
game_over_display.penup()
game_over_display.hideturtle()
game_over_display.goto(0, -100)


# Function to display "GAME OVER"
def show_game_over():
    game_over_display.clear()
    game_over_display.write(f"GAME OVER\nScore: {score}", align="center", font=("Courier", 48, "bold"))


# Function to update the lives display
def update_lives_display():
    lives_display.clear()
    lives_display.write("Lives: " + str(lives), align="left", font=("Courier", 24, "normal"))


update_lives_display()


# Function to update the score display
def update_score_display():
    score_display.clear()
    score_display.write("Score: " + str(score), align="right", font=("Courier", 24, "normal"))


update_score_display()


# Function to create blocks
def create_blocks():
    colors = ["red", "#D5202C", "#E23C47", "#E75F68", "#EC838A", "blue", "#3370FF", "#5C8DFF", "#85A9FF", "#ADC6FF"]  # Customize the colors
    rows = 10
    columns = 28

    start_x = -480  # Adjust the starting x-coordinate
    start_y = 380  # Adjust the starting y-coordinate

    for row in range(rows):
        for col in range(columns):
            if row % 5 == 0 or col % 7 == 0:
                continue

            color = colors[row % len(colors)]
            x = start_x + col * (block_size + 2 * padding)
            y = start_y - row * (block_size + 2 * padding)
            new_block = Block(color, x, y, block_size, padding)
            blocks.append(new_block)


# Call the function to create blocks
create_blocks()


def paddle_right_start():
    paddle.move_right = True


def paddle_right_end():
    paddle.move_right = False


def paddle_left_start():
    paddle.move_left = True


def paddle_left_end():
    paddle.move_left = False


# Keyboard bindings
wn.listen()

wn.onkeypress(paddle_right_start, "Right")
wn.onkeyrelease(paddle_right_end, "Right")

wn.onkeypress(paddle_left_start, "Left")
wn.onkeyrelease(paddle_left_end, "Left")


# Check for collision between ball and paddle
def is_collision_paddle(ball, paddle):
    ball_x, ball_y = ball.pos()
    paddle_x, paddle_y = paddle.pos()
    return (paddle_y - 10 <= ball_y <= paddle_y) and (paddle_x - 100 <= ball_x <= paddle_x + 100)


# Function to handle ball reset
def reset_ball():
    ball.goto(0, 0)
    ball.dx = random.randint(-4,4)
    ball.dy = -4


# Main game loop
while lives > 0 and score != 1920:
    if paddle.move_right:
        x = paddle.xcor()
        x += 10
        if x < 450:
            paddle.setx(x)

    if paddle.move_left:
        x = paddle.xcor()
        x -= 10
        if x > -450:
            paddle.setx(x)

    wn.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Border checking
    if ball.xcor() > 490:
        ball.setx(490)
        ball.dx *= -1

    if ball.xcor() < -490:
        ball.setx(-490)
        ball.dx *= -1

    if ball.ycor() > 390:
        ball.sety(390)
        ball.dy *= -1

    if ball.ycor() < -390:
        lives -= 1
        update_lives_display()
        if lives > 0 and score != 1920:
            reset_ball()
            speed_multiplier = 1.0
        elif lives == 0 or score == 1920:
            show_game_over()

    # Check for collisions between ball and blocks
    for block in blocks:
        if (ball.ycor() + 10 >= block.ycor() - 12.5 and
                ball.ycor() - 10 <= block.ycor() + 12.5 and
                ball.xcor() + 10 >= block.xcor() - 12.5 and
                ball.xcor() - 10 <= block.xcor() + 12.5):

            if ball.xcor() < block.xcor() - 12.5 or ball.xcor() > block.xcor() + 12.5:
                ball.dx *= -1
            else:
                ball.dy *= -1

            score += 10
            update_score_display()
            block.goto(1000, 1000)  # Move the block off-screen

    # Check for collision between ball and paddle
    if is_collision_paddle(ball, paddle):
        ball.sety(paddle.ycor() + 10)  # Adjust the ball's position to avoid sticking
        speed_multiplier += 0.002
        ball.dy *= -1 * speed_multiplier
        if paddle.xcor() - 100 <= ball.xcor() <= paddle.xcor() - 70:
            ball.dx = -6
            print("Left Left side of the paddle")
        elif paddle.xcor() - 70 <= ball.xcor() <= paddle.xcor() - 40:
            print("Left side of the paddle")
            ball.dx = -4
        elif paddle.xcor() + 40 <= ball.xcor() <= paddle.xcor() + 70:
            print("Right side of the paddle")
            ball.dx = 4
        elif paddle.xcor() + 70 <= ball.xcor() <= paddle.xcor() + 100:
            print("Right Right side of the paddle")
            ball.dx = 6
        else:
            pass


# Close the window
wn.mainloop()