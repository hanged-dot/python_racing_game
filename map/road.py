import pygame as pg
from map import config


class Road():
    def __init__(self, x: int, y: int, way):
        self.x = x
        self.y = y
        self.image = pg.image.load('images/' + way + '.png')
        self.passed = 0

    def draw(self):
        config.game_display.blit(self.image, (self.x, self.y))
