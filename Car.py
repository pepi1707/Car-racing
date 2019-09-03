import pygame
import Track
from math import *

class Car(object):

    def __init__(self, pos_x, pos_y, width, height, angle = -90.0, max_vel = 10.0, max_acc = 2.0, dec = 0.92):
        self.width = width
        self.height = height
        self.pos = pygame.math.Vector2(pos_x, pos_y)
        self.vel = pygame.math.Vector2(0, 0)
        self.angle = angle

        self.max_vel = max_vel
        self.max_acc = max_acc
        
        self.acc = pygame.math.Vector2(0, 0)
        self.dec = dec

        self.image = pygame.image.load("car.png")
        self.hitting_image = pygame.image.load("car_hitting.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.hitting_image = pygame.transform.scale(self.hitting_image, (self.width, self.height))

        self.hitting = False

    def move(self, dt):

        #self.acc = max(-self.max_acc, min(self.max_acc, self.acc))

        if self.acc.x:
            self.vel += self.acc
            if self.vel.length_squared() > self.max_vel * self.max_vel:
                self.vel *= self.max_vel / self.vel.length()
        else:
            self.vel = self.dec * self.vel
        
        self.pos += self.vel * dt

    def draw(self, game_window):
        if self.hitting == False:
            rotated_img = pygame.transform.rotate(self.image, self.angle + 90)
        else:
            rotated_img = pygame.transform.rotate(self.hitting_image, self.angle + 90)
        game_window.blit(rotated_img, self.pos - (self.width / 2, self.height / 2))

    def isHitting(self, track):

        def intersection(line1, line2):
            xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
            ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

            def det(a, b):
                return a[0] * b[1] - a[1] * b[0]

            div = det(xdiff, ydiff)
            if div == 0:
                return False

            d = (det(*line1), det(*line2))
            x = det(d, xdiff) / div
            y = det(d, ydiff) / div
            return x, y
        
        def isBetween(l, p):
            if l[0][0] <= p[0] <= l[1][0] or l[0][0] >= p[0] >= l[1][0]:
                if l[0][1] <= p[1] <= l[1][1] or l[0][1] >= p[1] >= l[1][1]:
                    return True
            return False

        to_corner = pygame.math.Vector2(self.width / 2, self.height / 2)
        corners = [(0, 0)] * 4
        corners[0] = self.pos + (to_corner.x * -1, to_corner.y * -1)
        corners[1] = self.pos + (to_corner.x * 1, to_corner.y * -1)
        corners[3] = self.pos + (to_corner.x * -1, to_corner.y * 1)
        corners[2] = self.pos + (to_corner.x * 1, to_corner.y * 1)

        for i in range(4):
            corners[i] -= self.pos
            new_x = cos(radians(self.angle)) * corners[i].x - sin(radians(self.angle)) * corners[i].y
            new_y = sin(radians(self.angle)) * corners[i].x + cos(radians(self.angle)) * corners[i].y
            corners[i].x = new_x
            corners[i].y = new_y
            corners[i] += self.pos
        lines = [(corners[0], corners[1]), (corners[1], corners[2]), (corners[2], corners[3]), (corners[3], corners[0])]

        border_lines = [(x, y) for (x,y) in zip(track.borders[0][:-1], track.borders[0][1:])] + [(x, y) for (x,y) in zip(track.borders[1][:-1], track.borders[1][1:])]

        for line in lines:
            for border_line in border_lines:
                if intersection(line, border_line):
                    inter = intersection(line, border_line)
                    if isBetween(line, inter) and isBetween(border_line, inter):
                        return True

        return False
 
