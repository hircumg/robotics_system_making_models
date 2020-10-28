
import matplotlib.pyplot as plt
import numpy as np
from math import atan2, sin, cos, sqrt, ceil

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300

def plot_lines(group_of_lines):
    """
    Plotting border of slice
    :param lines: array of lines for plotting
    :return: nothing
    """
    colors = ['skyblue', 'red', 'yellow']
    i = 0
    for lines in group_of_lines:

        for line in lines:
            plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='.',
                     markerfacecolor='red', markersize=1, color=colors[i], linewidth=1)

        i = (i+1)%3


    # plt.axis([-1, 101, -1, 101])
    # plt.axis([-21, 121, -21, 121])
    plt.axis([-6, 106, -6, 106])
    # plt.axis([-21, 21, 81, 121])
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

def is_inside_by_points(point, border):
    """
    Check is given 2d point inside given polygon or not
    :return: boolean value: 1 if point is inside polygon otherwise will be returned 0
    """

    polygon = []
    for i in range(1,len(border)):
        polygon.append([border[i-1], border[i]])

    c_west = 0
    i = 0
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

        i += 1
    return c_west



# borders = np.array([[[0, 0], [0, 100]], [[0, 100],[100, 100]],
#                     [[100, 100],[100, 0]], [[100, 0],[0, 0]]])
# borders2 = np.array([[[0, 10], [0, 100]], [[0, 100],[100, 100]],
#                     [[100, 100],[100, 0]], [[100, 0],[10, 0]],
#                      [[10, 0], [0, 10]]])

# lines_15 = np.load('lines_15.txt', allow_pickle=True)
# plot_lines(lines_15, borders)

examples = ['lines_15.txt', 'lines_55.txt', 'lines_10.txt', 'lines_45.txt']




def calc_dist(point1, point2):
    point1 = np.array(point1)
    point2 = np.array(point2)
    return np.sqrt(np.sum((point1 - point2) ** 2))

def calc_dict_bw_lines(line1, line2):
    return min(min(calc_dist(line1[0], line2[0]),calc_dist(line1[0], line2[1])),
                min(calc_dist(line1[1], line2[0]),calc_dist(line1[1], line2[1])))


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
        if u_b >= 0 and u_b <= 1 and u_a >=0 and u_a <= 1:
            return np.array([x, y])
    return None


def to_points_shape(lines_arr):
    points = []
    H1 = np.array([[1, 0, 1, 0],[0, 1, 0, 1]])
    H2 = np.array([[1, 1, 0, 0],[0, 0, 1, 1]])
    same_point = (np.argmin(np.sum((lines_arr[0].T@H1-lines_arr[1].T@H2)**2,axis=0)))%2
    points.append(lines_arr[0][(same_point+1)%2])
    for line in lines_arr:
        prev_point = points[-1].reshape((1,-1))
        H1 = np.array([[1, 1]])
        same_point = (np.argmin(np.sum((line.T - prev_point.T@H1) ** 2, axis=0))) % 2
        points.append(line[(same_point + 1) % 2])

    return np.array(points)


def add_intersections(border1, border2):
    new_border1 = []
    new_border1.append(border1[0])
    intersections = []
    new_border2 = border2.copy()
    for i in range(1, len(border1)):
        line = border1[i-1:i+1]
        j = 1
        while j < len(new_border2):
            line_2 = new_border2[j-1:j+1]
            inter_point = line_intersects(line, line_2)
            if inter_point is not None:
                line[0] = inter_point
                # print(inter_point,is_in_array(inter_point,border1), is_in_array(inter_point,new_border2))
                if not is_in_array(inter_point,border1):
                    new_border1.append(inter_point)
                if not is_in_array(inter_point,new_border2):
                    new_border2 = np.insert(new_border2,j,inter_point,axis=0)
                j +=1
                intersections.append(inter_point)
            j +=1
        new_border1.append(border1[i])
    return np.array(new_border1), new_border2, np.array(intersections)

def is_in_array(point, array):
    for t_point in array:
        if abs(np.sum((point - t_point)**2)) < 0.001:
            return True

    return False



def combine_borders(border1, border2, intersections):
    final_border = []
    final_border.append(border1[0])
    i = 1
    j = 1
    first_border = True
    second_border_direction = 0
    while i < len(border1):
        if first_border:
            final_border.append(border1[i])
            if not is_in_array(border1[i], intersections):
                i += 1
            else:
                first_border = False
                if second_border_direction == 0:
                    #                 there's no previous intersections
                    j = 0
                    prev_point_inside = None
                    while abs(np.sum((border2[j] - border1[i]) ** 2)) > 0.001:
                        t = (border2[j] + border2[j + 1]) / 2
                        prev_point_inside = is_inside_by_points((border2[j] + border2[j + 1]) / 2, border1)
                        j += 1

                    if prev_point_inside is None:
                        #      only if we started in the intersect point
                        prev_point_inside = not is_inside_by_points((border2[j] + border2[j + 1]) / 2,
                                                                    border1)

                    if prev_point_inside:
                        second_border_direction = 1
                    else:
                        second_border_direction = -1
                else:
                    while abs(np.sum((border2[j] - border1[i]) ** 2)) > 0.001:
                        j += second_border_direction
                j = (j + second_border_direction + len(border2)) % len(border2)
        else:
            #         iteration during second border
            final_border.append(border2[j])
            if not is_in_array(border2[j], intersections):
                j = (j + second_border_direction + len(border2)) % len(border2)
            else:
                first_border = True
                while abs(np.sum((border2[j] - border1[i]) ** 2)) > 0.001:
                    i += 1
                i += 1
    return final_border, i, j


def process_borders(borders):
    borders = [to_points_shape(bord) for bord in borders]
    combined_border = borders[0].copy()

    for k in range(1, len(borders)):
        # points = to_points_shape(combined_border)
        # points2 = to_points_shape(borders[k])

        new_points, new_points2, intersections = add_intersections(combined_border, borders[k])
        new_points = new_points[:-1]
        shift = 31
        new_points = np.append(new_points[shift:], new_points[:shift + 1], axis=0)

        print(len(borders), len(new_points), len(borders[k]), len(new_points2), len(intersections))
        plt.plot(new_points[::, 0], new_points[::, 1], marker='.', markersize=2, color='b', linewidth=1)
        plt.plot(new_points2[::, 0], new_points2[::, 1], marker='.', markersize=2, color='g', linewidth=1)
        if len(intersections) > 0:
            plt.scatter(intersections[::, 0], intersections[::, 1], s=20, color='r')
        plt.scatter(new_points[0, 0], new_points[0, 1], s=40, color='b')
        plt.scatter(new_points2[0, 0], new_points2[0, 1], s=40, color='y')
        plt.axis([-6, 106, -6, 106])
        plt.show()


        i = 0
        while is_inside_by_points(new_points[i], new_points2) or is_in_array(new_points[i], intersections):
            i += 1
        # print(f'Shift for i: {i}')
        new_points = new_points[:-1]
        new_points = np.append(new_points[i:], new_points[:i + 1], axis=0)
        # print(is_in_array(new_points[0], intersections))
        # print(len(points), len(new_points), len(points2), len(new_points2), len(intersections))

        combined_border, i, j = combine_borders(new_points, new_points2, intersections)
        if i == len(new_points):
            i -= 1

        combined_border = np.array(combined_border)
        plt.plot(combined_border[::, 0], combined_border[::, 1], marker='.', markersize=2, color='b', linewidth=1)
        # plt.plot(new_points2[::,0],new_points2[::,1],marker='.', markersize=2, color='g', linewidth=1)
        # plt.scatter(intersections[::,0], intersections[::,1], s=20, color='r')
        # plt.scatter(new_points[i,0], new_points[i,1], s=40, color='b')
        # plt.scatter(new_points2[j,0], new_points2[j,1], s=40, color='y')
        plt.axis([-6, 106, -6, 106])
        plt.show()


    polygon = []
    for i in range(1,len(combined_border)):
        polygon.append([combined_border[i-1], combined_border[i]])
    return polygon


if __name__ == "__main__":
    object = np.load(examples[2], allow_pickle=True)
    object1 = np.load(examples[1], allow_pickle=True)
    object2 = np.load(examples[0], allow_pickle=True)
    out_border = process_borders([object, object1, object2])
    plot_lines([out_border])

