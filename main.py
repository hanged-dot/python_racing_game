import pygame as pg
import pygame.display
from map import background
from cars import car
from pygame.locals import *
from map.pathgenerator import PathGenerator
from map import background
from cars.car import Car

pg.init()
pg.display.set_caption('Racing Game')

player_car = Car()
clock = pg.time.Clock()
crash = False
change_x=0
change_y=0
vel = 1.4

while not crash:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            crash = True
            # we can choose if we want to close the window or send a message here before closing
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                change_x = -vel
            if event.key == pg.K_RIGHT:
                change_x = vel
            if event.key == pg.K_UP:
                change_y = -vel
            if event.key == pg.K_DOWN:
                change_y = vel
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                change_x=0
            if event.key == pg.K_UP or event.key == pg.K_DOWN:
                change_y=0

        # print(event) # writes in terminal everything that user does in the window
    player_car.position[0] += change_x
    player_car.position[1] += change_y

    background.update_background(player_car)
    player_car.draw()
    pg.display.update()  # you can use flip here, will update everything, but it is recommended to use this in 2D
    clock.tick(60)  # the faster, the more you need here

pg.quit()
quit()
