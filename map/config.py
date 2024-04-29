from enum import Enum
import pygame as pg
from pygame.locals import *
# constants
display_width = 600
display_height = 400
zoom = 5
road_width = 30

game_display = pg.display.set_mode((display_width, display_height), HWSURFACE | DOUBLEBUF | RESIZABLE)