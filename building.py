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
    print(best_substrate, best_substrate.argmax())
    return best_substrate.argmax()

def provide_best_substrate(sliced_mesh):
    new_mesh = sliced_mesh.copy()
    best_substrate_ind = get_max_side(sliced_mesh)
    if best_substrate_ind == 0:
        new_mesh = np.rot90(new_mesh, 1, (1, 2))
    elif best_substrate_ind == 1:
        new_mesh = np.rot90(new_mesh, 1, (2, 1))
    elif best_substrate_ind == 2:
        new_mesh = np.rot90(new_mesh, 1, (0, 2))
    elif best_substrate_ind == 3:
        new_mesh = np.rot90(new_mesh, 1, (2, 0))
    elif best_substrate_ind == 4:
        pass
    elif best_substrate_ind == 5:
        new_mesh = np.rot90(new_mesh, 2, (2, 0))
    else:
        new_mesh = sliced_mesh.copy()

    return new_mesh

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
        for i in range(mesh_size[0]):
            for j in range(mesh_size[1]):
                if(sliced_mesh[i,j,k] == 1):
                    if(k != 0 and sliced_mesh[i,j,k-1] == 1):
                        sequence.append([i*box_size, j*box_size, k * box_size])
                    else:
                        in_queue.append([i,j])

        for j in range(len(in_queue)):
            i = 0
            while i < len(in_queue):
                item = in_queue[i]
                step = (sliced_mesh[item[0]-1, item[1], k] * int(item[0] - 1 >= 0) +
                        sliced_mesh[(item[0] + 1) % mesh_size[0], item[1], k] * int(item[0] + 1 < mesh_size[0]) +
                        sliced_mesh[item[0], item[1] - 1, k] * int(item[1] - 1 >= 0) +
                        sliced_mesh[item[0], (item[1] + 1) % mesh_size[1], k] * int(item[1] + 1 < mesh_size[1]))
                if(step > 0):
                    sequence.append([item[0]*box_size, item[1]*box_size, k * box_size])
                    in_queue.pop(i)
                else:
                    i += 1
            if(len(in_queue) == 0):
                break

        print("Left len of external: %i for %i" %(len(in_queue), k))

    return sequence



if __name__ == '__main__':
    box  = 10
    # Load the STL files
    # your_mesh = mesh.Mesh.from_file('Models/PLA_190to220_stl_file.stl')
    your_mesh = mesh.Mesh.from_file('Models/Minecraft_Hanger_hand_1.stl')
    # your_mesh = mesh.Mesh.from_file('Models/Groot_v1_1M_Merged.stl')
    # your_mesh = mesh.Mesh.from_file('Models/xyzCalibration_cube.stl')

    my_sliced_mesh = make_slice(your_mesh, box)
    my_sliced_mesh = provide_best_substrate(my_sliced_mesh)

    plot_points3d(my_sliced_mesh,box)

    len_of_slice = len(my_sliced_mesh[my_sliced_mesh == 1])
    sliced_sequence = get_building_sequence(my_sliced_mesh, box)
    print(len_of_slice, len(sliced_sequence))
    print(sliced_sequence)
