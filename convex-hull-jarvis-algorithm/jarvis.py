# zadanie ukonczone

class Point:
    def __init__(self, key, xpos, ypos):
        self.key = key
        self.xpos = xpos
        self.ypos = ypos

    def __str__(self):
        return f"{self.key} ({self.xpos},{self.ypos})"

    def __eq__(self, other):
        return self.key == other.key and \
               self.xpos == other.xpos and self.ypos == other.ypos


class Space:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.points = []

    def insertPoint(self, point):
        if point.xpos > self.max_x or point.ypos > self.max_y:
            raise ValueError(f"Point {point} is outside the space.")
        self.points.append(point)
        return self

COLLINEAR = 0
CLOCKWISE = 1
COUNTERCLOCKWISE = 2

def isCounterclockwise(p,q,r):

    wzor = (q.ypos - p.ypos) * (r.xpos - q.xpos) - (q.xpos - p.xpos) * (r.ypos - q.ypos) 

    if wzor == 0:
        return COLLINEAR
    elif wzor > 0:
        return CLOCKWISE
    else:
        return COUNTERCLOCKWISE

def isBetween(p, q, r):
    x_wise = q.xpos <= max(p.xpos, r.xpos) and q.xpos >= min(p.xpos, r.xpos)    # is between p and r on X-axis?
    y_wise = q.ypos <= max(p.ypos, r.ypos) and q.ypos >= min(p.ypos, r.ypos)    # is between p and r on Y-axis?
    return (x_wise and y_wise)  # if both are True, then q is between p and r


"""
Jarvis()
"""

def Jarvis(S:Space):

    n = len(S.points)

    if n < 3:
        raise ValueError("There must be at least 3 points to construct a hull.")

    f_point = Point('ERR', S.max_x, S.max_y)
    path = []

    for p in S.points:
        if p.xpos < f_point.xpos:
            f_point = p
        if p.xpos == f_point.xpos:
            if p.ypos < f_point.ypos:
                f_point = p

    p = S.points.index(f_point)
    q = 0

    while True:
        path.append(S.points[p])
        q = (p+1) % n
        for i in range(n):
            if isCounterclockwise(S.points[p], S.points[i], S.points[q]) == COUNTERCLOCKWISE:
                q = i
        p = q
        if p == S.points.index(f_point):
            break
        
    return path




"""
JarvisMod()
"""

def JarvisMod(S:Space):

    n = len(S.points)

    if n < 3:
        raise ValueError("There must be at least 3 points to construct a hull.")

    f_point = Point('ERR', S.max_x, S.max_y)
    path = []

    for p in S.points:
        if p.xpos < f_point.xpos:
            f_point = p
        if p.xpos == f_point.xpos:
            if p.ypos < f_point.ypos:
                f_point = p

    p = S.points.index(f_point)
    q = 0

    while True:
        path.append(S.points[p])
        q = (p+1) % n
        for i in range(n):
            if isCounterclockwise(S.points[p], S.points[i], S.points[q]) == COUNTERCLOCKWISE:
                q = i
            if p != i and \
                isCounterclockwise(S.points[p], S.points[i], S.points[q]) == COLLINEAR and \
                isBetween(S.points[p], S.points[q], S.points[i]):
                    q = i
        p = q
        if p == S.points.index(f_point):
            break
        
    return path




def test1():
    pts1 = [('A',0, 3), ('B',0, 0), ('C',0, 1), ('D',3, 0), ('E',3, 3)]
    S1 = Space(10,10)
    for pt in pts1:
        S1.insertPoint(Point(pt[0], pt[1], pt[2]))

    pts2 = [('A',0, 3), ('B',0, 1), ('C',0, 0), ('D',3, 0), ('E',3, 3)]
    S2 = Space(10,10)
    for pt in pts2:
        S2.insertPoint(Point(pt[0], pt[1], pt[2]))

    print([f"({el.xpos},{el.ypos})" for el in Jarvis(S1)])
    print([f"({el.xpos},{el.ypos})" for el in Jarvis(S2)])

    print()

    print([f"({el.xpos},{el.ypos})" for el in JarvisMod(S1)])
    print([f"({el.xpos},{el.ypos})" for el in JarvisMod(S2)])

    print()
test1()

def test2():
    pts = [('A',4,3), ('B',3,1), ('C',5,1), ('D',1,0), ('E',7,2), ('F',6,4),
    ('G',5,5), ('H',3,5), ('I',2,4), ('J',1,2)]

    S = Space(10,10)
    for pt in pts:
        S.insertPoint(Point(pt[0], pt[1], pt[2]))
    
    # print([f"{el}" for el in S.points])
    
    print([f"({el.xpos},{el.ypos})" for el in Jarvis(S)])
    print([f"({el.xpos},{el.ypos})" for el in JarvisMod(S)])

test2()
