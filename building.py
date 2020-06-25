from stl import mesh
import numpy as np
from plotting import plot_points3d, plot_mesh, set_ploting_required
from reading import make_slice
import json

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




def get_building_sequence(sliced_mesh, box_size):
    sequence = []
    mesh_size = sliced_mesh.shape
    in_queue = []
    for k in range(mesh_size[2]):
        for j in reversed(range(mesh_size[1])):
            for i in range(mesh_size[0]):
                if(sliced_mesh[i,j,k] == 1):
                    glue = {'up': int((j + 1 < mesh_size[1]) and ((sliced_mesh[i, j + 1, k] > 0) or ((i + 1 < mesh_size[0]) and (sliced_mesh[i+1, j + 1, k] > 0)))),
                            'left': int((i - 1 >= 0) and (sliced_mesh[i - 1, j, k] > 0)),
                            'down': int(False),
                            'right': int(False),
                            'top': int(False),
                            'bottom': int(True)}
                    if k == 0 or sliced_mesh[i, j, k - 1] == 2:
                        sequence.append({'x': i * box_size, 'y': j * box_size, 'z': (k) * box_size, 'glue': glue})
                        sliced_mesh[i, j, k] = 2
                    else:
                        in_queue.append([i,j])

        # print("Initially left number of external elements %i for %i" % (len(in_queue), k))
        for j in range(len(in_queue)):
            i = 0
            while i < len(in_queue):
                item = in_queue[i]
                step = (int(sliced_mesh[item[0]-1, item[1], k] == 2) * int(item[0] - 1 >= 0) +
                        int(sliced_mesh[(item[0] + 1) % mesh_size[0], item[1], k] == 2) * int(item[0] + 1 < mesh_size[0]) +
                        int(sliced_mesh[item[0], item[1] - 1, k] == 2) * int(item[1] - 1 >= 0) +
                        int(sliced_mesh[item[0], (item[1] + 1) % mesh_size[1], k] == 2) * int(item[1] + 1 < mesh_size[1]))
                if(step > 0):
                    glue = {'up': int((j + 1 < mesh_size[1]) and (sliced_mesh[i, j + 1, k] > 0)),
                            'left': int((i - 1 >= 0) and (sliced_mesh[i - 1, j, k] > 0)),
                            'down': int((j - 1 >= 0) and (sliced_mesh[i, j - 1, k] > 0)) ,
                            'right': int((i + 1 < mesh_size[0]) and (sliced_mesh[i + 1, j, k] > 0)),
                            'top': int(False),
                            'bottom': int(False)}
                    sliced_mesh[item[0], item[1], k] = 2
                    # sequence.append([item[0]*box_size, item[1]*box_size, k * box_size])
                    sequence.append({'x': item[0]*box_size, 'y': item[1]*box_size, 'z': (k) * box_size, 'glue': glue})
                    in_queue.pop(i)
                else:
                    i += 1
            if(len(in_queue) == 0):
                break

        # print("Left number of external elements %i for %i" %(len(in_queue), k))

    return sequence


def generate_building_sequence(box_size, stl_model, output_file,plot_name=None, plotting=True):
    set_ploting_required(plotting)
    # logs = open('logs.txt', 'a+')
    # logs.write(f"Started for {stl_model} with bot size: {box_size}\n")
    # print(f"Started for {stl_model} with bot size: {box_size}")

    # Load the STL files
    your_mesh = mesh.Mesh.from_file(stl_model)
    plot_mesh(your_mesh)

    my_sliced_mesh, dt = make_slice(your_mesh, box_size)
    plot_points3d(my_sliced_mesh, box_size,filename=plot_name)
    vol = my_sliced_mesh.sum()*box_size**3
    # print('Slicing finished with time %i ns' % dt)
    # print(f"Approximated model volume {vol} mm^3")
    # logs.write('Slicing finished with time %i ns \n' % dt)
    # logs.write(f"Approximated model volume {vol} mm^3 \n")
    # logs.write(f"{stl_model};{box_size};{dt};{vol}\n")
    print(f"{stl_model};{box_size};{dt};{vol}\n")
    # logs.close()
    # my_sliced_mesh, orient = provide_best_substrate(my_sliced_mesh)
    # plot_points3d(my_sliced_mesh,box_size)

    len_of_slice = len(my_sliced_mesh[my_sliced_mesh >= 1])
    sliced_sequence = get_building_sequence(my_sliced_mesh, box_size)

    if output_file is not None:
        outputfile = open(output_file,"w")
    for seq in sliced_sequence:
        # print(seq)
        if output_file is not None:
            outputfile.write(json.dumps(seq) + "\n")
    # print("Finished")
    if output_file is not None:
        outputfile.close()
    return seq



if __name__ == '__main__':
    working_dir = 'models_test/'
    files = ['box', 'hemisphere', 'pyramid', 'model1', 'model2']
    box_sizes = range(5,105,5)
    # file = files[0]
    box_size = 25
    for file in files:
        generate_building_sequence(box_size, f'{working_dir}{file}.stl',
                                   f'{working_dir}sequences/{file}_{box_size}.txt',
                                   plot_name=f'{working_dir}fig/{file}_{box_size}.png',
                                   plotting=True)



