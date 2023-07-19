import turtle
import time
import random
from tkinter import messagebox, simpledialog
import os
import csv
import winsound

window = turtle.Screen()
window.title("Ping-Pong by bot.py")
window.bgcolor("black")
window.setup(width=800, height=600)
window.tracer(0) #delays drawing update on canvas 

xVelocity = 3.40
yVelocity = 2.40

player_data_file = os.path.join(os.path.expanduser("~"), "Downloads", "player_data.csv")
power = None
player_a_name = simpledialog.askstring("Name?", "please enter a player name if you have one: ")
player_b_name = "AI"
player_a_score = player_b_score = 0

def difficulty_level():
    levels = ["beginner", "pro", "legend"]
    difficulty = simpledialog.askstring("Difficulty?", "Choose a difficulty level (beginner/pro/legend): ")
    while difficulty.lower() not in levels:
            difficulty = simpledialog.askstring("Difficulty?", "Choose a difficulty level (beginner/pro/legend): ")
    return difficulty.lower()

difficulty = difficulty_level()

winsound.PlaySound("C:\\Users\\Daniel-Panovest\\Downloads\\gamesound.wav", winsound.SND_ASYNC)
start_time = time.time()
player_data = []

def write_player_data(player_data_file):
    with open(player_data_file, "a", newline="") as file:
       csv_writer = csv.DictWriter(file, fieldnames= ["Player Name", "Difficulty"])

       if file.tell() == 0:
        csv_writer.writeheader()
       csv_writer.writerow({"Player Name": player_a_name, "Difficulty": difficulty})

def read_player_data():
    global player_a_name, difficulty, player_data, player_data_file

    #if not handles the absence of any player data file
    if not os.path.isfile(player_data_file):
        messagebox.showerror("File Not Found", "Player Data Missing!")
        player_data_file = os.path.join(os.path.expanduser("~"), "Downloads", "player_data.csv")
        player_a_name = simpledialog.askstring("Name?", "please enter a player name if you have one: ")
        difficulty = difficulty_level()
        player_data.append({"Player Name": player_a_name, "Difficulty": difficulty})
        return
    
    with open(player_data_file, "r") as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            player_data.append({"Player Name": row["Player Name"], "Difficulty": row["Difficulty"]})

def new_player():
    newplayer = messagebox.askyesno("New Player?", "new (Yes) or same player? (No)")
    return newplayer

def reset_game():
    if not new_game():
        window.bye()

class Paddle(turtle.Turtle): #passing a turtle.Turtle object as a superclass
    def __init__(self,x,y):
        super().__init__() #ensures the paddle object inherits turtle.Turtle's attributes
        self.shape("square")
        self.shapesize(stretch_wid=5, stretch_len=1)
        self.color("white")
        self.penup()
        self.speed(0)
        self.goto(x,y)
   
    def paddle_up(self):
        self.sety(self.ycor() + 10)
        
    def paddle_down(self):
        self.sety(self.ycor() - 10)
    
    #ai paddle using ball's ycor to determine movement / #the ai paddle responds accurately when random.random returns a value within higher random levels
    def ai_paddle(self, ball, difficulty):
        
        if difficulty == "beginner":
            threshold = 0.1
        elif difficulty == "pro":
            threshold = 0.3
        elif difficulty == "legend":
            threshold = 0.5

        if random.random() < threshold:
            if self.ycor() < ball.ycor():
                self.paddle_up()
            else:
                self.paddle_down()

    def check_border(self):
        if self.ycor() > 248:
            self.sety(248)
        elif self.ycor() < -248:
            self.sety(-248)
     
class Ball(turtle.Turtle):
    def __init__(self,x,y):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup() 
        self.speed(0)
        self.goto(x,y)

    def move_ball(self): #weight of 0.1 for smoother movement
        self.setx(self.xcor() + 0.1 * xVelocity)
        self.sety(self.ycor() + 0.1 * yVelocity)

    def border_checking(self):
        global xVelocity, yVelocity, player_a_score, player_b_score

        #right positive border
        if self.xcor() > 390:
            self.setx(390)
            xVelocity *= -1 #multiplying to derive a negative velocity
            player_a_score += 1
            winsound.PlaySound("C:\\Users\\Daniel-Panovest\\Downloads\\score.wav", winsound.SND_ASYNC)
            score.clear()
            score.write(f"{player_a_name}:{player_a_score} | {player_b_name}:{player_b_score}", align="center", font=("Consolas", 15, "normal"))
            self.color("white")

        #left negative border
        if self.xcor() < -390: 
            self.setx(-390)
            xVelocity *= -1
            player_b_score += 1
            winsound.PlaySound("C:\\Users\\Daniel-Panovest\\Downloads\\score.wav", winsound.SND_ASYNC)
            score.clear()
            score.write(f"{player_a_name}:{player_a_score} | {player_b_name}:{player_b_score}", align="center", font=("Consolas", 15, "normal"))
            self.color("white")

        #top border
        if self.ycor() > 290:
            self.sety(290)
            yVelocity *= -1

        #lower border
        if self.ycor() < -290:
            self.sety(-290)
            yVelocity *= -1
        
    def collisions(self):
        global xVelocity, power

        if self.color()[0] == "red":
            return
        
        #center, upper and lower paddle collisions with the ball
        if (350 > self.xcor() > 340) and (paddle_b.ycor() + 40 > self.ycor() > paddle_b.ycor() - 40):
            self.setx(340)
            xVelocity *= -1
            winsound.PlaySound("C:\\Users\\Daniel-Panovest\\Downloads\\paddleballcol.wav", winsound.SND_ASYNC)

        
        elif (-350 < self.xcor() < -340) and (paddle_a.ycor() - 40 < self.ycor() < paddle_a.ycor() + 40):
            self.setx(-340)
            xVelocity *= -1
            winsound.PlaySound("C:\\Users\\Daniel-Panovest\\Downloads\\paddleballcol.wav", winsound.SND_ASYNC)

        if power is not None and self.distance(power) <= 20:
            global yVelocity
            winsound.PlaySound("C:\\Users\\Daniel-Panovest\\Downloads\\powerballcol.wav", winsound.SND_ASYNC)
            power.hideturtle()
            self.color("red")
            power = None
            xVelocity *= -1
            yVelocity *= -1
            return

class Score(turtle.Turtle):
    def __init__(self,x,y):
        super().__init__()
        self.color("white")
        self.penup()
        self.speed(0)
        self.goto(x,y)
        self.hideturtle()
        self.write(f"{player_a_name}:{player_a_score} | {player_b_name}:{player_b_score}", align="center", font=("Consolas", 15, "normal"))

class Display(turtle.Turtle):
    def __init__(self,x,y):
        super().__init__()
        self.color("white")
        self.penup()
        self.speed(0)
        self.goto(x,y)
        self.hideturtle()
        self.write("Press 's' to start\nQuit: q | Move Up: ↑ | Move Down: ↓\nAvoid the power up ball :D", align="center", font=("Consolas", 15, "normal"))

class Winner(turtle.Turtle):
    def __init__(self,x,y):
        super().__init__()
        self.color("white") 
        self.penup()
        self.speed(0)
        self.goto(x,y)
        self.hideturtle()

class Powerup(turtle.Turtle):
    def __init__(self,x,y):
        super().__init__()
        self.shape("circle")
        self.color("red")
        self.penup()
        self.speed(0)
        self.goto(x,y)
        self.hideturtle()

    def show_powerup(self):
        self.showturtle()

    def hide_powerup(self):
        self.hideturtle()

def game_over():
    global winner, xVelocity, yVelocity
    if player_a_score == 10:
        winsound.PlaySound("C:\\Users\\Daniel-Panovest\\Downloads\\playerawins.wav", winsound.SND_ASYNC)
        winner.write(f"{player_a_name} wins!👏🏽", align="center", font=("Consolas", 14, "normal"))
        window.update()
        time.sleep(1.1)
        winner.clear()
        return True
       
    elif player_b_score == 10:
        winsound.PlaySound("C:\\Users\\Daniel-Panovest\\Downloads\\playerbwins.wav", winsound.SND_ASYNC)
        winner.write(f"{player_b_name} wins!👏🏽", align="center", font=("Consolas", 14, "normal"))
        window.update()
        time.sleep(1.1)
        winner.clear()
        return True
    else:
        return False
    
def new_game():
    global player_a_name, player_data_file, player_data, display, paddle_a, paddle_b, player_a_score, player_b_score, power, start_time, xVelocity, yVelocity

    response = messagebox.askyesno("New Game", "Play Again?")
    if response:
        newplayer = new_player()
        if newplayer:
            player_a_name = simpledialog.askstring("Name?", "please enter a player name if you have one: ")
            difficulty = difficulty_level()
            display.write("Press 's' to start\nQuit: q | Move Up: ↑ | Move Down: ↓\nAvoid the power up ball :D", align="center", font=("Consolas", 15, "normal"))
            winsound.PlaySound("C:\\Users\\Daniel-Panovest\\Downloads\\gamesound.wav", winsound.SND_ASYNC)
            
            window.listen()
            window.onkeypress(start_game, "s")
        else:
            change_difficulty = messagebox.askyesno("New Difficulty?", "change difficulty level? ")
            if change_difficulty:
                difficulty = difficulty_level()
                display.write("Press 's' to start\nQuit: q | Move Up: ↑ | Move Down: ↓\nAvoid the power up ball :D", align="center", font=("Consolas", 15, "normal"))
                winsound.PlaySound("C:\\Users\\Daniel-Panovest\\Downloads\\gamesound.wav", winsound.SND_ASYNC)
            else:
                read_player_data()
                display.write("Press 's' to start\nQuit: q | Move Up: ↑ | Move Down: ↓\nAvoid the power up ball :D", align="center", font=("Consolas", 15, "normal"))
                winsound.PlaySound("C:\\Users\\Daniel-Panovest\\Downloads\\gamesound.wav", winsound.SND_ASYNC)
               
        player_a_score = player_b_score = 0
        winner.clear()
        score.clear()
        score.write(f"{player_a_name}:{player_a_score} | {player_b_name}:{player_b_score}", align="center", font=("Consolas", 15, "normal"))

        paddle_a.goto(-350,0)
        paddle_b.goto(350,0)
        ball.goto(0,0)
        ball.hideturtle()
        paddle_a.hideturtle()
        paddle_b.hideturtle()

        #reset the time
        start_time = time.time()

        #hide the power up ball if it exists
        if power is not None:
            power.hide_powerup()

        xVelocity = 4
        yVelocity = 3
        ball.move_ball()

        powerup_timer()

        write_player_data(player_data_file)
        read_player_data()
            
        window.update()
        window.mainloop()

    else:
        window.bye()

def powerup_timer():
    global power, start_time, xVelocity, yVelocity
    elapsed_time = time.time() - start_time

    if elapsed_time > 30 and power is None and ball.color()[0]!= "red":
        power = Powerup(x=random.randint(-340,340), y=random.randint(-250,250))
        power.show_powerup()
        winsound.PlaySound("C:\\Users\\Daniel-Panovest\\Downloads\\powerup.wav", winsound.SND_ASYNC)
        xVelocity *= 1.1
        yVelocity *= 1.1
        start_time = time.time()    

    powerup_elapsed_time = time.time() - start_time

    if powerup_elapsed_time > 18 and power is not None:
        power.hide_powerup()     
        power = None
        start_time = time.time()      

display = Display(0,0)
paddle_a = Paddle(-350,0) 
paddle_b = Paddle(350,0)
ball = Ball(0,0)
score = Score(0,250)
winner = Winner(0,229) 

write_player_data(player_data_file)

def start_game():
    global display
    while True:
        window.update()
        display.clear()
        ball.showturtle()
        ball.move_ball()
        ball.border_checking()
        ball.collisions()
        paddle_a.showturtle()
        paddle_b.showturtle()
        paddle_a.check_border()
        paddle_b.check_border()
        paddle_b.ai_paddle(ball, difficulty)
    
        powerup_timer()

        if game_over():        
            new_game()

window.listen()
window.onkeypress(paddle_a.paddle_up, "Up")
window.onkeypress(paddle_a.paddle_down, "Down")
window.onkeypress(reset_game, "q")
window.onkeypress(start_game, "s")

window.mainloop()