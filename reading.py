from stl import mesh
import numpy as np
from matplotlib import pyplot
from mpl_toolkits import mplot3d


def one_slice(mesh, heigth):
    pass

def one_height(mesh):
    pass

def slice(mesh, bottom, upper):
    pass

def find_mins_maxs(mesh):
    points = np.reshape(mesh.vectors, (-1,3))
    print(points)
    print(points.shape)
    x_min = None
    x_max = None
    y_min = None
    y_max = None
    z_min = None
    z_max = None
    for point in points:
        if(x_max is None):
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
            elif(x_min > point[0]):
                x_min = point[0]

            # find y borders
            if (x_max < point[0]):
                x_max = point[0]
            elif(x_min > point[0]):
                x_min = point[0]

            #  find z borders
            if (x_max < point[0]):
                x_max = point[0]
            elif(x_min > point[0]):
                x_min = point[0]


# Load the STL files
your_mesh = mesh.Mesh.from_file('Models/PLA_190to220_stl_file.stl')

mesh_points = your_mesh.points
# print(mesh_points)
find_mins_maxs(your_mesh)
# print(your_mesh.vectors)
# print(your_mesh.normals)
# print(find_mins_maxs(your_mesh))





# # Create a new plot
# figure = pyplot.figure()
# axes = mplot3d.Axes3D(figure)
#

# axes.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))
#
# # Auto scale to the mesh size
# scale = your_mesh.points.flatten(-1)
# # print(scale)
# axes.auto_scale_xyz(scale, scale, scale)
# # Show the plot to the screen
# pyplot.show()

