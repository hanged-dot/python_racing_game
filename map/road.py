import pygame as pg
from map import config
from map.pathgenerator import PathGenerator


class Road():
    def __init__(self):
        self.path = PathGenerator(width=config.display_width,height=config.display_height,path_width=config.road_width).get_path()

    def draw_line(self,surf,p1,p2,c,w):
        p1v = pg.math.Vector2(p1)
        p2v = pg.math.Vector2(p2)
        lv = (p2v - p1v).normalize()
        lnv = pg.math.Vector2(-lv.y, lv.x) * w // 2
        pts = [p1v + lnv, p2v + lnv, p2v - lnv, p1v - lnv]
        pg.draw.polygon(surf, c, pts)
        pg.draw.circle(surf, c, p1, round(w / 2))
        pg.draw.circle(surf, c, p2, round(w / 2))

    def draw(self):
        for i in range(len(self.path)-1):
            self.draw_line(config.game_display,self.path[i],self.path[i+1],"orange",config.road_width)
