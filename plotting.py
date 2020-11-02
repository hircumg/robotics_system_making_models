import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot
from mpl_toolkits import mplot3d


def plot_mesh(mesh, debug=False):
    if not debug:
        return 0

    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh.vectors))

    # Auto scale to the mesh size
    scale = mesh.points.flatten('F')
    axes.auto_scale_xyz(scale, scale, scale)
    # Show the plot to the screen
    # print("plotted mesh")
    pyplot.show()


def plot_points3d(points3d, box_size, filename=None, debug=False):
    if not debug:
        return 0

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
                    if points3d[i, j, k] % 2 == 1:
                        x.append(i*box_size)
                        y.append(j*box_size)
                        z.append(k*box_size)
    elif len(points3d.shape) == 2:
        for i in range(points3d.shape[0]):
            for j in range(points3d.shape[1]):
                if points3d[i, j] % 2 == 1:
                    x.append(i*box_size)
                    y.append(j*box_size)
                    z.append(0)
    ax.scatter3D(x, y, z, c='b', marker='o')

    # ax.annotate("A", (x[0], y[0], z[0]))

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # print("plotted 3d points")
    if filename is not None:
        plt.savefig(filename, format='png')
    plt.show()


def plot_lines3d(slice, box_size, debug=False):
    if not debug:
        return 0

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
    for i in range(len(slice)):
        ax.plot(slice[i][::,0], slice[i][::,1], i*box_size, c='b', marker='o')

    # ax.annotate("A", (x[0], y[0], z[0]))

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

def plot_lines(lines, debug=False):
    if not debug:
        return 0

    """
    Plotting border of slice
    :param lines: array of lines for plotting
    :return: nothing
    """
    for line in lines:
        plt.plot([line[0][0], line[1][0]], [line[0][1], line[1][1]], marker='o', markerfacecolor='red', markersize=5, color='skyblue', linewidth=4)
     # plt.plot(all_lines, marker='o', markerfacecolor='red', markersize=5, color='skyblue', linewidth=4)

    plt.show()

def plot_vectors(vectors, debug=False):
    if not debug:
        return 0
    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)

    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(vectors))

    # Auto scale to the mesh size
    try:
        scale = np.concatenate([v[0] for v in vectors]).flatten('F')
        axes.auto_scale_xyz(scale, scale, scale)

        # Show the plot to the screen
        pyplot.show()
    except ValueError:
        pass

def plot_points(points, box_size=1, debug=False):
    if not debug:
        return 0

    """
    Plotting array where indexes is coordinates of plotting points.
    Point will be plotted only if element value is 1
    :param points: two-dimensional binary array
    :return: nothing
    """
    for i in range(points.shape[0]):
        for j in range(points.shape[1]):
            if points[i, j] % 2 == 1:
                plt.plot(i * box_size, j * box_size, 'bo')
    plt.show()