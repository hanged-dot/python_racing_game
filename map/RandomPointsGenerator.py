import random

class RandomPointsGenerator:
    def __init__(self,width,height,count):
        self.P = self.__all_positions__(width,height)
        random.shuffle(self.P)
        self.P = self.P[:count]

    def __all_positions__(self,width,height):
        P = []

        for x in range(1,width+1):
            for y in range(1,height+1):
                P.append((x,y))

        return P
    
    def get_positions(self):
        return self.P