import pygame as pg
from map import background
from cars.car import Car

pg.init()
pg.display.set_caption('Racing Game')

player_car = Car()
clock = pg.time.Clock()
crash = False

while not crash:
    for event in pg.event.get():
        # print(event) # writes in terminal everything that user does in the window
        if event.type == pg.QUIT:
            crash = True
            # we can choose if we want to close the window or send a message here before closing


    keys=pg.key.get_pressed() # we need to move on this because we need both keys pressed to move
    player_car.update_car(keys)
    background.update_background(player_car)
    player_car.draw()
    pg.display.update()  # you can use flip here, will update everything, but it is recommended to use this in 2D
    background.check_boundaries(player_car)
    background.check_for_checkpoints(player_car)

    if player_car.checkpoint == 99:
        print("win")
    #print(f'Nodes so far: {done}/{all}')
    clock.tick(60)  # the faster, the more you need here

pg.quit()
quit()
