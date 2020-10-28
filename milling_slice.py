
import matplotlib.pyplot as plt
import numpy as np
from math import atan2, sin, cos, sqrt, ceil

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300

def plot_lines(lines,inc_lines, borders=None, middle_point=None):
    """
    Plotting border of slice
    :param lines: array of lines for plotting
    :return: nothing
    """
    if lines is not None:
        for line in lines:
            plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='.',
                     markerfacecolor='red', markersize=1, color='yellow', linewidth=1)
     # plt.plot(all_lines, marker='o', markerfacecolor='red', markersize=5, color='skyblue', linewidth=4)

    if inc_lines is not None:
        for line in inc_lines:
            plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='o',
                     markerfacecolor='red', markersize=1, color='skyblue', linewidth=1)
     # plt.plot(all_lines, marker='o', markerfacecolor='red', markersize=5, color='skyblue', linewidth=4)

    if borders is not None:
        if borders is not None:
            for lines in borders:
                for line in lines:
                    plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='o',
                             markerfacecolor='black', markersize=1, color='red', linewidth=1)

    if middle_point is not None:

        plt.plot([middle_point[0]], [middle_point[1]], marker='.', markerfacecolor='yellow', markersize=10)

    # plt.axis([-1, 101, -1, 101])
    # plt.axis([-21, 121, -21, 121])
    plt.axis([-6, 106, -6, 106])
    # plt.axis([-21, 21, 81, 121])
    plt.show()

def plot_lines_new(lines,inc_lines, borders=None, clear_border=None, middle_point=None):
    """
    Plotting border of slice
    :param lines: array of lines for plotting
    :return: nothing
    """
    if lines is not None:
        for line in lines:
            plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='.',
                     markerfacecolor='red', markersize=1, color='yellow', linewidth=1)
     # plt.plot(all_lines, marker='o', markerfacecolor='red', markersize=5, color='skyblue', linewidth=4)

    if inc_lines is not None:
        for line in inc_lines:
            plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='o',
                     markerfacecolor='red', markersize=1, color='skyblue', linewidth=1)
     # plt.plot(all_lines, marker='o', markerfacecolor='red', markersize=5, color='skyblue', linewidth=4)

    if borders is not None:
        for i,line in enumerate(borders):

            plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='o',
                     markerfacecolor='black', markersize=1 if i > 0 else 3, color='red', linewidth=1)

    if clear_border is not None:
        for i,line in enumerate(clear_border):
            plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='o',
                     markerfacecolor='black', markersize=1 if i > 0 else 3, color='green', linewidth=1)

    if middle_point is not None:

        plt.plot([middle_point[0]], [middle_point[1]], marker='.', markerfacecolor='yellow', markersize=10)

    # plt.axis([-1, 101, -1, 101])
    # plt.axis([-21, 121, -21, 121])
    plt.axis([-6, 106, -6, 106])
    # plt.axis([-21, 21, 81, 121])
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

def get_max_distance(lines, middle_point):
    points = np.unique(lines.reshape(-1,2), axis=0)
    max_dst = -1
    point_bigger = None
    for point in points:
        dst = np.sqrt(np.sum((point - middle_point) ** 2))
        if dst > max_dst:
            max_dst = dst
            point_bigger = point

    return max_dst


def get_min_distance(lines, middle_point):
    points = np.unique(lines.reshape(-1,2), axis=0)
    max_dst = 10000
    point_bigger = None
    for point in points:
        dst = np.sqrt(np.sum((point - middle_point) ** 2))
        if dst < max_dst:
            max_dst = dst
            point_bigger = point

    return max_dst

def generate_steps(object_projection, lines, num, middle_point, initial_distance):
    steps = []
    for i,line in enumerate(lines):
        cur_steps = []
        for j,point in enumerate(line):
            max_dist = np.sqrt(np.sum((object_projection[i][j] - middle_point) ** 2))
            dst = np.sqrt(np.sum((lines[i][j] - middle_point) ** 2))
            extra= max_dist - dst
            # extra = extra if extra > initial_distance/2 else initial_distance/2
            extra = extra if extra > 0 else 0
            new_step = round(extra / num, 2)
            cur_steps.append(new_step)
        steps.append(cur_steps)
    return steps

def calc_dist(point1, point2):
    point1 = np.array(point1)
    point2 = np.array(point2)
    return np.sqrt(np.sum((point1 - point2) ** 2))

def calc_dict_bw_lines(line1, line2):
    return min(min(calc_dist(line1[0], line2[0]),calc_dist(line1[0], line2[1])),
                min(calc_dist(line1[1], line2[0]),calc_dist(line1[1], line2[1])))

def create_milling_line(lines, distance, middle_point, last_border, milling_diam):
    array_of_lines = []
    first_point = []
    last_point = []
    # i = 0
    dst = True
    max_dst = get_max_distance(last_border,middle_point) - distance*0.25
    extra = max_dst-get_min_distance(np.array(lines),middle_point)
    num = ceil((max_dst-get_min_distance(np.array(lines),middle_point))/distance)
    new_step = round(extra/num,2)
    print(extra, num, distance, new_step, extra/new_step)
    distance = new_step
    object_projection = get_object_projection(lines,middle_point,last_border)
    steps = generate_steps(object_projection,lines,num,middle_point, distance)
    # print(max_dst, (max_dst-get_min_distance(np.array(lines),middle_point)),
    #       (max_dst-get_min_distance(np.array(lines),middle_point))/distance)
    # print(get_min_distance(np.array(lines),middle_point), get_max_distance(np.array(lines),middle_point))
    # while dst:
    len_of_lines = len(lines)

    for i in range(num+1):
        new_lines = []
        for j,line in enumerate(lines):
            new_line = []
            for k,point in enumerate(line):
                cur_distance = steps[j][k]
                # cur_distance = distance
                atg = atan2(middle_point[1] - point[1], middle_point[0] - point[0])
                new_point = [point[0] - cur_distance * i * cos(atg), point[1] - cur_distance * i * sin(atg)]
                # dst = np.sum((new_point - middle_point) **2 ) < max_dst**2
                # print(f"new_point: {new_point}, dst: {dst}")
                new_line.append(new_point)
            # if last_border is None or ((not is_inside(new_line[0], last_border)) and (not is_inside(new_line[1], last_border))):

            if j == 1:
                if abs(calc_dist(new_lines[0][0], new_line[0])) < 0.0001:
                    first_point.append(new_lines[0][0])
                else:
                    first_point.append(new_lines[0][1])



            # if j > len_of_lines//2 and (calc_dict_bw_lines(new_line,new_lines[0]) < distance):
            if i != 0 and j >= len_of_lines//2 and \
                    (min(calc_dist(first_point[i], new_line[0]),calc_dist(first_point[i], new_line[1])) <= distance/2.0):
                d1 = calc_dist(first_point[i], new_line[0])
                d2 = calc_dist(first_point[i], new_line[1])
                x0, y0 = new_line[0]
                x1, y1 = new_line[1]
                x2, y2 = first_point[i]
                R = distance/2.0
                Lk = (y1 - y0)/(x1- x0)
                Lb = y0 - x0 * (y1-y0)/(x1-x0)
                Da = 1 + Lk**2
                Db = Lk*Lb - y2 * Lk - x2
                Dc = Lb**2 + y2**2 + x2**2 - R**2 -2 * y2 * Lb
                D = Db**2 - Da * Dc
                D = sqrt(D)
                x = [(-Db - D)/(Da), (-Db + D)/(Da)]
                y = [Lk * x[0] + Lb, Lk * x[1] + Lb]
                if x[0] >= min(x0,x1) and x[0] <= max(x0,x1) and y[0] >= min(y0,y1) and y[0] <= max(y0,y1):
                    last_point_t = [x[0], y[0]]
                else:
                    last_point_t = [x[1], y[1]]
                last_point.append(last_point_t)

                if calc_dist(first_point[i], new_line[0]) <= distance/2.0:
                    new_line = [new_line[1], last_point_t]
                else:
                    new_line = [new_line[0], last_point_t]

                # if i != 0:
                    # to close the pre-cleaning path
                new_lines.append(new_line)
                break
            new_lines.append(new_line)
        if i == 0:
            last_point.append(first_point[i])
        print(f"{i}: {len(first_point)}|{len(last_point)} ")



        array_of_lines.append(new_lines)
        dst = get_min_distance(np.array(new_lines), middle_point) < max_dst
        # i +=1
        # print(i, dst, get_min_distance(np.array(new_lines), middle_point))
    print(f"Extended: {i} times")

    array_of_lines.reverse()

    first_point.reverse()
    last_point.reverse()
    new_array_of_lines = []
    for i in range(len(array_of_lines)-1):
        new_array_of_lines += array_of_lines[i]
        new_array_of_lines += [[last_point[i], first_point[i+1]]]
    new_array_of_lines += array_of_lines[-1]
    new_array_of_lines = np.array(new_array_of_lines)
    return new_array_of_lines, last_point[-1]


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
        # if u_a >= 0 and u_a <= 1:
        x = x1 + u_a * (x2 - x1)
        y = y1 + u_a * (y2 - y1)

        numerator = (x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)
        u_b = numerator / denominator
        # if u_b >= 0 and u_b <= 1:
        return np.array([x, y]), u_b
    return None, None


def get_object_projection(lines, middle_point, borders):
    new_lines = []
    for line in lines:
        c_line = []
        for point in line:
            new_point_min = None
            u_b_min = 1000
            for border in borders:
                new_point, u_b = line_intersects(border, [middle_point, point])
                if new_point is not None and u_b > 0 and u_b < u_b_min:
                    new_point_min = new_point
                    u_b_min = u_b
            c_line.append(new_point_min)
        new_lines.append(np.array(c_line))

    return new_lines


clear_offset = 1
threshold = 1 - 0.15
milling_diameter = 10
distance = milling_diameter*threshold
object_offset = -milling_diameter/2 - clear_offset
middle_point = get_avg(borders2)
object = np.load(examples[2], allow_pickle=True)
object_middle_point = get_avg(object)

inc_object = add_offset(object,object_offset, object_middle_point)
new_lines, last_point = create_milling_line(inc_object,distance,middle_point,borders2, milling_diameter)

# add clear path
clear_border  = add_offset(object,object_offset+clear_offset,object_middle_point)
# plot_lines(object, borders2,borders=new_lines, middle_point=middle_point)

object_projection = get_object_projection(inc_object,middle_point,borders2)
plot_lines_new(object, object_projection,borders=new_lines,clear_border=clear_border, middle_point=middle_point)
