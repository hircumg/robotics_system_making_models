import matplotlib.pyplot as plt
import numpy as np
from math import atan2, sin, cos, sqrt

def plot_lines(lines,inc_lines, borders=None, middle_point=None):
    """
    Plotting border of slice
    :param lines: array of lines for plotting
    :return: nothing
    """
    if lines is not None:
        for line in lines:
            plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='o',
                     markerfacecolor='red', markersize=1, color='skyblue', linewidth=4)
     # plt.plot(all_lines, marker='o', markerfacecolor='red', markersize=5, color='skyblue', linewidth=4)

    if inc_lines is not None:
        for line in inc_lines:
            plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='.',
                     markerfacecolor='red', markersize=1, color='skyblue', linewidth=2)
     # plt.plot(all_lines, marker='o', markerfacecolor='red', markersize=5, color='skyblue', linewidth=4)

    if borders is not None:
        if borders is not None:
            for lines in borders:
                for line in lines:
                    plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='o',
                             markerfacecolor='black', markersize=2, color='red', linewidth=1)

    if middle_point is not None:

        plt.plot([middle_point[0]], [middle_point[1]], marker='.', markerfacecolor='yellow', markersize=10)

    plt.axis([-1, 101, -1, 101])
    plt.show()


def plot_borders(array_of_lines, borders = None, middle_point=None):
    """
    Plotting border of slice
    :param lines: array of lines for plotting
    :return: nothing
    """
    if array_of_lines is not None:
        for lines in array_of_lines:
            for line in lines:
                plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='.',
                         markerfacecolor='black', markersize=1, color='red', linewidth=1)
     # plt.plot(all_lines, marker='o', markerfacecolor='red', markersize=5, color='skyblue', linewidth=4)

    # if borders is not None:
    #     for line in borders:
    #         plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='o',
    #                  markerfacecolor='skyblue', markersize=3, color='black', linewidth=1)

    if middle_point is not None:
        plt.plot([middle_point[0]], [middle_point[1]], marker='.', markerfacecolor='yellow', markersize=10)

    plt.axis([-1, 101, -1, 101])
    plt.show()

def is_inside(point, polygon):
    """
    Check is given 2d point inside given polygon or not
    :param point: 2d point for check
    :param polygon: list of lines of polygons
    :return: boolean value: 1 if point is inside polygon otherwise will be returned 0
    """
    c_west = 0
    i = 0
    for line in polygon:
        if abs(line[1][1] - line[0][1]) > 0.001:
            x_int = line[0][0] + (point[1] - line[0][1]) * (line[1][0] - line[0][0]) / (line[1][1] - line[0][1])
            if abs(line[1][0] - line[0][0]) < 0.001:
                # parralel Ox
                x_int = line[1][0]

            if ((min(line[0][0], line[1][0]) <= x_int) and
                    (max(line[0][0], line[1][0]) >= x_int) and
                    (min(line[0][1], line[1][1]) <= point[1]) and
                    (max(line[0][1], line[1][1]) >= point[1]) and
                    (x_int <= point[0])):
                c_west = 1 - c_west
                # print(i, x_int, line[0][0], line[1][0], c_west)

        i += 1
    return c_west


def get_avg(borders):
    borders_reshaped = borders.reshape(-1, 2)
    x_borders = borders_reshaped[::,:1:].reshape(-1)
    y_borders = borders_reshaped[::,1::].reshape(-1)
    x_agv = (x_borders.max() + x_borders.min())/2
    y_agv = (y_borders.max() + y_borders.min())/2
    return np.array([x_agv, y_agv])

borders = np.array([[[0, 0], [0, 100]], [[0, 100],[100, 100]],
                    [[100, 100],[100, 0]], [[100, 0],[0, 0]]])
borders2 = np.array([[[0, 10], [0, 100]], [[0, 100],[100, 100]],
                    [[100, 100],[100, 0]], [[100, 0],[10, 0]],
                     [[10, 0], [0, 10]]])

# lines_15 = np.load('lines_15.txt', allow_pickle=True)
# plot_lines(lines_15, borders)

examples = ['lines_15.txt', 'lines_55.txt', 'lines_10.txt', 'lines_45.txt']
# examples = ['lines_10.txt', 'lines_45.txt']

# for ex in examples:
#     lines = np.load(ex, allow_pickle=True)
#     print(get_avg(lines))
#     plot_lines(lines, borders2)
#     # print(lines)

def create_milling_line(lines, distance, middle_point, object=None, repeats = -1):
    array_of_lines = []
    if repeats == -1:
        i = 0
        dst = True
        while dst:
            new_lines = []
            for line in lines:
                new_line = []
                for point in line:
                    atg = atan2(middle_point[1] - point[1], middle_point[0] - point[0])
                    new_point = [point[0] + distance * i * cos(atg), point[1] + distance * i * sin(atg)]
                    dst = (new_point[1] - middle_point[1])**2 + (new_point[0] - middle_point[1])**2 > distance**2
                    # print(f"new_point: {new_point}, dst: {dst}")
                    new_line.append(new_point)
                if object is None or ((not is_inside(new_line[0],object)) and (not is_inside(new_line[1], object))):
                    new_lines.append(new_line)
            array_of_lines.append(np.array(new_lines))
            i +=1

    else:
        for i in range(repeats):
            new_lines = []
            for line in lines:
                new_line = []
                for point in line:
                    atg =atan2(middle_point[1]-point[1],middle_point[0]-point[0])
                    new_line.append([point[0]+distance*i*cos(atg), point[1]+distance*i*sin(atg)])
                new_lines.append(new_line)
            array_of_lines.append(np.array(new_lines))

    return array_of_lines
    
def add_offset(lines, distance, middle_point):
    new_lines = []
    for line in lines:
        new_line = []
        for point in line:
            atg = atan2(middle_point[1] - point[1], middle_point[0] - point[0])
            new_line.append([point[0] + distance  * cos(atg), point[1] + distance  * sin(atg)])
        new_lines.append(new_line)
    return new_lines


def line_intersects(border_line, object_line):
    x1,y1 = border_line[0]
    x2,y2 = border_line[1]
    x3,y3 = object_line[0]
    x4,y4 = object_line[1]
    numerator = (x4-x3)*(y1-y3) - (y4 - y3)*(x1-x3)
    denominator = (y4-y3)*(x2-x1) - (x4-x3) * (y2-y1)
    if denominator != 0:
        u_a = numerator/denominator
        if u_a >= 0 and u_a <= 1:
            x = x1 + u_a * (x2 - x1)
            y = y1 + u_a * (y2 - y1)

            numerator = (x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)
            u_b = numerator / denominator
            if u_b >= 0 and u_b <= 1:
                return np.array([x, y])
    return None

def check_point_ends(point, line):
    for p in line:
        if point[0] == p[0] and point[1] == p[1]:
            return True
    return False

def update_intersections(borders, inc_object):
    new_borders = []
    for border in borders:
        new_border = []
        for i,b_line in enumerate(border):
            t_border = []
            was_intersect = False
            b_line_copy = b_line
            for j,line in enumerate(inc_object):
                point = line_intersects(b_line_copy,line)
                if not was_intersect:
                    if point is not None:
                        was_intersect = True
                        if i == 0:
                            if check_point_ends(b_line_copy[0],border[i+1]):
                                t_border.append([b_line[1], point])
                                b_line = [b_line[0], point]
                            else:
                                t_border.append([b_line[0], point])
                                b_line = [point, b_line[1]]
                        else:
                            if check_point_ends(b_line_copy[0],border[i-1]):
                                t_border.append([b_line[0], point])
                                b_line = [point, b_line[1]]
                            else:
                                t_border.append([b_line[1], point])
                                b_line = [b_line[0], point]

                        if j == 0:
                            if check_point_ends(line[0],inc_object[j+1]):
                                t_border.append([line[0],point])
                            else:
                                t_border.append([point,line[1]])
                        else:
                            if check_point_ends(line[0],inc_object[j-1]):
                                t_border.append([point,line[1]])
                            else:
                                t_border.append([line[0], point])

                else:
                    if point is None:
                        t_border.append(line)
                    else:
                        was_intersect = False
                        if j == 0:
                            if check_point_ends(line[0],inc_object[j+1]):
                                t_border.append([line[1],point])
                            else:
                                t_border.append([point,line[0]])
                        else:
                            if check_point_ends(line[0],inc_object[j-1]):
                                t_border.append([point,line[0]])
                            else:
                                t_border.append([line[1],point])

                        if i == 0:
                            if check_point_ends(b_line_copy[0],border[i+1]):
                                # t_border.append([b_line_copy[1], point])
                                b_line = [b_line[0], point]
                            else:
                                # t_border.append([b_line_copy[0], point])
                                b_line = [point, b_line[1]]
                        else:
                            if check_point_ends(b_line_copy[0],border[i-1]):
                                # t_border.append([b_line_copy[0], point])
                                b_line = [point, b_line[1]]
                            else:
                                # t_border.append([b_line_copy[1], point])
                                b_line = [b_line[0], point]
            t_border.append(b_line)
            new_border += t_border

        new_borders.append(new_border)
    return new_borders



threshold = 0.15
milling_diameter = 10
distance = milling_diameter - milling_diameter*threshold
object_offset = -milling_diameter/2 - 1
middle_point = get_avg(borders2)
object = np.load(examples[1], allow_pickle=True)
object_middle_point = get_avg(object)
inc_object = add_offset(object,object_offset, object_middle_point)
new_lines =create_milling_line(borders2,distance,middle_point,inc_object)
plot_lines(object, inc_object,borders=new_lines, middle_point=middle_point)

updated_borders = update_intersections(new_lines,inc_object)
plot_lines(object, inc_object,borders=updated_borders, middle_point=middle_point)
