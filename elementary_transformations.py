from numpy import array, sin, cos
import numpy as np


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



def getMatrix(p1, p2, p3):
    translation = tx(p1[0]).dot(ty(p1[1])).dot(tz(p1[2]))

    x_new = p3 - p1
    x_new = x_new / np.linalg.norm(x_new)
    x_old = np.array([1, 0, 0])

    angle_z = np.arctan2(x_new[1], x_new[0])

    rz_current = rz(angle_z)[0:3, 0:3]
    vector_current = rz_current.dot(x_old)

    angle_y = np.arctan2(-x_new[2], np.sqrt(x_new[0] ** 2 + x_new[1] ** 2))

    ry_current = ry(angle_y)[0:3, 0:3]

    y_new = p2 - p1
    y_new = y_new / np.linalg.norm(y_new)

    angle_x = np.arctan2(y_new[2], np.sqrt(y_new[0] ** 2 + y_new[1] ** 2))


    rotation = rx(angle_x).dot(ry(angle_y)).dot(rz(angle_z))
    H = translation.dot(rotation)
    # print(H)
    return H
