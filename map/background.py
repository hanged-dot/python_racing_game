import os
import pygame as pg
import pygame.display
from pygame.locals import *

display_width = 800
display_height = 600
game_display = pg.display.set_mode((display_width, display_height), HWSURFACE | DOUBLEBUF | RESIZABLE)
pg.display.set_caption('Racing Game')
background = pg.transform.scale(pg.image.load('images/desert.png').convert(), (240, 160))


def update_background():
    for y in range(0, display_height, 160):
        for x in range(0, display_width, 240):
            game_display.blit(background, (x, y))
