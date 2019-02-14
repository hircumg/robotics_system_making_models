
from stl import mesh
import numpy as np
import math
from matplotlib import pyplot
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def plot_lines(lines):
    for line in lines:
        plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='o', markerfacecolor='red', markersize=5,
                 color='skyblue', linewidth=4)

    plt.show()

def plot_points(points):
    for i in range(points.shape[0]):
        for j in range(points.shape[1]):
            if points[i,j] % 2 ==  1:
                plt.plot(i, j, 'bo')
    plt.show()

def plot3d_points(points):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = []
    y = []
    z = []
    for point in points:
        x.append(point[0])
        y.append(point[1])
        z.append(point[2])
    print(x)
    print(y)
    print(z)
    ax.scatter3D(x, y, z, c='r', marker='o')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()



def plot_vectors(vectors):
    new_vectors = []
    for vec in vectors:
        new_vectors.append(vec[0])

    new_vectors = np.array(new_vectors)

    # print(new_vectors.shape)
    # print(new_vectors)

    data = np.zeros(len(new_vectors), dtype=mesh.Mesh.dtype)
    data['vectors'] = new_vectors

    cube = mesh.Mesh(data)
    cube.save('test.stl')
    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    # Render the cube
    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(cube.vectors))

    # Auto scale to the mesh size
    scale = cube.points.flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    pyplot.show()


def is_inside(point, polygon):
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


def one_slice(vectors, height, x_min, x_max, y_min, y_max, decimals=6, frac=0.001):
    vectors = np.around(vectors - 10 ** (-(decimals + 5)), decimals=decimals)
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
    # triangles_of_slice = np.array(triangles_of_slice)
    # print( np.array(triangles_of_slice).shape)
    # plot_vectors(triangles_of_slice)

    # save only line of triangles in horizontal plane
    for triangle, upper in triangles_of_slice:

        # find points for neadble lines
        point_m = None
        point_a = None
        point_b = None
        if upper == 2:
            #         two points upper than height
            min_ind = 0
            for i in range(2):
                if triangle[min_ind][2] > triangle[i + 1][2]:
                    min_ind = i + 1
            point_m = triangle[min_ind]
            point_a = triangle[(min_ind + 1) % 3]
            point_b = triangle[(min_ind + 2) % 3]

        else:
            #         two points lower than height
            max_ind = 0
            for i in range(2):
                if triangle[max_ind][2] < triangle[i + 1][2]:
                    max_ind = i + 1
            point_m = triangle[max_ind]
            point_a = triangle[(max_ind + 1) % 3]
            point_b = triangle[(max_ind + 2) % 3]
        # print(point_m[2], point_a[2], point_b[2], upper)

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
    # print(lines_of_slice)
    # print(lines_of_slice.shape)
    # plot_lines(lines_of_slice)

    # separate borders
    separated_lines_of_slice = []
    for time in range(1000):
        if len(lines_of_slice) == 0:
            break
        closed_line_of_slice = [lines_of_slice[0]]
        last_point = lines_of_slice[0][1]
        lines_of_slice = np.delete(lines_of_slice, 0, 0)
        # print(last_line)
        next_index = 1
        while next_index != None:
            next_index = None
            for i in range(lines_of_slice.shape[0]):
                temp_line = lines_of_slice[i]
                if abs(temp_line[0][0] - last_point[0]) <= frac and abs(temp_line[0][1] - last_point[1]) <= frac:
                    next_index = i
                    closed_line_of_slice.append(lines_of_slice[next_index])
                    last_point = lines_of_slice[next_index][1]
                    lines_of_slice = np.delete(lines_of_slice, next_index, 0)
                    break
                elif abs(temp_line[1][0] - last_point[0]) <= frac and abs(temp_line[1][1] - last_point[1]) <= frac:
                    next_index = i
                    closed_line_of_slice.append(lines_of_slice[next_index])
                    last_point = lines_of_slice[next_index][0]
                    lines_of_slice = np.delete(lines_of_slice, next_index, 0)
                    break

            # print(next_index, last_line)
        separated_lines_of_slice.append(closed_line_of_slice)

    # print(len(separated_lines_of_slice))
    # for s_lines_of_slice in separated_lines_of_slice:
    #     plot_lines(s_lines_of_slice)
    # create dotted plane
    plane = np.zeros((int(round(abs(x_max-x_min))),int(round(abs(y_max-y_min)))))
    # print(plane.shape)
    # print(is_inside([-56, 6], separated_lines_of_slice[0]))
    for cur_lines_of_slice in separated_lines_of_slice:
        for i in range(plane.shape[0]):
            for j in range(plane.shape[1]):
                plane[i,j] += is_inside([int(round(x_min)) + i, int(round(y_min)) + j], cur_lines_of_slice)
                # print([int(round(x_min)) + i, int(round(y_min)) + j], plane[i,j])

    plane = plane % 2
    # plot_points(plane)
    return plane

def convert_to_current_height(slice, begin_height, box_size):
    points = []
    for i in range(slice.shape[0]):
        for j in range(slice.shape[1]):
            x_i = int(round(i*box_size+box_size/2))
            y_i = int(round(j*box_size+box_size/2))
            z_i = int(round(begin_height + box_size/2))
            points.append([x_i,y_i,z_i])

    points = np.array(points)
    # print(points)
    return points

def one_height_slice(mesh, begin_height, box_size, fraction=3):
    vectors = mesh.vectors
    x_min, x_max, y_min, y_max, z_min, z_max = find_mins_maxs(your_mesh)
    step = box_size // fraction
    height = begin_height
    slice_plane = one_slice(vectors, height, x_min, x_max, y_min, y_max)

    # for iter in range(fraction-2):
    #     height += step
    #     slice_plane += one_slice(vectors, height, x_min, x_max, y_min, y_max)

    slice_plane += one_slice(vectors, begin_height+box_size, x_min, x_max, y_min, y_max)

    slice_plane[slice_plane != 0] = 1
    plot_points(slice_plane)
    length = math.ceil(slice_plane.shape[0]/box_size)
    width = math.ceil(slice_plane.shape[1]/box_size)
    slice_plane_cubes = np.zeros((length, width))
    print(slice_plane.shape, slice_plane_cubes.shape)

    for i in range(slice_plane_cubes.shape[0]):
        for j in range(slice_plane_cubes.shape[1]):
            for k in range(box_size**2):
                if(slice_plane_cubes[i,j] != 0):
                    break
                else:
                    if (i*box_size+k%box_size < slice_plane.shape[0]) and (j*box_size + k//box_size < slice_plane.shape[1]):
                        slice_plane_cubes[i,j] = slice_plane[i*box_size+k%box_size, j*box_size + k//box_size]


    plot_points(slice_plane_cubes)
    converted_plane = convert_to_current_height(slice_plane_cubes,begin_height,box_size)
    plot3d_points(converted_plane)
    return slice_plane


def slice(mesh, bottom, upper):
    pass


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


# Load the STL files
your_mesh = mesh.Mesh.from_file('Models/PLA_190to220_stl_file.stl')
# your_mesh = mesh.Mesh.from_file('Models/Minecraft_Hanger_hand_1.stl')
# your_mesh = mesh.Mesh.from_file('Models/xyzCalibration_cube.stl')


x_min, x_max, y_min, y_max, z_min, z_max = find_mins_maxs(your_mesh)

# one_slice(your_mesh.vectors, 3, x_min, x_max, y_min, y_max, 10)
one_height_slice(your_mesh, 0, 10)
# one_slice(your_mesh.vectors, 13, abs(x_max-x_min), abs(y_max-y_min),10)
# one_slice(your_mesh.vectors, 19, abs(x_max-x_min), abs(y_max-y_min),10)
# print(your_mesh.normals)
# print(find_mins_maxs(your_mesh))

# # Create a new plot
# figure = pyplot.figure()
# axes = mplot3d.Axes3D(figure)
#
# axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
#
# # Auto scale to the mesh size
# scale = your_mesh.points.flatten('C')
# axes.auto_scale_xyz(scale, scale, scale)
# # Show the plot to the screen
# pyplot.show()
