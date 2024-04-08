from enum import Enum
import pygame as pg
from pygame.locals import *
# constants
display_width = 1280
display_height = 800
game_display = pg.display.set_mode((display_width, display_height), HWSURFACE | DOUBLEBUF | RESIZABLE)


class Way(Enum):
    down_left = 0
    down_right = 1
    side = 2
    up = 3
    up_left = 4
    up_right = 5
