import os
import pygame as pg

from map import config
from map import background


class Car():
    def __init__(self):
        self.image = pg.image.load("images/car.png")
        self.position = [background.road.path[0][0],background.road.path[0][1]]
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def draw(self):
        temp_position = [self.position[0]*config.zoom+config.display_width/2-self.position[0]*config.zoom-self.width/2,
                         self.position[1]*config.zoom+config.display_height/2-self.position[1]*config.zoom-self.height/2]
        config.game_display.blit(self.image, temp_position)


'''
class Car(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = car_image

'''
