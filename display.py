import pygame as pg
from pygame.locals import *


class Display:
    def __init__(self,width,height,music_volume,sound_volume):
        self.width = width
        self.height = height
        self.display = pg.display.set_mode((self.width, self.height), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.music_volume = music_volume
        self.sound_volume = sound_volume
        pg.mixer.music.load("images/Real Gone-[AudioTrimmer.com].mp3")
        pg.mixer.music.set_volume(self.music_volume)
        pg.mixer.music.play(-1)

    def update_display(self, width,height):
        self.width=width
        self.height=height
        self.display =pg.display.set_mode((self.width, self.height), HWSURFACE | DOUBLEBUF | RESIZABLE)
