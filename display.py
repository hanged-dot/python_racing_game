import pygame as pg
from pygame.locals import *

class Display:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.display = pg.display.set_mode((self.width, self.height), HWSURFACE | DOUBLEBUF | RESIZABLE)