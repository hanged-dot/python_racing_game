import pygame as pg
from cars.car import Car
from map.road import Road
from map.background import Background
from map import config
from display import Display

pg.init()
pg.mixer.init()
pg.display.set_caption('Racing Game')

display = Display(config.display_width,config.display_height,config.music_volume,config.sound_volume)
road = Road(config.road_length,config.road_width,config.max_speed,config.zoom,display)
player_car = Car(road,display)

background = Background(config.display_width,config.display_height,display)

clock = pg.time.Clock()
crash = False

while not crash:
    for event in pg.event.get():
        if event.type!= pg.MOUSEMOTION: print(event) # writes in terminal everything that user does in the window
        if event.type == pg.QUIT:
            crash = True
            # we can choose if we want to close the window or send a message here before closing
        if event.type == pg.WINDOWSIZECHANGED:
            background.update_display(event.x,event.y)
            background.draw()
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            pg.mixer.Sound("images/automobile-horn-153260.mp3").play()
        if event.type == pg.KEYDOWN and (event.key == pg.K_UP or event.key == pg.K_DOWN):
            player_car.engine_sound.play()



    keys=pg.key.get_pressed() # we need to move on this because we need both keys pressed to move

    player_car.update(keys)
    road.check_boundaries(player_car)
    road.check_for_checkpoints(player_car)
    
    background.draw()
    road.draw(player_car.get_position())
    player_car.draw()


    pg.display.update()  # you can use flip here, will update everything, but it is recommended to use this in 2D
    #print(f'Nodes so far: {done}/{all}')
    clock.tick(60)  # the faster, the more you need here

pg.quit()
quit()
