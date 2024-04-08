import pygame as pg
import pygame.display

from map import grid
from map import config


background = pg.transform.scale(pg.image.load('images/desert.png').convert(), (256, 256))
game_grid=grid.Grid(config.display_width, config.display_height,[(0,0,config.Way.up)])

def update_background():
    for y in range(0, config.display_height, 256):
        for x in range(0, config.display_width, 256):
            config.game_display.blit(background, (x, y))
    game_grid.draw_grid()

def borders(x, y, object_width, object_height):
    if x > config.display_width - object_width or x < 0:
        return False
    if y > config.display_height - object_height or y < 0:
        return False
    return True
