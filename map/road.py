import pygame as pg
from map import config
from map.pathgenerator import PathGenerator
from map.distance import dist, dist_point_segment


class Road():
    def __init__(self):
        self.road_length = 100
        self.wholepath=PathGenerator(path_points=self.road_length,width=config.display_height,height=config.display_width,path_width=config.road_width)
        self.path = self.wholepath.get_path()

    def draw_line(self,surf,p1,p2,c,w):
        p1v = pg.math.Vector2(p1)
        p2v = pg.math.Vector2(p2)
        lv = (p2v - p1v).normalize()
        lnv = pg.math.Vector2(-lv.y, lv.x) * w // 2
        pts = [p1v + lnv, p2v + lnv, p2v - lnv, p1v - lnv]
        pg.draw.polygon(surf, c, pts)
        pg.draw.circle(surf, c, p1, round(w / 2))
        pg.draw.circle(surf, c, p2, round(w / 2))

    def draw(self,car):
        for i in range(len(self.path)-1):
            p1 = [self.path[i][0]*config.zoom+config.display_width/2-car.position[0]*config.zoom,
                  self.path[i][1]*config.zoom+config.display_height/2-car.position[1]*config.zoom]
            p2 = [self.path[i+1][0]*config.zoom+config.display_width/2-car.position[0]*config.zoom,
                  self.path[i+1][1]*config.zoom+config.display_height/2-car.position[1]*config.zoom]
            self.draw_line(config.game_display,p1,p2,"orange",config.road_width*config.zoom)

    def checkpoints(self,car):
        distances = [(i,dist_point_segment(self.path[i],self.path[i+1],car.position)) for i in range(len(self.path)-1)]
        distances.sort(key=lambda x: x[1])
        car.checkpoint = distances[0][0]

        if distances[0][0] == self.road_length-2:
            if dist(self.path[self.road_length-1],car.position) < dist(self.path[car.checkpoint],car.position):
                car.checkpoint = self.road_length-1





