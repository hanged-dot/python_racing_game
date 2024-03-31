import pygame as pg
import pygame.display
from pygame.locals import *
display_width = 1000
display_height = 800
game_display = pg.display.set_mode((display_width, display_height), HWSURFACE | DOUBLEBUF | RESIZABLE)
background = pg.transform.scale(pg.image.load('images/desert.png').convert(), (240, 160))


def update_background():
    for y in range(0, display_height, 160):
        for x in range(0, display_width, 240):
            game_display.blit(background, (x, y))


def borders(x, y, object_width, object_height):
    if x > display_width - object_width or x < 0:
        return False
    if y > display_height - object_height or y < 0:
        return False
    return True

