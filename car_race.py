import pygame
import sys
import Car
import Track

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1000

background_colour = (0, 80, 80)

pygame.init()

game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

clock = pygame.time.Clock()

pygame.display.set_caption("nice")

game_running = True

car = Car.Car(100, 100, 20, 40)
track = Track.Track('easy.txt', (255, 255, 255))

while game_running:
    dt = clock.get_time() / 20
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_UP]:
        car.acc -= dt * 0.1
    elif pressed[pygame.K_DOWN]:
        car.acc += dt * 0.1
    else:
        car.acc = 0

    if pressed[pygame.K_LEFT]:
        car.steering -= car.max_steering * dt * 0.3
    elif pressed[pygame.K_RIGHT]:
        car.steering += car.max_steering * dt * 0.3
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

    clock.tick(120)

pygame.quit()
sys.exit()