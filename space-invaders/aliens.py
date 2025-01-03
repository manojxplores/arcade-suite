import turtle
import random

HEIGHT_MAX = 300
WIDTH_MAX = 250
ALIEN_SPACING = 50

alien_img = "alien1.gif"
turtle.register_shape(alien_img)


class Aliens:
    def __init__(self):
        self.alien_swarm = []
        self.add_swarm()

    def add_swarm(self):
        for _ in range(10):
            self.add_alien()

    def add_alien(self):
        while True:
            x = random.uniform(-WIDTH_MAX, WIDTH_MAX)
            y = random.uniform(100, HEIGHT_MAX)
            if all(alien.distance(x, y) > ALIEN_SPACING for alien in self.alien_swarm):
                alien = turtle.Turtle()
                alien.penup()
                alien.shape(alien_img)
                alien.speed("slowest")
                alien.goto(x, y)
                self.alien_swarm.append(alien)
                break

    def move(self):
        for alien in self.alien_swarm:
            alien.sety(alien.ycor() - 0.5)


# REPLACE forward()/backward() with setx/sety
# add_alien method now checks distances from all existing aliens to avoid clustering.
