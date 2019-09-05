import pygame
import sys
import Car
import Track
from math import *

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1000

background_colour = (0, 80, 80)

pygame.init()

game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

clock = pygame.time.Clock()

pygame.display.set_caption("nice")

game_running = True

car = Car.Car(220, 420, 40, 20)
track = Track.Track('easy.txt', (255, 255, 255))

while game_running:
    dt = clock.get_time() / 40
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_UP]:
        car.acc = pygame.math.Vector2(dt * 3 * cos(radians(car.angle)), dt * 3 * sin(radians(car.angle))) 
    elif pressed[pygame.K_DOWN]:
        car.acc = pygame.math.Vector2(-dt * 3 * cos(radians(car.angle)), -dt * 3 * sin(radians(car.angle))) 
    else:
        car.acc = pygame.math.Vector2(0, 0)

    if pressed[pygame.K_LEFT]:
        #car.steering += car.max_steering * dt * 0.3
        car.angle -= dt * 8 * car.vel.length() / car.max_vel
    elif pressed[pygame.K_RIGHT]:
        #car.steering += car.max_steering * dt * 0.3
        car.angle += dt * 8 * car.vel.length() / car.max_vel
    else:
        car.steering = 0

    game_window.fill(background_colour)

    track.draw(game_window, background_colour)

    if car.isHitting(track) == True:
        car.hitting = True
    else:
        car.hitting = False

    car.move(dt)
    car.draw(game_window)

    pygame.display.update()

    clock.tick(60)

pygame.quit()
sys.exit()