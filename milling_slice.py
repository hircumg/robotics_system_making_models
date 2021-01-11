
import matplotlib.pyplot as plt
import numpy as np
from math import atan2, sin, cos, sqrt, ceil

import matplotlib as mpl

from union_of_sections import to_points_shape

mpl.rcParams['figure.dpi'] = 300

def plot_lines(lines,inc_lines, borders=None, middle_point=None):
    """
    Plotting border of slice
    :param lines: array of lines for plotting
    :return: nothing
    """
    if lines is not None:
        for t_lines in lines:
            for line in t_lines:
                plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='.',
                         markerfacecolor='red', markersize=1, color='red', linewidth=1)
     # plt.plot(all_lines, marker='o', markerfacecolor='red', markersize=5, color='skyblue', linewidth=4)

    if inc_lines is not None:
        for line in inc_lines:
            plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='o',
                     markerfacecolor='red', markersize=1, color='skyblue', linewidth=2)
     # plt.plot(all_lines, marker='o', markerfacecolor='red', markersize=5, color='skyblue', linewidth=4)

    if borders is not None:
        if borders is not None:
            for lines in borders:
                for line in lines:
                    plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='o',
                             markerfacecolor='black', markersize=1, color='y', linewidth=1)

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




def get_avg(borders):
    borders_reshaped = borders.reshape(-1, 2)
    x_borders = borders_reshaped[::,:1:].reshape(-1)
    y_borders = borders_reshaped[::,1::].reshape(-1)
    x_agv = (x_borders.max() + x_borders.min())/2
    y_agv = (y_borders.max() + y_borders.min())/2
    return np.array([x_agv, y_agv])


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

def generate_steps(object_projection, lines, num, middle_point, initial_distance,distance):
    steps = []
    for i,line in enumerate(lines):
        cur_steps = []
        for j,point in enumerate(line):
            max_dist = np.sqrt(np.sum((object_projection[i][j] - middle_point) ** 2))
            dst = np.sqrt(np.sum((lines[i][j] - middle_point) ** 2))
            extra= max_dist - dst
            # extra = extra if extra > initial_distance/2 else initial_distance/2
            extra = extra if extra > 0 else 0
            new_step = round(extra / num, 2) if num != 0 else distance
            cur_steps.append(new_step)
        steps.append(cur_steps)
    return steps

def calc_dist(point1, point2):
    point1 = np.array(point1)
    point2 = np.array(point2)
    return np.sqrt(np.sum((point1 - point2) ** 2))

# def calc_dict_bw_lines(line1, line2):
#     return min(min(calc_dist(line1[0], line2[0]),calc_dist(line1[0], line2[1])),
#                 min(calc_dist(line1[1], line2[0]),calc_dist(line1[1], line2[1])))


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
                new_point,u_b = line_intersects(border, [middle_point, point])
                if new_point is not None and u_b > 0 and u_b < u_b_min:
                    new_point_min = new_point
                    u_b_min = u_b
            c_line.append(new_point_min)
        new_lines.append(np.array(c_line))
    return new_lines

def create_milling_line(lines, distance, middle_point, last_border, milling_diam):
    array_of_lines = []
    first_point = []
    last_point = []
    # i = 0
    dst = True
    max_dst = get_max_distance(last_border,middle_point) - distance*0.25
    extra = max_dst-get_min_distance(np.array(lines),middle_point)
    num = ceil((max_dst-get_min_distance(np.array(lines),middle_point))/distance)
    new_step = round(extra/num,2) if num != 0 else distance
    print(extra, num, distance, new_step, extra/new_step)
    # distance = new_step
    object_projection = get_object_projection(lines,middle_point,last_border)
    steps = generate_steps(object_projection,lines,num,middle_point, new_step,distance)
    len_of_lines = len(lines)

    for i in range(num+1):
        new_lines = []
        for j,line in enumerate(lines):
            new_line = []
            for k,point in enumerate(line):
                cur_distance = steps[j][k]
                atg = atan2(middle_point[1] - point[1], middle_point[0] - point[0])
                new_point = [point[0] - cur_distance * i * cos(atg), point[1] - cur_distance * i * sin(atg)]
                # dst = np.sum((new_point - middle_point) **2 ) < max_dst**2
                # print(f"new_point: {new_point}, dst: {dst}")
                new_line.append(new_point)

            if j == 1:
                if abs(calc_dist(new_lines[0][0], new_line[0])) < 0.0001 or \
                        abs(calc_dist(new_lines[0][0], new_line[1])) < 0.0001:
                    first_point.append(new_lines[0][1])
                else:
                    first_point.append(new_lines[0][0])



            if i != 0 and j >= len_of_lines//2:
                d1 = calc_dist(first_point[i], new_line[0])
                d2 = calc_dist(first_point[i], new_line[1])
                if (min(calc_dist(first_point[i], new_line[0]),calc_dist(first_point[i], new_line[1])) <= distance/2.0):
                    x0, y0 = new_line[0]
                    x1, y1 = new_line[1]
                    x2, y2 = first_point[i]
                    R = distance/2.0
                    Da = (x1 - x0)**2 + (y1 - y0) ** 2
                    Db = (x0 - x2) * (x1-x0) + (y0 - y2) * (y1 - y0)
                    Dc = (x0 - x2) ** 2 + (y0 - y2) ** 2 - R**2
                    # Lk = (y1 - y0)/(x1- x0)
                    # Lb = y0 - x0 * (y1-y0)/(x1-x0)
                    # Da = 1 + Lk**2
                    # Db = Lk*Lb - y2 * Lk - x2
                    # Dc = Lb**2 + y2**2 + x2**2 - R**2 -2 * y2 * Lb
                    D = Db**2 - Da * Dc
                    D = sqrt(Db**2 - Da * Dc)
                    t = [(-Db - D) / (Da), (-Db + D) / (Da)]
                    x = [(x1 - x0) * t[0] + x0, (x1 - x0) * t[1] + x0]
                    y = [(y1 - y0) * t[0] + y0, (y1 - y0) * t[1] + y0]
                    # x = [(-Db - D)/(Da), (-Db + D)/(Da)]
                    # y = [Lk * x[0] + Lb, Lk * x[1] + Lb]
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
        # print(f"{i}: {len(first_point)}|{len(last_point)} ")



        array_of_lines.append(new_lines)
        dst = get_min_distance(np.array(new_lines), middle_point) < max_dst
        # i +=1
        # print(i, dst, get_min_distance(np.array(new_lines), middle_point))
    print(f"Extended: {i} times")
    # plot_lines(array_of_lines,lines)
    array_of_lines.reverse()

    first_point.reverse()
    last_point.reverse()
    new_array_of_lines = []
    for i in range(len(array_of_lines)-1):
        new_array_of_lines += array_of_lines[i]
        new_array_of_lines += [[last_point[i], first_point[i+1]]]
    new_array_of_lines += array_of_lines[-1]
    new_array_of_lines = np.array(new_array_of_lines)
    return new_array_of_lines


def process_milling_slice(initial_object, cur_border, milling_diameter, clear_offset, threshold,prev_first_point=None):
    # plot_lines([initial_object], cur_border)

    distance = milling_diameter*threshold
    object_offset = -milling_diameter/2 - clear_offset
    middle_point_cur_border = get_avg(cur_border)
    object_middle_point = get_avg(initial_object)

    inc_object = add_offset(initial_object,object_offset, object_middle_point)
    new_lines= create_milling_line(inc_object,distance,middle_point_cur_border,cur_border, milling_diameter)

    points = to_points_shape(new_lines)

    # add clear path
    clear_border = to_points_shape(np.array(add_offset(initial_object,object_offset+clear_offset,object_middle_point)))
    # clear_border = np.append(clear_border[1::, ::], [clear_border[1]], axis=0)
    # plt.plot(clear_border[::, 0], clear_border[::, 1], marker='o',
    #                  markerfacecolor='red', markersize=1, color='skyblue', linewidth=2)
    # plt.plot(clear_border[-1,0], clear_border[-1,1], marker='.', markerfacecolor='red', markersize=10)
    # if prev_first_point is not None:
    #     plt.plot([prev_first_point[0]], [prev_first_point[1]], marker='.', markerfacecolor='yellow', markersize=10)
    # plt.show()

    shift = 0
    if prev_first_point is not None:
        dp2 = np.sum( (clear_border - prev_first_point) ** 2,axis=1)
        shift = np.argmin(dp2)

    if shift != 0:
        clear_border = np.append(clear_border[:-1, ::], clear_border[:shift+1,::], axis=0)

    if prev_first_point is not None:
        clear_border = np.append(clear_border, [prev_first_point], axis=0)

    # plt.plot(clear_border[::, 0], clear_border[::, 1], marker='o',
    #                  markerfacecolor='red', markersize=1, color='skyblue', linewidth=2)
    # plt.plot(clear_border[-1,0], clear_border[-1,1], marker='.', markerfacecolor='red', markersize=10)
    # if prev_first_point is not None:
    #     plt.plot([prev_first_point[0]], [prev_first_point[1]], marker='.', markerfacecolor='yellow', markersize=10)
    # plt.show()

    points = np.append(points, clear_border, axis=0)
    return points



if __name__ == "__main__":
    borders = np.array([[[0, 0], [0, 100]], [[0, 100],[100, 100]],
                        [[100, 100],[100, 0]], [[100, 0],[0, 0]]])
    borders2 = np.array([[[0, 10], [0, 100]], [[0, 100],[100, 100]],
                        [[100, 100],[100, 0]], [[100, 0],[10, 0]],
                         [[10, 0], [0, 10]]])
    examples = ['lines_15.txt', 'lines_55.txt', 'lines_10.txt', 'lines_45.txt']
    object = np.load(examples[3], allow_pickle=True)

    points = process_milling_slice(object, borders2,10, 1, 0.85)
    # points = process_milling_slice(np.load('final_model_slice.npy', allow_pickle=True),
    #                                np.load('initial_model_slice.npy', allow_pickle=True),
    #                                10, 1, 0.85)

    plt.plot(points[::, 0], points[::, 1], marker='.', markersize=2, color='b', linewidth=1)
    plt.axis([-6, 106, -6, 106])
    plt.show()
