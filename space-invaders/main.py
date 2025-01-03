from turtle import Turtle, Screen
from space_ship import SpaceShip
from aliens import Aliens
from scoreboard import ScoreBoard
import time

screen = Screen()
screen.title("Space Invaders")
screen.setup(width=600, height=600)
screen.bgpic("bg.png")
screen.listen()
screen.tracer(0)

sunny = SpaceShip()
aliens = Aliens()
score_board = ScoreBoard()


key_states = {'Left': False, 'Right': False, 'Space': False}

def start_move_right():
    key_states['Right'] = True

def start_move_left():
    key_states['Left'] = True

def start_shoot():
    key_states['Space'] = True

def stop_move_right():
    key_states['Right'] = False

def stop_move_left():
    key_states['Left'] = False

def stop_shoot():
    key_states['Space'] = False


screen.onkeypress(start_move_right, "d")
screen.onkeyrelease(stop_move_right, "d")
screen.onkeypress(start_move_left, "a")
screen.onkeyrelease(stop_move_left, "a")
screen.onkeypress(start_shoot, "space")
screen.onkeyrelease(stop_shoot, "space")


def display_game_over():
    game_over_turtle = Turtle()
    game_over_turtle.hideturtle()
    game_over_turtle.penup()
    game_over_turtle.color("white")
    game_over_turtle.goto((0, 0))
    game_over_turtle.write("GAME OVER !", align="center", font=("Fixedsys", 25, "normal"))


last_shot_time = time.time()
SHOT_COOLDOWN = 0.5

game_over = False
while not game_over:
    if key_states['Right']:
        sunny.move_right()
    if key_states['Left']:
        sunny.move_left()

    current_time = time.time()
    if key_states['Space'] and current_time - last_shot_time >= SHOT_COOLDOWN:
        sunny.add_laser()
        last_shot_time = current_time

    aliens.move()
    sunny.fire_laser()
    for beam in sunny.cartridge:
        for alien in aliens.alien_swarm:
            if alien.distance(beam) < 20:
                score_board.increase_score()
                sunny.cartridge.remove(beam)
                beam.hideturtle()
                aliens.alien_swarm.remove(alien)
                alien.hideturtle()

    if len(aliens.alien_swarm) < 5:
        aliens.add_alien()

    screen.update()
    time.sleep(0.01)

    for alien in aliens.alien_swarm:
        if alien.ycor() < -240:
            game_over = True
            display_game_over()
            break

screen.exitonclick()
