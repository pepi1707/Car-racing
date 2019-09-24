import pygame
import sys
import Car
import Track
import numpy as np
from math import *

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1000

background_colour = (0, 80, 80)

class Car_Environment(object):

    def __init__(self):

        self.car = Car.Car(220, 420, 40, 20)
        self.track = Track.Track('test', (255, 255, 255))

        self.isRendering = False
        self.observation_space = ((0, 1e9)) * 7

        self.rewardIndex = 0
        self.isRendering = False

    def render(self):
        import os
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (42,42)
        self.isRendering = True
        pygame.init()
        self.game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    def endRender(self):
        self.isRendering = False
        pygame.quit()

    def reset(self):
        self.car = Car.Car(200, 420, 40, 20)
        self.track.rewardIndex = 0
        self.car.isHitting(self.track)
        return np.array([(x - y).length() for x,y in self.car.sensors])

    def step(self, act):

        if act == 0:
            self.car.acc = pygame.math.Vector2(0.425 * 3 * cos(radians(self.car.angle)), 0.425 * 3 * sin(radians(self.car.angle))) 
        elif act == 3:
            self.car.acc = pygame.math.Vector2(-0.425 * 3 * cos(radians(self.car.angle)), -0.425 * 3 * sin(radians(self.car.angle))) 
        else:
            self.car.acc = pygame.math.Vector2(0, 0)

        if act == 1:
            self.car.angle -= 0.425 * 10 #* self.car.vel.length() / self.car.max_vel
        elif act == 2:
            self.car.angle += 0.425 * 10 #* self.car.vel.length() / self.car.max_vel

        if self.car.isHitting(self.track) == True:
            return np.zeros(7), -1, True, 1

        self.car.move(0.425)
        if self.isRendering:
            self.game_window.fill(background_colour)

            self.track.draw(self.game_window, background_colour)

            self.car.draw(self.game_window)

            pygame.display.update()
        
        return np.array([(x - y).length() / 100 for x,y in self.car.sensors]), self.car.hasReward, False, 1



