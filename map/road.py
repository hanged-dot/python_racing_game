import pygame as pg


class Road():
    def __init__(self, x, y, way):
        self.x = x
        self.y = y
        self.image = pg.image.load('images' + way + '_tile.png')
