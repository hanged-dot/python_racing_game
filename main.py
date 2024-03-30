import pygame as pg
import pygame.display
from map import background
from cars import car

pg.init()

clock = pg.time.Clock()
crash = False
position = [0, 0]
change_x=0
change_y=0
while not crash:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            crash = True
            # we can choose if we want to close the window or send a message here before closing
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_LEFT:
                change_x = -10
            if event.key == pg.K_RIGHT:
                change_x = 10
            if event.key == pg.K_UP:
                change_y = -10
            if event.key == pg.K_DOWN:
                change_y = 10
        if event.type == pg.KEYUP:
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                change_x=0
            if event.key == pg.K_UP or event.key == pg.K_DOWN:
                change_y=0

        # print(event) # writes in terminal everything that user does in the window
    position[0] += change_x
    position[1] += change_y
    background.update_background()
    car.car(position[0], position[1])
    pg.display.update()  # you can use flip here, will update everything, but it is recommended to use this in 2D
    clock.tick(60)  # the faster, the more you need here

pg.quit()
quit()
