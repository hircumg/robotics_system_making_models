from stl import mesh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from reading import make_slice


def get_max_side(sliced_mesh):
    best_substrate = [sliced_mesh[0, :, :].sum(),
                      sliced_mesh[-1, :, :].sum(),
                      sliced_mesh[:, 0, :].sum(),
                      sliced_mesh[:, -1, :].sum(),
                      sliced_mesh[:, :, 0].sum(),
                      sliced_mesh[:, :, -1].sum()]

    best_substrate = np.array(best_substrate)
    print("Sides values %s, best side %i" %(best_substrate, best_substrate.argmax()))
    return best_substrate.argmax()

def provide_best_substrate(sliced_mesh):
    new_mesh = sliced_mesh.copy()
    best_substrate_ind = get_max_side(sliced_mesh)
    if best_substrate_ind == 0:
        new_mesh = np.rot90(new_mesh, 1, (0, 2))
    elif best_substrate_ind == 1:
        new_mesh = np.rot90(new_mesh, 1, (2, 0))
    elif best_substrate_ind == 2:
        new_mesh = np.rot90(new_mesh, 1, (1, 2))
    elif best_substrate_ind == 3:
        new_mesh = np.rot90(new_mesh, 1, (2, 1))
    elif best_substrate_ind == 4:
        pass
    elif best_substrate_ind == 5:
        new_mesh = np.rot90(new_mesh, 2, (2, 0))
    else:
        new_mesh = sliced_mesh.copy()

    return new_mesh, best_substrate_ind

def plot_points3d(points3d, box_size):
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

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()



def get_building_sequence(sliced_mesh, box_size):
    sequence = []
    mesh_size = sliced_mesh.shape
    in_queue = []
    for k in range(mesh_size[2]):
        for j in reversed(range(mesh_size[1])):
            for i in range(mesh_size[0]):
                if(sliced_mesh[i,j,k] == 1):
                    glue = {'up': (j + 1 < mesh_size[1]) and (sliced_mesh[i, j + 1, k] > 0),
                            'left': (i - 1 >= 0) and (sliced_mesh[i - 1, j, k] > 0),
                            'down': False,
                            'right': False,
                            'top': False,
                            'bottom': k > 0}
                    if k == 0 or sliced_mesh[i, j, k - 1] == 2:
                        sequence.append({'x': i * box_size, 'y': j * box_size, 'z': k * box_size, 'glue': glue})
                        sliced_mesh[i, j, k] = 2
                    else:
                        in_queue.append([i,j])

        print("Initially left number of external elements %i for %i" % (len(in_queue), k))
        for j in range(len(in_queue)):
            i = 0
            while i < len(in_queue):
                item = in_queue[i]
                step = (int(sliced_mesh[item[0]-1, item[1], k] == 2) * int(item[0] - 1 >= 0) +
                        int(sliced_mesh[(item[0] + 1) % mesh_size[0], item[1], k] == 2) * int(item[0] + 1 < mesh_size[0]) +
                        int(sliced_mesh[item[0], item[1] - 1, k] == 2) * int(item[1] - 1 >= 0) +
                        int(sliced_mesh[item[0], (item[1] + 1) % mesh_size[1], k] == 2) * int(item[1] + 1 < mesh_size[1]))
                if(step > 0):
                    glue = {'up': (j + 1 < mesh_size[1]) and (sliced_mesh[i, j + 1, k] > 0),
                            'left': (i - 1 >= 0) and (sliced_mesh[i - 1, j, k] > 0),
                            'down': (j - 1 >= 0) and (sliced_mesh[i, j - 1, k] > 0) ,
                            'right': (i + 1 < mesh_size[0]) and (sliced_mesh[i + 1, j, k] > 0),
                            'top': False,
                            'bottom': False}
                    sliced_mesh[item[0], item[1], k] = 2
                    # sequence.append([item[0]*box_size, item[1]*box_size, k * box_size])
                    sequence.append({'x': item[0]*box_size, 'y': item[1]*box_size, 'z': k * box_size, 'glue': glue})
                    in_queue.pop(i)
                else:
                    i += 1
            if(len(in_queue) == 0):
                break

        print("Left number of external elements %i for %i" %(len(in_queue), k))

    return sequence

def plot_mesh(mesh):
    from matplotlib import pyplot
    from mpl_toolkits import mplot3d
    # Create a new plot
    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)


    axes.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh.vectors))

    # Auto scale to the mesh size
    scale = mesh.points.flatten(-1)
    axes.auto_scale_xyz(scale, scale, scale)

    # Show the plot to the screen
    pyplot.show()


if __name__ == '__main__':
    box  = 100
    # Load the STL files
    # your_mesh = mesh.Mesh.from_file('Models/PLA_190to220_stl_file.stl')
    # your_mesh = mesh.Mesh.from_file('Models/Minecraft_Hanger_hand_1.stl')
    # your_mesh = mesh.Mesh.from_file('Models/inclined_plane.stl')
    your_mesh = mesh.Mesh.from_file('Models/demo_1.stl')
    # your_mesh = mesh.Mesh.from_file('Models/for_test_1.stl')
    # your_mesh = mesh.Mesh.from_file('Models/for_test_2.stl')
    # your_mesh = mesh.Mesh.from_file('Models/Groot_v1_1M_Merged.stl')
    # your_mesh = mesh.Mesh.from_file('Models/xyzCalibration_cube.stl')

    plot_mesh(your_mesh)
    my_sliced_mesh = make_slice(your_mesh, box)

    plot_points3d(my_sliced_mesh, box)
    my_sliced_mesh, orient = provide_best_substrate(my_sliced_mesh)

    plot_points3d(my_sliced_mesh,box)

    len_of_slice = len(my_sliced_mesh[my_sliced_mesh >= 1])
    sliced_sequence = get_building_sequence(my_sliced_mesh, box)

    for seq in sliced_sequence:
        # print(seq)
        print("[" + str(seq.get('x')/1000) + "," + str(seq.get('y')/1000) + "," + str((seq.get('z') + box)/1000) + "],")

