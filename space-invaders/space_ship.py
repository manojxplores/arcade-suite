import turtle

ship_img = "assets/spaceship.gif"
bullet_img = "assets/bullet.gif"
turtle.register_shape(bullet_img)
turtle.register_shape(ship_img)


class SpaceShip(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape(ship_img)
        self.penup()
        self.speed("fastest")
        self.goto((0, -240))
        self.cartridge = []

    def add_laser(self):
        beam = turtle.Turtle()
        beam.penup()
        beam.setheading(90)
        beam.shape("square")
        beam.color("DeepSkyBlue")
        beam.shapesize(stretch_len=1, stretch_wid=0.25)
        beam.goto((self.xcor(), self.ycor()))
        self.cartridge.append(beam)

    def fire_laser(self):
        for beam in self.cartridge[:]:
            beam.forward(5)
            if beam.ycor() > 300:
                self.cartridge.remove(beam)
                beam.hideturtle()

    def move_right(self):
        self.setx(self.xcor() + 5)

    def move_left(self):
        self.setx(self.xcor() - 5)


# changes from self.forward to setx()
# Logic to remove lasers that go off screen