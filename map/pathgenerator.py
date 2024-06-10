import random
import numpy as np
from scipy.spatial import Delaunay
from math import sqrt
from collections import deque
from map.randompointsgenerator import RandomPointsGenerator
from map.distance import dist, dist_point_segment


class PathGenerator:

    def __is_eligible_point(self, v):
        if self.__parent[v] != -1:
            p = self.__parent[v]
            t = self.__parent[p]
            dist_to_t = dist(self.__points[p], self.__points[t])

            while t != -1:
                if dist_point_segment(self.__points[v], self.__points[p], self.__points[
                    t]) <= self.__path_width and dist_to_t > self.__shortening_tolerance * self.__path_width:
                    return False

                dist_to_t += dist(self.__points[t], self.__points[self.__parent[t]])
                t = self.__parent[t]

            t = self.__parent[v]
            dist_to_t = dist(self.__points[v], self.__points[t])

            while self.__parent[t] != -1:
                if dist_point_segment(self.__points[t], self.__points[self.__parent[t]], self.__points[
                    v]) <= self.__path_width and dist_to_t > self.__shortening_tolerance * self.__path_width:
                    return False

                dist_to_t += dist(self.__points[t], self.__points[self.__parent[t]])
                t = self.__parent[t]

        return True

    def __ancestors(self, v):
        anc = []

        while v != -1:
            anc.append(v)
            v = self.__parent[v]

        return anc

    def __find_path(self):
        queue = [(i, 0) for i in range(self.__all_points)]
        random.shuffle(queue)
        queue = deque(queue)

        self.__parent = [-1 for _ in range(self.__all_points)]

        while (len(queue)):
            v, depth = queue.pop()
            anc = self.__ancestors(v)

            if not self.__is_eligible_point(v):
                continue

            if depth == self.__path_points - 1:
                return anc

            for u in self.__G[v]:
                if u not in anc:
                    self.__parent[u] = v
                    queue.append((u, depth + 1))

        return None

    def __graph_representation(self, tri, n):
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
        self.__path_width = path_width  # 2 x path_radius
        self.__shortening_tolerance = shortening_tolerance
        self.__all_points = all_points
        self.__path_points = path_points
        self.__points = RandomPointsGenerator(width, height, all_points)._positions
        self.__G = self.__graph_representation(Delaunay(np.array(self.__points)), len(self.__points))

        self._path = [self.__points[i] for i in self.__find_path()]
