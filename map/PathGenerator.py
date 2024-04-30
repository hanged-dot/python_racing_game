import random
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from math import sqrt
from collections import deque
from map.randompointsgenerator import RandomPointsGenerator
from map.distance import dist, dist_point_segment


class PathGenerator:

    def __is_eligible_point__(self, v):
        if self.__parent__[v] != -1:
            p = self.__parent__[v]
            t = self.__parent__[p]
            dist_to_t = dist(self.__points__[p], self.__points__[t])

            while t != -1:
                if dist_point_segment(self.__points__[v], self.__points__[p], self.__points__[
                    t]) <= self.__path_width__ and dist_to_t > self.__shortening_tolerance__ * self.__path_width__:
                    return False

                dist_to_t += dist(self.__points__[t], self.__points__[self.__parent__[t]])
                t = self.__parent__[t]

            t = self.__parent__[v]
            dist_to_t = dist(self.__points__[v], self.__points__[t])

            while self.__parent__[t] != -1:
                if dist_point_segment(self.__points__[t], self.__points__[self.__parent__[t]], self.__points__[
                    v]) <= self.__path_width__ and dist_to_t > self.__shortening_tolerance__ * self.__path_width__:
                    return False

                dist_to_t += dist(self.__points__[t], self.__points__[self.__parent__[t]])
                t = self.__parent__[t]

        return True

    def __ancestors__(self, v):
        anc = []

        while v != -1:
            anc.append(v)
            v = self.__parent__[v]

        return anc

    def __find_path__(self):
        queue = [(i, 0) for i in range(self.__all_points__)]
        random.shuffle(queue)
        queue = deque(queue)

        self.__parent__ = [-1 for _ in range(self.__all_points__)]

        while (len(queue)):
            v, depth = queue.pop()
            anc = self.__ancestors__(v)

            if not self.__is_eligible_point__(v):
                continue

            if depth == self.__path_points__ - 1:
                return anc

            for u in self.__G__[v]:
                if u not in anc:
                    self.__parent__[u] = v
                    queue.append((u, depth + 1))

        return None

    def __graph_representation__(self, tri, n):
        G = [[] for _ in range(n)]

        for triple in tri.simplices:
            for i in range(3):
                for j in range(3):
                    if i != j and triple[j] not in G[triple[i]]:
                        G[triple[i]].append(triple[j])

        for L in G:
            random.shuffle(L)

        return G

    def __init__(self, width=600, height=600, path_width=30, all_points=1000, path_points=50, shortening_tolerance=1.2):
        self.__path_width__ = path_width  # 2 x path_radius
        self.__shortening_tolerance__ = shortening_tolerance
        self.__all_points__ = all_points
        self.__path_points__ = path_points

        self.__points__ = RandomPointsGenerator(width, height, all_points).get_positions()

        self.__G__ = self.__graph_representation__(Delaunay(np.array(self.__points__)), len(self.__points__))

        self.__path__ = self.__find_path__()

    def get_path(self):
        return [self.__points__[i] for i in self.__path__]
