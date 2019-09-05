import pygame
import Track
from math import *

class Car(object):

    def __init__(self, pos_x, pos_y, width, height, angle = -90.0, max_vel = 12.0, max_acc = 2.0, dec = 0.94):
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

        self.sensors = [None] * 7

    def move(self, dt):

        #self.acc = max(-self.max_acc, min(self.max_acc, self.acc))
        if self.angle > 360.0:
            self.angle -= 360.0
        if self.angle < 0:
            self.angle += 360.0

        if self.acc.x:
            self.vel += self.acc
            if self.vel.length_squared() > self.max_vel * self.max_vel:
                self.vel *= self.max_vel / self.vel.length()
        else:
            self.vel = self.dec * self.vel
        
        self.pos += self.vel * dt

    def draw(self, game_window):
        if self.hitting == False:
            rotated_img = pygame.transform.rotozoom(self.image, -self.angle, 1)
        else:
            rotated_img = pygame.transform.rotozoom(self.hitting_image, -self.angle, 1)
        rect = rotated_img.get_rect()
        rect.center = self.pos
        game_window.blit(rotated_img, rect)

        for sensor in self.sensors:
            pygame.draw.line(game_window, (0, 0, 0), sensor[0] ,sensor[1])

    def rotate(self, point):
        point -= self.pos
        new_x = cos(radians(self.angle)) * point[0] - sin(radians(self.angle)) * point[1]
        new_y = sin(radians(self.angle)) * point[0] + cos(radians(self.angle)) * point[1]
        point[0] = new_x
        point[1] = new_y
        point += self.pos
        return point

    def isHitting(self, track):

        to_corner = pygame.math.Vector2(self.width / 2, self.height / 2)
        corners = [(0, 0)] * 4
        corners[0] = self.pos + (to_corner.x * -1, to_corner.y * -1)
        corners[1] = self.pos + (to_corner.x * 1, to_corner.y * -1)
        corners[2] = self.pos + (to_corner.x * 1, to_corner.y * 1)
        corners[3] = self.pos + (to_corner.x * -1, to_corner.y * 1)

        top_point = self.pos + (self.width / 2, 0)
        bonus_points = [(0, 0)] * 7
        bonus_points[4] = top_point + (2000, 0)
        bonus_points[5] = top_point + (2000, 2000)
        bonus_points[6] = top_point + (2000, -2000)
        bonus_points[0] = corners[0] - (0, 2000)
        bonus_points[1] = corners[1] - (0, 2000)
        bonus_points[2] = corners[2] + (0, 2000)
        bonus_points[3] = corners[3] + (0, 2000)

        top_point = self.rotate(top_point)
        for i in range(4):
            corners[i] = self.rotate(corners[i])
        for i in range(7):
            bonus_points[i] = self.rotate(bonus_points[i])
        
        lines = [(x,y) for (x,y) in zip(corners[:-1], corners[1:])] + [(corners[-1], corners[0])]
        sensors = [(x,top_point) for x in bonus_points[4:]] + [(x,y) for (x,y) in zip(bonus_points[:4], corners[:4])]

        border_lines = [(x, y) for (x,y) in zip(track.borders[0][:-1], track.borders[0][1:])] + [(x, y) for (x,y) in zip(track.borders[1][:-1], track.borders[1][1:])]

        for i,sensor in enumerate(sensors):
            min_dist = 2000 ** 2
            self.sensors[i] = sensor
            for border_line in border_lines:
                inter = intersection(sensor, border_line)
                if inter:
                    if isBetween(border_line, inter) and isBetween(sensor, inter) and dist(sensor[1], inter) < min_dist:
                        min_dist = dist(sensor[1], inter)
                        self.sensors[i] = (inter, sensor[1])

        for line in lines:
            for border_line in border_lines:
                inter = intersection(line, border_line)
                if inter:
                    if isBetween(line, inter) and isBetween(border_line, inter):
                        return True

        return False


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

def dist(p1, p2):
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2