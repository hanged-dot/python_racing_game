import pygame as pg

class Background():
    def __init__(self,width,height,display):
        self.__image = pg.transform.scale(pg.image.load('images/desert.png').convert(), (256, 256))
        self.__width = width
        self.__height = height
        self.__display = display

    def draw(self):
        for y in range(0, self.__height, 256):
            for x in range(0, self.__width, 256):
                self.__display.display.blit(self.__image, (x, y))
    def update_display(self, width,height):
        self.__height = height
        self.__width = width
