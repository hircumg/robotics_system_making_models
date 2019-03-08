from stl import mesh
import numpy as np
import math
from matplotlib import pyplot
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time


def plot_lines(lines):
    """
    Plotting border of slice
    :param lines: array of lines for plotting
    :return: nothing
    """
    for line in lines:
        plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='o', markerfacecolor='red', markersize=5,
                 color='skyblue', linewidth=4)

    plt.show()

def plot_points(points):
    """
    Plotting array where indexes is coordinates of plotting points.
    Point will be plotted only if element value is 1
    :param points: two-dimensional binary array
    :return: nothing
    """
    for i in range(points.shape[0]):
        for j in range(points.shape[1]):
            if points[i,j] % 2 ==  1:
                plt.plot(i, j, 'bo')
    plt.show()

def plot3d_points(points):
    """
    Plotting list of points in 3d plot
    :param points: list of 3d points
    :return: nothing
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = []
    y = []
    z = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    ax.scatter3D(x, y, z, c='b', marker='o')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()

def plot_points3d(points3d):
    """
    Plotting array where indexes is coordinates of plotting points.
    Point will be plotted only if element value is 1
    :param points3d: two or three dimensional binary array
    :return: nothing
    """


    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = []
    y = []
    z = []

    if len(points3d.shape) == 3:
        for i in range(points3d.shape[0]):
            for j in range(points3d.shape[1]):
                for k in range(points3d.shape[2]):
                    if points3d[i,j,k] % 2 ==  1:
                        x.append(i)
                        y.append(j)
                        z.append(k)
    elif len(points3d.shape) == 2:
        for i in range(points3d.shape[0]):
            for j in range(points3d.shape[1]):
                    if points3d[i,j] % 2 ==  1:
                        x.append(i)
                        y.append(j)
                        z.append(0)
    ax.scatter3D(x, y, z, c='b', marker='o')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

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
            x_int =line[0][0] +  (point[1] - line[0][1]) * (line[1][0] - line[0][0]) / (line[1][1] - line[0][1])
            if abs(line[1][0] - line[0][0]) < 0.001:
                #parralel Ox
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


def one_slice(vectors, height, x_min, x_max, y_min, y_max, box_size, decimals=6, frac=0.001):
    """
    make boxed slice for given height
    :param vectors: array of 3d object
    :param height: heeigth for slice
    :param x_min: min x coordinate of the object
    :param x_max: max x coordinate of the object
    :param y_min: min y coordinate of the object
    :param y_max: max y coordinate of the object
    :param decimals: number of the decimals after point for rounding operations after math calculation
    :param box_size: size of the cube box
    :param frac: error in comparison
    :return: 2d binary array where 1 means that there`s a cube
    """


    lines_of_slice = []
    triangles_of_slice = []

    # left only triangles which crosses horizontal plane
    for triangle in vectors:
        upper = 0
        lower = 0
        for i in triangle:
            if i[2] > height:
                upper += 1
            else:
                lower += 1
        if upper != 0 and lower != 0:
            triangles_of_slice.append([triangle.copy(), upper])

    print("Triangles taken for height %.3f" %(height))
    # save only line of triangles in horizontal plane
    for triangle, upper in triangles_of_slice:
        # find points for neadble lines
        point_m = None
        point_a = None
        point_b = None
        if upper == 2:
            # two points upper than height
            min_ind = 0
            for i in range(2):
                if triangle[min_ind][2] > triangle[i + 1][2]:
                    min_ind = i + 1
            point_m = triangle[min_ind]
            point_a = triangle[(min_ind + 1) % 3]
            point_b = triangle[(min_ind + 2) % 3]

        else:
            # two points lower than height
            max_ind = 0
            for i in range(2):
                if triangle[max_ind][2] < triangle[i + 1][2]:
                    max_ind = i + 1
            point_m = triangle[max_ind]
            point_a = triangle[(max_ind + 1) % 3]
            point_b = triangle[(max_ind + 2) % 3]

        #     find intersections between lines and plane
        #     with a line
        z = height
        x_a = point_m[0] + (point_a[0] - point_m[0]) * (z - point_m[2]) / (point_a[2] - point_m[2])
        y_a = point_m[1] + (point_a[1] - point_m[1]) * (z - point_m[2]) / (point_a[2] - point_m[2])

        x_b = point_m[0] + (point_b[0] - point_m[0]) * (z - point_m[2]) / (point_b[2] - point_m[2])
        y_b = point_m[1] + (point_b[1] - point_m[1]) * (z - point_m[2]) / (point_b[2] - point_m[2])
        lines_of_slice.append([[x_a, y_a], [x_b, y_b]])
    lines_of_slice = np.array(lines_of_slice)
    lines_of_slice = np.around(lines_of_slice - 10 ** (-(decimals + 5)), decimals=decimals)
    print("Lines taken for height %.3f" % (height))
    # plot_lines(lines_of_slice)

    # create dotted plane from given group of borders
    length = math.ceil(abs(x_max - x_min) / box_size)
    width = math.ceil(abs(y_max - y_min) / box_size)
    slice_plane_cubes = np.zeros((length, width))
    for i in range(length):
        for j in range(width):
            for k in range(box_size ** 2):
                if (slice_plane_cubes[i, j] != 0):
                    break
                else:
                    if (i * box_size + k % box_size < abs(x_max - x_min)) and (
                            j * box_size + k // box_size < abs(y_max - y_min)):
                        slice_plane_cubes[i, j] += is_inside([int(round(x_min)) + i * box_size + k % box_size,
                                                              int(round(y_min)) + j * box_size + k // box_size],
                                                             lines_of_slice)
                        slice_plane_cubes[i, j] = slice_plane_cubes[i, j] % 2
    print("Slice converted into 2d binary array for height %.3f" % (height))

    # plot_points(slice_plane_cubes)
    return slice_plane_cubes

def convert_to_current_height(slice, begin_height, box_size):
    points = []

    for i in range(slice.shape[0]):
        for j in range(slice.shape[1]):
            if(slice[i, j] > 0):
                x_i = int(round(i*box_size+box_size/2))
                y_i = int(round(j*box_size+box_size/2))
                z_i = int(round(begin_height + box_size/2))
                points.append([x_i,y_i,z_i])

    points = np.array(points)
    # print(points)
    return points

def one_height_slice(mesh, begin_height, box_size, fraction=3):
    vectors = mesh.vectors.copy()
    x_min, x_max, y_min, y_max, z_min, z_max = find_mins_maxs(your_mesh)
    step = box_size // fraction
    height = begin_height


    slice_plane = one_slice(vectors, height, x_min, x_max, y_min, y_max,box_size)
    print("Temp slice on height %.3f made" %(height))
    for iter in range(fraction-2):
        height += step
        slice_plane += one_slice(vectors, height, x_min, x_max, y_min, y_max,box_size)
        print("Temp slice on height %.3f made" % (height))

    slice_plane += one_slice(vectors, begin_height+box_size, x_min, x_max, y_min, y_max,box_size)
    print("Temp slice on height %.3f made" % (begin_height+box_size))

    slice_plane[slice_plane != 0] = 1

    # plot_points(slice_plane)
    return slice_plane



def slice(mesh, box_size, fraction= 3):
    begining_time = time.time()
    x_min, x_max, y_min, y_max, z_min, z_max = find_mins_maxs(your_mesh)
    print("Size of the 3d object: x:[%.3f, %.3f], y:[%.3f, %.3f], z: %.3f" %(x_min, x_max, y_min, y_max, z_max))

    length = math.ceil(abs(x_max - x_min) / box_size)
    width = math.ceil(abs(y_max - y_min) / box_size)
    z_size = int(round(z_max / box_size))
    sliced_image = np.zeros((length,width,z_size))

    for i in range(z_size):
        time_slice = time.time()
        temp_slice = one_height_slice(mesh, i*box_size, box_size, fraction=fraction)
        sliced_image[:,:,i] = temp_slice
        current_height = i * box_size + box_size/2
        time_slice = time.time() - time_slice
        print("Height is: %.3f made. Taken time: %i s" %(current_height,time_slice))

    print("Sliced image shape: ", sliced_image.shape)
    plot_points3d(sliced_image)
    slicing_time = time.time() - begining_time
    print('Slicing finished with time %i s' %(slicing_time))
    return sliced_image

def get_max_side(sliced_mesh):
    best_substrate = []
    best_substrate.append(sliced_mesh[0,:,:].sum()) # x_min
    best_substrate.append(sliced_mesh[-1,:,:].sum()) # x_max
    best_substrate.append(sliced_mesh[:,0,:].sum()) # y_min
    best_substrate.append(sliced_mesh[:,-1,:].sum()) # y_max
    best_substrate.append(sliced_mesh[:,:,0].sum()) # z_min
    best_substrate.append(sliced_mesh[:,:,-1].sum()) # z_max
    best_substrate = np.array(best_substrate)
    print(best_substrate, best_substrate.argmax())
    return best_substrate.argmax()



def provide_best_substrate(sliced_mesh):
    new_mesh = sliced_mesh.copy()
    best_substate_ind = get_max_side(sliced_mesh)
    if best_substate_ind == 0:
        new_mesh = np.rot90(new_mesh, 1, (1, 2))
    elif best_substate_ind == 1:
        new_mesh = np.rot90(new_mesh, 1, (2, 1))
    elif best_substate_ind == 2:
        new_mesh = np.rot90(new_mesh, 1, (0, 2))
    elif best_substate_ind == 3:
        new_mesh = np.rot90(new_mesh, 1, (2, 0))
    elif best_substate_ind == 4:
        pass
    elif best_substate_ind == 5:
        new_mesh = np.rot90(new_mesh, 2, (2, 0))
    else:
        new_mesh = sliced_mesh.copy()

    return new_mesh


def find_mins_maxs(mesh, decimals=6):
    '''
    Find borders of given 3d object
    :param mesh: mesh of given 3d object
    :param decimals: number of decimal places to round to
    :return: borders in all axes
    '''
    points = np.reshape(mesh.vectors, (-1, 3))
    points = np.around(points - 10 ** (-(decimals + 5)), decimals=decimals)
    x_min = None
    x_max = None
    y_min = None
    y_max = None
    z_min = None
    z_max = None
    for point in points:
        if (x_max is None):
            x_max = point[0]
            y_max = point[0]
            x_min = point[1]
            y_min = point[1]
            z_min = point[2]
            z_max = point[2]
        else:
            # find x borders
            if (x_max < point[0]):
                x_max = point[0]
            elif (x_min > point[0]):
                x_min = point[0]

            # find y borders
            if (y_max < point[1]):
                y_max = point[1]
            elif (y_min > point[1]):
                y_min = point[1]

            #  find z borders
            if (z_max < point[2]):
                z_max = point[2]
            elif (z_min > point[2]):
                z_min = point[2]

    return x_min, x_max, y_min, y_max, z_min, z_max


if __name__ == '__main__':
    # Load the STL files
    # your_mesh = mesh.Mesh.from_file('Models/PLA_190to220_stl_file.stl')
    your_mesh = mesh.Mesh.from_file('Models/Minecraft_Hanger_hand_1.stl')
    # your_mesh = mesh.Mesh.from_file('Models/Groot_v1_1M_Merged.stl')
    # your_mesh = mesh.Mesh.from_file('Models/xyzCalibration_cube.stl')

    my_sliced_mesh = slice(your_mesh, 10)
    new_sliced_mesh = provide_best_substrate(my_sliced_mesh)
    plot_points3d(new_sliced_mesh)

