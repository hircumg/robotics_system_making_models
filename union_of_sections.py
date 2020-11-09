
import matplotlib.pyplot as plt
import numpy as np
from math import atan2, sin, cos, sqrt, ceil

import matplotlib as mpl
mpl.rcParams['figure.dpi'] = 300

from utils import line_intersects, is_inside_by_points



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

def to_points_shape_unsorded(lines_arr):
    points = []
    if len(lines_arr) == 0:
        return []
    H1 = np.array([[1, 0, 1, 0],[0, 1, 0, 1]])
    H2 = np.array([[1, 1, 0, 0],[0, 0, 1, 1]])
    same_point = (np.argmin(np.sum((lines_arr[0].T@H1-lines_arr[1].T@H2)**2,axis=0)))%2
    points.append(lines_arr[0][(same_point+1)%2])
    points.append(lines_arr[0][same_point])
    lines_arr = np.delete(lines_arr, 0, axis=0)
    i = 0
    H1 = np.array([[1, 1]])
    while len(lines_arr) > 0:
        prev_point = points[-1].reshape((1, -1))
        for i,line in enumerate(lines_arr):
            is_requested_line = np.min(np.sum((line.T - prev_point.T @ H1) ** 2, axis=0)) < 0.0001
            if is_requested_line:
                same_point = (np.argmin(np.sum((line.T - prev_point.T @ H1) ** 2, axis=0))) % 2
                points.append(line[(same_point + 1) % 2])
                lines_arr = np.delete(lines_arr, i, axis=0)


    return np.array(points)


def add_intersections(border1, border2):
    new_border1 = []
    new_border1.append(border1[0])
    intersections = []
    new_border2 = border2.copy()
    for i in range(1, len(border1)):
        line = border1[i-1:i+1].copy()
        j = 1
        while j < len(new_border2):
            line_2 = new_border2[j-1:j+1].copy()
            inter_point, _, _ = line_intersects(line, line_2)
            if inter_point is not None:
                line[0] = inter_point
                # print(inter_point,is_in_array(inter_point,border1), is_in_array(inter_point,new_border2))
                if not is_in_array(inter_point,border1):
                    new_border1.append(inter_point)
                if not is_in_array(inter_point,new_border2):
                    new_border2 = np.insert(new_border2,j,inter_point,axis=0)
                j +=1
                if not is_in_array(inter_point, intersections):
                    intersections.append(inter_point)
            j +=1
        # if not is_in_array(inter_point, new_border1):
        new_border1.append(border1[i])

    return np.array(new_border1), new_border2, np.array(intersections)


def is_in_array(point, array):
    for t_point in array:
        if abs(np.sum((point - t_point)**2)) < 0.001:
            return True
    return False


def combine_borders(border1, border2, intersections):
    final_border = []
    # final_border.append(border1[0])
    i = 0
    j = 0
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
                    if i == len(border1):
                        break
                i += 1
    return final_border, i, j


def process_borders(borders, debug=False):
    borders = [to_points_shape_unsorded(bord) for bord in borders]
    combined_border = borders[0].copy()

    for k in range(1, len(borders)):
        print("===================")
        print('k:',k, len(borders))
        new_points, new_points2, intersections = add_intersections(combined_border, borders[k])
        # new_points = new_points[:-1]
        # shift = 31
        # new_points = np.append(new_points[shift:], new_points[:shift + 1], axis=0)
        print("is_in_array: ", is_in_array(new_points[0],intersections))
        if debug:
            plt.plot(new_points[::, 0], new_points[::, 1], marker='.', markersize=2, color='b', linewidth=1)
            plt.plot(new_points2[::, 0], new_points2[::, 1], marker='.', markersize=2, color='g', linewidth=1)
            if len(intersections) > 0:
                plt.scatter(intersections[::, 0], intersections[::, 1], s=20, color='r')
            plt.scatter(new_points[0, 0], new_points[0, 1], s=40, color='b')
            plt.scatter(new_points2[0, 0], new_points2[0, 1], s=40, color='y')
            plt.axis([-6, 106, -6, 106])
            plt.title(f"Initital plot for k: {k}")
            plt.show()


        i = 0
        while (i < len(new_points)) and is_inside_by_points(new_points[i], new_points2) or ((len(intersections) > 0) and not is_in_array(new_points[i], intersections)):
            i += 1
            if i >= len(new_points):
                # i = 0
                break

        if i >= len(new_points):
            print('Split points')
            new_points3 = new_points2.copy()
            new_points2 = new_points.copy()
            new_points = new_points3
            i = 0
            while (i < len(new_points)) and is_inside_by_points(new_points[i], new_points2) or \
                    ((len(intersections) > 0) and not is_in_array(new_points[i], intersections)):
                i += 1

        if debug:
            print(f'Shift for i: {i}')
        new_points = new_points[:-1]
        new_points = np.append(new_points[i:], new_points[:i + 1], axis=0)
        if debug:
            print(len(combined_border), len(new_points), len(borders[k]), len(new_points2), len(intersections))

        combined_border, i, j = combine_borders(new_points, new_points2, intersections)
        if i == len(new_points):
            i -= 1

        combined_border = np.array(combined_border)
        if debug:
            plt.plot(combined_border[::, 0], combined_border[::, 1], marker='.', markersize=2, color='b', linewidth=1)
            # plt.plot(new_points2[::,0],new_points2[::,1],marker='.', markersize=2, color='g', linewidth=1)
            # plt.scatter(intersections[::,0], intersections[::,1], s=20, color='r')
            # plt.scatter(new_points[i,0], new_points[i,1], s=40, color='b')
            # plt.scatter(new_points2[j,0], new_points2[j,1], s=40, color='y')
            plt.axis([-6, 106, -6, 106])
            plt.title(f"Final plot for k: {k}")
            plt.show()
    polygon = []
    for i in range(1,len(combined_border)):
        polygon.append([combined_border[i-1], combined_border[i]])
    return polygon


if __name__ == "__main__":
    examples = ['lines_15.txt', 'lines_55.txt', 'lines_10.txt', 'lines_45.txt']
    object = np.load(examples[2], allow_pickle=True)
    object1 = np.load(examples[1], allow_pickle=True)
    object2 = np.load(examples[0], allow_pickle=True)
    objects = np.load('lines_test.npy', allow_pickle=True)

    borders2 = [to_points_shape_unsorded(bord) for bord in objects]
    border = borders2[0]
    a = border[:-1]
    b = border[1:]
    diff = a - b
    x_param = np.append(a[::,0].reshape((-1,1)), diff[::,0].reshape((-1,1)), axis=1)
    y_param = np.append(a[::,1].reshape((-1,1)), diff[::,1].reshape((-1,1)), axis=1)
    params = np.append(x_param, y_param, axis=1)
    num =  diff[::,0]
    dmun = diff[::,1]
    divide = num / dmun
    print(len(a), len(b))
    # out_border = process_borders(objects, debug=True)
    out_border = process_borders([object1,object, object2], debug=True)
    # plot_lines([out_border])

