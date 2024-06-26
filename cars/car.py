import os
import copy
import pygame as pg
from math import pi, sin, cos, atan

import config
from map import background


class Car:
    def __init__(self, road, display):
        self.road = road
        self.__image = pg.image.load("images/car.png")
        self.__default_image = pg.image.load("images/car.png")
        self.__position = [self.road.get_path()[0][0], self.road.get_path()[0][1]]
        self.__width = self.__image.get_width()
        self.__height = self.__image.get_height()
        self.__velocity = 0
        self.__acceleration = 0.002
        self.__standby = 0.001
        self.__angle = 0
        self.__rotation = 3
        self.__drift_factor = 0.01
        self.__drift_dir = 0
        self.__max_speed = config.max_speed
        self.__checkpoint = 0
        self.__dist_to_goal = 0
        self.__display = display
        self.__volume = 0
        self.__iter = 0
        self.__velsum = 0
        self.engine_sound = pg.mixer.Sound("images/car-engine-71198.mp3")

        self.__road_angle()

    def set_dist_to_goal(self, dist):
        self.__dist_to_goal = dist

    def get_dist_to_goal(self):
        return self.__dist_to_goal

    def get_position(self):
        return self.__position

    def restart(self):
        self.__checkpoint = 0
        self.move_to_checkpoint()

    def get_velocity(self):
        return self.__velocity

    def draw(self, center):
        temp_position = [
            self.__position[0] * self.road.get_zoom() + self.__display.width / 2 - center[
                0] * self.road.get_zoom() - self.__width / 2,
            self.__position[1] * self.road.get_zoom() + self.__display.height / 2 - center[
                1] * self.road.get_zoom() - self.__height / 2]

        self.__display.display.blit(self.__image, temp_position)

    def update(self, keys):
        self.__rotate(keys)
        self.__move(keys)

        self.__iter += 1
        self.__velsum += self.__velocity

    def get_avg_velocity(self):
        return self.__velsum / self.__iter

    def __road_angle(self):
        if self.__checkpoint + 1 == self.road.get_length():
            return

        A = self.road.get_path()[self.__checkpoint]
        B = self.road.get_path()[self.__checkpoint + 1]

        if B[0] < A[0]:
            self.__angle = atan(-(B[1] - A[1]) / (B[0] - A[0] + 1e-10)) / 2 / pi * 360 + 90
        else:
            self.__angle = atan(-(B[1] - A[1]) / (B[0] - A[0] + 1e-10)) / 2 / pi * 360 + 270

    def move_to_checkpoint(self):
        self.__position = list(self.road.get_path()[self.__checkpoint])
        self.__velocity = 0
        self.__drift_dir = 0
        self.__road_angle()

    def get_checkpoint(self):
        return self.__checkpoint

    def set_checkpoint(self, checkpoint):
        self.__checkpoint = checkpoint

    def __move(self, keys):
        rad = -1 * (90 - self.__angle) * 2 * pi / 360
        if keys[pg.K_UP]:
            if abs(self.__velocity) < self.__max_speed:
                self.__velocity += self.__acceleration
        elif keys[pg.K_DOWN]:
            if abs(self.__velocity) < self.__max_speed:
                self.__velocity -= self.__acceleration
        else:
            if self.__velocity > self.__standby and self.__velocity > 0:
                self.__velocity -= self.__standby
            elif self.__velocity < -self.__standby and self.__velocity < 0:
                self.__velocity += self.__standby
            else:
                self.__velocity = 0
        #self.volume = (1 - ((self.__max_speed-abs(self.__velocity))/self.__max_speed))*pg.mixer.music.get_volume()
        self.engine_sound.set_volume(self.__volume)
        change_x = self.__velocity * cos(rad) * -1
        change_y = self.__velocity * sin(rad)

        change_x += cos(rad + pi / 2) * -1 * self.__drift_dir
        change_y += sin(rad + pi / 2) * self.__drift_dir

        self.__position[0] += change_x
        self.__position[1] += change_y

    def __rotate(self, keys):
        self.__rotation = 3 * self.__velocity
        const = self.__drift_factor * self.__velocity
        if keys[pg.K_LEFT] and self.__velocity > 0:
            self.__angle += self.__rotation
            self.__drift_dir += -1 * const
        if keys[pg.K_RIGHT] and self.__velocity > 0:
            self.__angle += -self.__rotation
            self.__drift_dir += 1 * const
        if keys[pg.K_LEFT] and self.__velocity < 0:
            self.__angle += -self.__rotation
            self.__drift_dir += -1 * const
        if keys[pg.K_RIGHT] and self.__velocity < 0:
            self.__angle += self.__rotation
            self.__drift_dir += 1 * const

        if not keys[pg.K_LEFT] and not keys[pg.K_RIGHT]:
            if self.__drift_dir < 0: self.__drift_dir += 0.02 * abs(self.__velocity)
            if self.__drift_dir > 0: self.__drift_dir -= 0.02 * abs(self.__velocity)

        rotated_image = pg.transform.rotate(self.__default_image, self.__angle)
        self.__image = rotated_image

    def finish_line(self):
        if self.__dist_to_goal == 0:
            return True
        return False
