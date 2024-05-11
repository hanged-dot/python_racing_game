import random

class RandomPointsGenerator:
    def __init__(self,width,height,count):
        self._positions = self.__all_positions(width,height)
        random.shuffle(self._positions)
        self._positions = self._positions[:count]

    def __all_positions(self,width,height):
        P = []

        for x in range(1,width+1):
            for y in range(1,height+1):
                P.append((x,y))

        return P