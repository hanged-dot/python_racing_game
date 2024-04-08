import pygame as pg
import typing
from map.config import Way
from map.road import Road


class Grid:  # set up route for cars with checkpoints
    def __init__(self, width: int, height: int, list: typing.List[typing.Tuple[int, int, Way]]):
        self.width = width
        self.height = height
        self.cell_height = 256
        self.cell_width = 256
        self.list = list
        self.checkpoints = []
        self.roads = []

    def create_checkpoint(self):
        for i in self.list:
            if self.switch_way(i[2]) == 1:
                self.checkpoints.append(((i[0], i[1]), (i[0] + self.cell_height, i[1] + self.cell_width)))
            elif self.switch_way(i[2]) == 2:
                self.checkpoints.append(((i[0] + self.cell_height, i[1]), (i[0], i[1] + self.cell_width)))
            elif self.switch_way(i[2]) == 3:
                self.checkpoints.append(
                    ((i[0] + self.cell_height / 2, i[1]), (i[0] + self.cell_height / 2, i[1] + self.cell_width)))
            else:
                self.checkpoints.append(
                    ((i[0], i[1] + self.cell_width / 2), (i[0] + self.cell_height, i[1] + self.cell_width / 2)))

    def switch_way(self, way: Way):
        match way:
            case 0:  # down_left
                return 2  # checkpoint line diagonally from bottom left to upper right
            case 1:  # down_right
                return 1  # checkpoint line diagonally from upper left to bottom right
            case 2:  # side
                return 4  # checkpoint line vertical in the middle
            case 3:  # up
                return 3  # checkpoint line horizontal in the middle
            case 4:  # up_left
                return 1  # checkpoint line diagonally from upper left to bottom right
            case 5:  # up_right
                return 2  # checkpoint line diagonally from bottom left to upper right

    def create_road(self):
        for i in self.list:
            road_to_add = Road(i[0], i[1], i[3])
            self.roads.append(road_to_add)

    def draw_grid(self):
        for i in self.roads:
            i.draw()
