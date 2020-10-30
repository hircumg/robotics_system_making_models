import numpy as np

def is_inside(point, polygon):
    """
    Check is given 2d point inside given polygon or not
    :param point: 2d point for check
    :param polygon: list of lines of polygons
    :return: boolean value: 1 if point is inside polygon otherwise will be returned 0
    """
    c_west = 0
    for line in polygon:
        if abs(line[1][1] - line[0][1]) > 0.0001:
            # direct the beam along the x-axis in the negative direction

            x_int = line[0][0] + (point[1] - line[0][1]) * (line[1][0] - line[0][0]) / (line[1][1] - line[0][1])
            # if abs(line[1][0] - line[0][0]) < 0.0001:
            #     # parralel Ox
            #     x_int = line[1][0]

            if ((min(line[0][0], line[1][0]) <= x_int) and
                    (max(line[0][0], line[1][0]) >= x_int) and
                    (min(line[0][1], line[1][1]) <= point[1]) and
                    (max(line[0][1], line[1][1]) >= point[1]) and
                    (x_int <= point[0])):
                c_west = 1 - c_west
                # print(i, x_int, line[0][0], line[1][0], c_west)
        else:
            if min(line[0][0], line[1][0]) <= point[0]:
                c_west = 1 - c_west

    return c_west

def is_inside_by_points(point, border):
    """
    Check is given 2d point inside given polygon or not
    :return: boolean value: 1 if point is inside polygon otherwise will be returned 0
    """
    polygon = []
    for i in range(1,len(border)):
        polygon.append([border[i-1], border[i]])
    return  is_inside(point, polygon)



def line_intersects(border_line, object_line):
    x1,y1 = border_line[0]
    x2,y2 = border_line[1]
    x3,y3 = object_line[0]
    x4,y4 = object_line[1]
    numerator = (x4-x3)*(y1-y3) - (y4 - y3)*(x1-x3)
    denominator = (y4-y3)*(x2-x1) - (x4-x3) * (y2-y1)
    if denominator != 0:
        u_a = numerator/denominator
        # if u_a >= 0 and u_a <= 1:
        x = x1 + u_a * (x2 - x1)
        y = y1 + u_a * (y2 - y1)

        numerator = (x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)
        u_b = numerator / denominator
        if u_b >= 0 and u_b <= 1 and u_a >=0 and u_a <= 1:
            return np.array([x, y]), u_a, u_b
    return None, None, None
