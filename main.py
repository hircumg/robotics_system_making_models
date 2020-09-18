from stl import mesh
import numpy as np
from reading import make_slice
import math
from plotting import plot_points3d
import json

# !! set constant
MILING = 'miling'


class Params():
    def __init__(self, type):
        self.type = type

    def configureMilling(self, diameter, height):
        if self.type == MILING:  # !! set variable
            self.diameter = diameter
            self.height = height
            return 0
        else:
            # todo throw error
            return -1


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


# !! to meters
def xyz_to_meters(dct):
    for pair in dct.items():
        v = pair[1]
        if len(v) == 3:
            # (x,y,z)
            dct[pair[0]] = (v[0] * 0.001, v[1] * 0.001, v[2] * 0.001)
        else:
            # (x,y,z,w,p,r)
            dct[pair[0]] = (v[0] * 0.001, v[1] * 0.001, v[2] * 0.001, v[3], v[4], v[5])


def get_milling_sequence(sliced_image, drilling_radius, drilling_height):
    trajectory = []

    t_point = 'p0'
    t_point_old = 'p0'
    #todo provide start point
    points = {}
    point_iter = 0
    is_milling = False
    top_height = sliced_image.shape[2]
    for i in range(sliced_image.shape[2] - 1, 0 - 1, -1):
        for j in range(sliced_image.shape[1]):
            for k in range(sliced_image.shape[0]):
                if sliced_image[k, j, i] == 1:
                    if not is_milling:
                        t_point = 'p' + str(point_iter)
                        trajectory.append({'type': 'lin', 'proc': is_milling, 'points': [t_point]})
                        t_point_old = t_point

                        t_point = 'p' + str(point_iter + 1)
                        points.update(
                            {t_point_old: (drilling_radius * k, drilling_radius * j, drilling_height * top_height)})
                        points.update({t_point: (drilling_radius * k, drilling_radius * j, drilling_height * i)})
                        is_milling = True
                        trajectory.append({'type': 'lin', 'proc': is_milling, 'points': [t_point]})
                        t_point_old = t_point
                        point_iter += 2

                else:
                    if is_milling:
                        t_point = 'p' + str(point_iter)
                        trajectory.append({'type': 'lin', 'proc': is_milling, 'points': [t_point]})
                        t_point_old = t_point

                        t_point = 'p' + str(point_iter + 1)
                        points.update({t_point_old: (drilling_radius * k, drilling_radius * j, drilling_height * i)})
                        points.update({t_point: (drilling_radius * k, drilling_radius * j, drilling_height * top_height)})
                        is_milling = False
                        trajectory.append({'type': 'lin', 'proc': is_milling, 'points': [t_point]})
                        t_point_old = t_point
                        point_iter += 2

            if is_milling:
                t_point = 'p' + str(point_iter)
                trajectory.append({'type': 'lin', 'proc': is_milling, 'points': [t_point]})
                t_point_old = t_point

                t_point = 'p' + str(point_iter + 1)
                points.update({t_point_old: (drilling_radius * k, drilling_radius * j, drilling_height * i)})
                points.update({t_point: (drilling_radius * k, drilling_radius * j, drilling_height * top_height)})
                is_milling = False
                trajectory.append({'type': 'lin', 'proc': is_milling, 'points': [t_point]})
                t_point_old = t_point
                point_iter += 2

    # !! convert units
    xyz_to_meters(points)
    return {'points': points, 'trajectory': trajectory}


class Slicer():
    def __init__(self, fraction=3):
        self.fraction = fraction
        pass

    def _find_mins_maxs(self, mesh, decimals=6):
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
            if x_max is None:
                x_max = point[0]
                y_max = point[0]
                x_min = point[1]
                y_min = point[1]
                z_min = point[2]
                z_max = point[2]
            else:
                # find x borders
                if x_max < point[0]:
                    x_max = point[0]
                elif x_min > point[0]:
                    x_min = point[0]

                # find y borders
                if y_max < point[1]:
                    y_max = point[1]
                elif y_min > point[1]:
                    y_min = point[1]

                #  find z borders
                if z_max < point[2]:
                    z_max = point[2]
                elif z_min > point[2]:
                    z_min = point[2]

        return x_min, x_max, y_min, y_max, z_min, z_max

    def _substract_stls(self, initial_model, final_model):
        # todo initial_model - final_model
        stl_model = initial_model
        return stl_model

    def _slice_per_layer(self, mesh, params, layer):
        vectors = mesh.vectors.copy()
        x_min, x_max, y_min, y_max, z_min, z_max = self._find_mins_maxs(mesh)
        step = params.height // self.fraction
        cur_height = layer * params.height

        slice_plane = self._slice_one_height_cont(vectors, cur_height)
        slice_plane_bin = self._binearize(slice_plane, x_min, x_max, y_min, y_max, params)
        # todo make binearization after combining several slises
        # todo modify algorithm for milling process
        for iter in range(self.fraction - 2):
            cur_height += step
            slice_plane = self._slice_one_height_cont(vectors, cur_height)
            slice_plane_bin += self._binearize(slice_plane, x_min, x_max, y_min, y_max, params)
            # !! print("Temp slice on height %.3f made" % cur_height)

        slice_plane = self._slice_one_height_cont(vectors, (layer + 1) * params.height)
        slice_plane_bin += self._binearize(slice_plane, x_min, x_max, y_min, y_max, params)
        slice_plane_bin[slice_plane_bin != 0] = 1
        # !! plot_points(slice_plane_bin)
        return slice_plane_bin

    def _binearize(self, lines_of_slice, x_min, x_max, y_min, y_max, params):
        # create dotted plane from given group of borders
        length = math.ceil(abs(x_max - x_min) / params.diameter)
        width = math.ceil(abs(y_max - y_min) / params.diameter)
        slice_plane_cubes = np.zeros((length, width))
        for i in range(length):
            for j in range(width):
                for k in range(params.diameter ** 2):
                    if slice_plane_cubes[i, j] != 0:
                        break
                    else:
                        if (i * params.diameter + k % params.diameter < abs(x_max - x_min)) and (
                                j * params.diameter + k // params.diameter < abs(y_max - y_min)):
                            slice_plane_cubes[i, j] += is_inside(
                                [int(round(x_min)) + i * params.diameter + k % params.diameter,
                                 int(round(y_min)) + j * params.diameter + k // params.diameter],
                                lines_of_slice)
                            slice_plane_cubes[i, j] = slice_plane_cubes[i, j] % 2

        # !! plot_points(slice_plane_cubes)
        return slice_plane_cubes

    def _slice_one_height_cont(self, vectors, height, decimals=6, frac=0.001):
        lines_of_slice = []
        triangles_of_slice = []
        # plot_vectors(vectors)
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
        # !! print("Triangles taken for height %.3f" % height)
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
        # !! print("Lines taken for height %.3f" % (height))
        # !! plot_lines(lines_of_slice)
        return lines_of_slice



    # !! It seems that the process should be universal and depends
    # !! on type in params object
    # !! The first model is obligatory, the second could be None if it useless
    def processing(self, initial_model, final_model, params, debug=False):
        # check params
        if params == None:
            print("Parmeters are not defined")
            return None
        elif params.type == MILING:
            initial_model_slice,_ = make_slice(initial_model, params.diameter, params.height, debug=debug)
            final_model_slice,_ = make_slice(final_model, params.diameter, params.height, debug=debug)
            sliced_image = initial_model_slice - final_model_slice
            return sliced_image
        else:
            print("Unexpected process", params.type)
            return None



# !! collect actions
def findTrajectory(srcName, dstName, params):
    src_mesh = mesh.Mesh.from_file(srcName)
    if dstName:
        dst_mesh = mesh.Mesh.from_file(dstName)

    slicer = Slicer()
    sliced_mesh = slicer.processing(src_mesh, dst_mesh, params, debug=False)
    if params.type == MILING:
        return get_milling_sequence(sliced_mesh, params.diameter, params.height)
    # default
    return None



if __name__ == '__main__':
    params = Params(MILING)
    params.configureMilling(20, 5)
    commands = findTrajectory('models_test/box.stl', 'models_test/pyramid.stl', params)
    # commands = findTrajectory('models_test/box.stl', 'models_test/hemisphere.stl', params)
    print(commands['points'])
    print(commands['trajectory'])


    output_file = "test.txt"
    if output_file is not None:
        outputfile = open(output_file,"w")
    if output_file is not None:
        outputfile.write(json.dumps(commands['points']) + "\n")
        outputfile.write(json.dumps(commands['trajectory']) + "\n")
    print("Finished")