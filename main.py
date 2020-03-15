from stl import mesh
import numpy as np
from plotting import plot_points3d, plot_mesh, set_ploting_required
from reading import make_slice
import json



def get_milling_sequence(sliced_image, drilling_radius, drilling_height):
    trajectory = []
    points = {'p0':(0,0,0)}
    point_iter = 1
    is_milling = False
    t_point = 'p0'
    t_point_old = 'p0'
    for i in range(sliced_image.shape[2]-1,0-1,-1):
        for j in range(sliced_image.shape[1]):
            for k in range(sliced_image.shape[0]):
                if sliced_image[k,j,i] == 1:
                    if not is_milling:
                        t_point = 'p' + str(point_iter)
                        trajectory.append({'type': 'lin', 'proc': is_milling, 'points': [t_point_old, t_point]})
                        t_point_old = t_point

                        t_point = 'p' + str(point_iter+1)
                        points.update({t_point_old : (drilling_radius*k, drilling_radius*j, drilling_height*(i+1))})
                        points.update({t_point : (drilling_radius*k, drilling_radius*j, drilling_height*i)})
                        is_milling = True
                        trajectory.append({'type': 'lin', 'proc': is_milling, 'points': [t_point_old, t_point]})
                        t_point_old = t_point
                        point_iter += 2

                else:
                    if is_milling:
                        t_point = 'p' + str(point_iter)
                        trajectory.append({'type': 'lin', 'proc': is_milling, 'points': [t_point_old, t_point]})
                        t_point_old = t_point

                        t_point = 'p' + str(point_iter+1)
                        points.update({t_point_old : (drilling_radius*k, drilling_radius*j, drilling_height*i)})
                        points.update({t_point : (drilling_radius*k, drilling_radius*j, drilling_height*(i+1))})
                        is_milling = False
                        trajectory.append({'type': 'lin', 'proc': is_milling, 'points': [t_point_old, t_point]})
                        t_point_old = t_point
                        point_iter +=2

            if is_milling:
                t_point = 'p' + str(point_iter)
                trajectory.append({'type': 'lin', 'proc': is_milling, 'points': [t_point_old, t_point]})
                t_point_old = t_point

                t_point = 'p' + str(point_iter+1)
                points.update({t_point_old : (drilling_radius * k, drilling_radius * j, drilling_height * i)})
                points.update({t_point : (drilling_radius * k, drilling_radius * j, drilling_height * (i + 1))})
                is_milling = False
                trajectory.append({'type': 'lin', 'proc': is_milling, 'points': [t_point_old, t_point]})
                t_point_old = t_point
                point_iter += 2

    return {'points':points, 'trajectory': trajectory}


if __name__ == '__main__':
    # Load the STL files
    your_mesh = mesh.Mesh.from_file('Models/piramid_50.stl')
    plot_mesh(your_mesh)
    box_size = 5
    my_sliced_mesh = make_slice(your_mesh, box_size)
    # my_sliced_mesh[:,:,::-1]
    for i in range(my_sliced_mesh.shape[2]):
        print(my_sliced_mesh[:,:,i])
    commands =   get_milling_sequence(my_sliced_mesh,box_size, box_size)


    output_file = "test.txt"
    if output_file is not None:
        outputfile = open(output_file,"w")
    print(commands)
    if output_file is not None:
        outputfile.write(json.dumps(commands['points']) + "\n")
        outputfile.write(json.dumps(commands['trajectory']) + "\n")
    print("Finished")