import pygame as pg
from map import config
from map.road import Road
from map.distance import dist_point_segment

background = pg.transform.scale(pg.image.load('images/desert.png').convert(), (256, 256))
road = Road()

def update_background(car):
    for y in range(0, config.display_height, 256):
        for x in range(0, config.display_width, 256):
            config.game_display.blit(background, (x, y))

    road.draw(car)

def borders(x, y, object_width, object_height):
    if x > config.display_width - object_width or x < 0:
        return False
    if y > config.display_height - object_height or y < 0:
        return False
    return True

def check_for_checkpoints(car):
    return road.checkpoints(car)

def check_boundaries(car):
    distances = [dist_point_segment(road.path[i],road.path[i+1],car.position) for i in range(len(road.path)-1)]
    
    if min(distances) > config.road_width/2:
        car.move_to_checkpoint(road)