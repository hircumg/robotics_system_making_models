from numpy import array, sin, cos

def tz(l):
    return array([[1, 0, 0, 0],
                   [0, 1, 0, 0],
                   [0, 0, 1, l],
                   [0, 0, 0, 1]])


def tx(l):
    return array([[1, 0, 0, l],
                   [0, 1, 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])

def ty(l):
    return array([[1, 0, 0, 0],
                   [0, 1, 0, l],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]])    


def rz(q):
    return array([[cos(q), -sin(q), 0, 0],
                   [sin(q), cos(q), 0, 0],
                   [0, 0, 1, 0],
                   [0, 0, 0, 1]
                   ])


def ry(q):
    return array([[cos(q), 0, sin(q), 0],
                   [0, 1, 0, 0],
                   [-sin(q), 0, cos(q), 0],
                   [0, 0, 0, 1]
                   ])


def rx(q):
    return array([[1, 0, 0, 0],
                   [0, cos(q), -sin(q), 0],
                   [0, sin(q), cos(q), 0],
                   [0, 0, 0, 1]
                   ])