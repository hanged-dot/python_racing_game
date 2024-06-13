import pygame as pg
from map.pathgenerator import PathGenerator
from map.distance import dist, dist_point_segment


class Road:
    def __init__(self, road_length, road_width, max_speed, zoom, display):
        self.__length = road_length
        self.__zoom = zoom
        self.__width = road_width
        self.__wholepath = PathGenerator(shortening_tolerance=1, path_points=self.__length, width=1500, height=1500,
                                         all_points=3000, path_width=road_width + max_speed)
        self.__path = self.__wholepath._path
        self.__dist_to_goal = [0 for _ in range(len(self.__path))]
        self.__display = display
        self.__road_width = road_width
        self.update_surface()

        for i in range(len(self.__path) - 2, -1, -1):
            self.__dist_to_goal[i] = self.__dist_to_goal[i + 1] + dist(self.__path[i + 1], self.__path[i])

    def get_path(self):
        return self.__path

    def get_length(self):
        return self.__length

    def get_zoom(self):
        return self.__zoom

    def check_for_checkpoints(self, car):
        return self.checkpoints(car)

    def check_boundaries(self, car):
        distances = [dist_point_segment(self.__path[i], self.__path[i + 1], car.get_position()) for i in
                     range(len(self.__path) - 1)]

        if min(distances) > self.__width / 2:
            car.move_to_checkpoint()

    def __draw_line(self, p1, p2):
        c = "orange"
        w = self.__width * self.__zoom
        p1v = pg.math.Vector2(p1)
        p2v = pg.math.Vector2(p2)
        lv = (p2v - p1v).normalize()
        lnv = pg.math.Vector2(-lv.y, lv.x) * w // 2
        pts = [p1v + lnv, p2v + lnv, p2v - lnv, p1v - lnv]
        pg.draw.polygon(self.__surface, c, pts)
        pg.draw.circle(self.__surface, c, p1, round(w / 2))
        pg.draw.circle(self.__surface, c, p2, round(w / 2))

    def draw(self, center):
        self.__display.display.blit(self.__surface, (-self.__zoom * center[0] - self.__road_width / 2 * self.__zoom,
                                                     -self.__zoom * center[1] - self.__road_width / 2 * self.__zoom))

    def checkpoints(self, car):
        distances = [(i, dist_point_segment(self.__path[i], self.__path[i + 1], car.get_position())) for i in
                     range(len(self.__path) - 2, -1, -1)]
        distances.sort(key=lambda x: x[1])
        car.set_checkpoint(distances[0][0])
        car.set_dist_to_goal(self.__dist_to_goal[car.get_checkpoint() + 1] + dist(car.get_position(), self.__path[
            car.get_checkpoint() + 1]))

        if distances[0][0] == self.__length - 2:
            if dist(self.__path[self.__length - 1], car.get_position()) < dist(self.__path[car.get_checkpoint()],
                                                                               car.get_position()):
                car.set_checkpoint(self.__length - 1)
                car.set_dist_to_goal(dist(car.get_position(), self.__path[-1]))

    def update_surface(self):
        self.__surface = pg.surface.Surface(((1500 + self.__road_width) * self.__zoom + self.__display.width / 2,
                                             (1500 + self.__road_width) * self.__zoom + self.__display.height / 2),
                                            pg.SRCALPHA)
        for i in range(len(self.__path) - 1):
            p1 = [self.__path[i][0] * self.__zoom + self.__display.width / 2 + self.__road_width / 2 * self.__zoom,
                  self.__path[i][1] * self.__zoom + self.__display.height / 2 + self.__road_width / 2 * self.__zoom]
            p2 = [self.__path[i + 1][0] * self.__zoom + self.__display.width / 2 + self.__road_width / 2 * self.__zoom,
                  self.__path[i + 1][1] * self.__zoom + self.__display.height / 2 + self.__road_width / 2 * self.__zoom]
            self.__draw_line(p1, p2)
