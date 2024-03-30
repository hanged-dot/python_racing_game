import os
import pygame as pg

from map.background import game_display

car_image = pg.image.load("images/car.png")


def car(x,y):
    game_display.blit(car_image, (x, y))


'''
class Car(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = car_image

'''
