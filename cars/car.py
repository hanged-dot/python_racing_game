import os
import pygame as pg
from math import pi, sin, cos, sqrt

from map import config
from map import background


class Car():
    def __init__(self):
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
        self.max_speed = 5
        self.checkpoint = 0

    def draw(self):
        temp_position = [
            self.position[0] * config.zoom + config.display_width / 2 - self.position[0] * config.zoom - self.width / 2,
            self.position[1] * config.zoom + config.display_height / 2 - self.position[
                1] * config.zoom - self.height / 2]
        config.game_display.blit(self.image, temp_position)

    def update_car(self, keys):
        self.rotate_car(keys)
        self.move_car(keys)

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




