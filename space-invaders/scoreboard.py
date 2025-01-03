from turtle import Turtle


class ScoreBoard(Turtle):
    def __init__(self):
        super().__init__()
        self.score = 0
        self.penup()
        self.color("white")
        self.hideturtle()
        self.display_score()

    def display_score(self):
        self.clear()
        self.goto((-250, 250))
        self.write(f"Score: {self.score}", align="left", font=("Fixedsys", 15, "normal"))

    def increase_score(self):
        self.score += 1
        self.display_score()
