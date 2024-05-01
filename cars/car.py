import os
import pygame as pg
from math import pi, sin, cos, atan

from map import config
from map import background


class Car():
    def __init__(self,road):
        self.image = pg.image.load("images/car.png")
        self.default_image = pg.image.load("images/car.png")
        self.position = [background.road.path[0][0], background.road.path[0][1]]
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.velocity = 0
        self.acceleration = 0.002
        self.standby=0.001
        self.angle = 0
        self.rotation = 3
        self.max_speed = config.max_speed
        self.checkpoint = 0
        self.dist_to_goal = 0

        self.road_angle(road)

    def draw(self):
        temp_position = [
            self.position[0] * config.zoom + config.display_width / 2 - self.position[0] * config.zoom - self.width / 2,
            self.position[1] * config.zoom + config.display_height / 2 - self.position[1] * config.zoom - self.height / 2]
        config.game_display.blit(self.image, temp_position)

    def update_car(self, keys):
        self.rotate_car(keys)
        self.move_car(keys)
    
    def road_angle(self,road):
        if self.checkpoint+1 == 100:
            return

        A = road.path[self.checkpoint]
        B = road.path[self.checkpoint+1]

        if B[0] < A[0]:
            self.angle = atan(-(B[1]-A[1])/(B[0]-A[0])) / 2 / pi * 360 + 90
        else:
            self.angle = atan(-(B[1]-A[1])/(B[0]-A[0])) / 2 / pi * 360 + 270

    def move_to_checkpoint(self,road):
        self.position = list(background.road.path[self.checkpoint])
        self.velocity = 0
        self.road_angle(road)

    def move_car(self, keys):
        rad = -1*(90-self.angle) * 2 * pi / 360
        if keys[pg.K_UP]:
            if abs(self.velocity) < self.max_speed:
                self.velocity += self.acceleration
        elif keys[pg.K_DOWN]:
            if abs(self.velocity) < self.max_speed:
                self.velocity -= self.acceleration
        else:
            if self.velocity > self.standby and self.velocity>0:
                self.velocity -= self.standby
            elif self.velocity < -self.standby and self.velocity<0:
                self.velocity += self.standby
            else:
                self.velocity = 0
        change_x = self.velocity * cos(rad) * -1
        change_y = self.velocity * sin(rad)
        self.position[0] += change_x
        self.position[1] += change_y

    def rotate_car(self, keys):
        self.rotation=3*self.velocity
        if keys[pg.K_LEFT] and keys[pg.K_UP]:
            self.angle += self.rotation
        if keys[pg.K_RIGHT] and keys[pg.K_UP]:
            self.angle += -self.rotation
        if keys[pg.K_LEFT] and keys[pg.K_DOWN]:
            self.angle += -self.rotation
        if keys[pg.K_RIGHT] and keys[pg.K_DOWN]:
            self.angle += self.rotation
        rotated_image = pg.transform.rotate(self.default_image, self.angle)
        self.image = rotated_image




