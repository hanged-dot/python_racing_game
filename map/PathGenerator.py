import random
import numpy as np
import matplotlib.pyplot as plt 
from scipy.spatial import Delaunay 
from math import sqrt
from collections import deque
from map.randompointsgenerator import RandomPointsGenerator
from map.distance import dist

class PathGenerator:
    def __dist_point_segment__(self,A,B,C): # distance from segment |AB| to point C assuming all coordinates > 0
        # równanie prostej l: A1x + B1y + C1 = 0, do prostej należą punkty A i B
        x1, y1 = A
        x2, y2 = B
        x3, y3 = C

        if x1/y1 == x2/y2:
            C1 = 0
            B1 = 1
            A1 = -y1/x1
        elif y1 == y2:
            A1 = 0
            B1 = 1
            C1 = -y1
        else:
            C1 = 1
            B1 = C1*(x2-x1)/(x1*y2 - x2*y1)
            A1 = (-B1*y1-C1)/x1
        
        # równanie prostej prostopadłej k: A2x + B2y + C2 = 0, do prostej należy punkt C

        if A1 == 0:
            A2 = 1
            B2 = 0
            C2 = -x3
        else:
            A2 = -B1/A1
            B2 = 1
            C2 = -A2*x3-B2*y3

        # punkt przecięcia

        if B1 == 0:
            x4 = -C1/A1
            y4 = (-C2-A2*x4)/B2
        else:
            x4 = (B2*C1-B1*C2)/(A2*B1-A1*B2)
            y4 = (-C1-A1*x4)/B1

        X = (x4,y4)

        # dystans

        if dist(A,X) < dist(A,B) and dist(B,X) < dist(A,B):
            return dist(C,X)

        return min(dist(A,C),dist(B,C))

    def __is_eligible_point__(self,v):
        if self.__parent__[v] != -1:
            p = self.__parent__[v]
            t = self.__parent__[p]
            dist_to_t = dist(self.__points__[p],self.__points__[t])

            while t != -1:
                if self.__dist_point_segment__(self.__points__[v],self.__points__[p],self.__points__[t]) <= self.__path_width__ and dist_to_t > self.__shortening_tolerance__*self.__path_width__:
                    return False

                dist_to_t += dist(self.__points__[t],self.__points__[self.__parent__[t]])
                t = self.__parent__[t]
                
            t = self.__parent__[v]
            dist_to_t = dist(self.__points__[v],self.__points__[t])

            while self.__parent__[t] != -1:
                if self.__dist_point_segment__(self.__points__[t],self.__points__[self.__parent__[t]],self.__points__[v]) <= self.__path_width__ and dist_to_t > self.__shortening_tolerance__*self.__path_width__:
                    return False

                dist_to_t += dist(self.__points__[t],self.__points__[self.__parent__[t]])
                t = self.__parent__[t]

        return True

    def __ancestors__(self,v):
        anc = []

        while v != -1:
            anc.append(v)
            v = self.__parent__[v]
        
        return anc

    def __find_path__(self):
        queue = [(i,0) for i in range(self.__all_points__)]
        random.shuffle(queue)
        queue = deque(queue)

        self.__parent__ = [-1 for _ in range(self.__all_points__)]

        while(len(queue)):
            v, depth = queue.pop()
            anc = self.__ancestors__(v)

            if not self.__is_eligible_point__(v):
                continue

            if depth == self.__path_points__-1:
                return anc

            for u in self.__G__[v]:
                if u not in anc:
                    self.__parent__[u] = v
                    queue.append((u,depth+1))

        return None

    def __graph_representation__(self,tri,n):
        G = [[] for _ in range(n)]

        for triple in tri.simplices:
            for i in range(3):
                for j in range(3):
                    if i != j and triple[j] not in G[triple[i]]:
                        G[triple[i]].append(triple[j])
        
        for L in G:
            random.shuffle(L)
        
        return G

    def __init__(self,width=600,height=600,path_width=30,all_points=1000,path_points=50,shortening_tolerance=1.2):
        self.__path_width__ = path_width # 2 x path_radius
        self.__shortening_tolerance__ = shortening_tolerance
        self.__all_points__ = all_points
        self.__path_points__ = path_points

        self.__points__ = RandomPointsGenerator(width,height,all_points).get_positions()

        self.__G__ = self.__graph_representation__(Delaunay(np.array(self.__points__)),len(self.__points__))

        self.__path__ = self.__find_path__()

    def get_path(self):
        return [self.__points__[i] for i in self.__path__]