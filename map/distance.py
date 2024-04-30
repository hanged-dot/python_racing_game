from math import sqrt

def dist(A,B):
    return sqrt((A[0]-B[0])**2+(A[1]-B[1])**2)

def dist_point_segment(A, B, C):  # distance from segment |AB| to point C assuming all coordinates > 0
    # równanie prostej l: A1x + B1y + C1 = 0, do prostej należą punkty A i B
    x1, y1 = A
    x2, y2 = B
    x3, y3 = C

    if x1 / y1 == x2 / y2:
        C1 = 0
        B1 = 1
        A1 = -y1 / x1
    elif y1 == y2:
        A1 = 0
        B1 = 1
        C1 = -y1
    else:
        C1 = 1
        B1 = C1 * (x2 - x1) / (x1 * y2 - x2 * y1)
        A1 = (-B1 * y1 - C1) / x1

    # równanie prostej prostopadłej k: A2x + B2y + C2 = 0, do prostej należy punkt C

    if A1 == 0:
        A2 = 1
        B2 = 0
        C2 = -x3
    else:
        A2 = -B1 / A1
        B2 = 1
        C2 = -A2 * x3 - B2 * y3

    # punkt przecięcia

    if B1 == 0:
        x4 = -C1 / A1
        y4 = (-C2 - A2 * x4) / B2
    else:
        x4 = (B2 * C1 - B1 * C2) / (A2 * B1 - A1 * B2)
        y4 = (-C1 - A1 * x4) / B1

    X = (x4, y4)

    # dystans

    if dist(A, X) < dist(A, B) and dist(B, X) < dist(A, B):
        return dist(C, X)

    return min(dist(A, C), dist(B, C))