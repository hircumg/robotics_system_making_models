import urx
import numpy as np
from elementary_transformations import getMatrix
import time
import json


def open_gripper():
    # print("Opening")
    # открыть захват
    rob.send_program('set_tool_digital_out(0, False)')
    rob.send_program('set_tool_digital_out(1, True)')
    time.sleep(0.3)
    # print("Opened")

def close_gripper():
    # print("Closing")
    # закрыть захват
    rob.send_program('set_tool_digital_out(0, True)')
    rob.send_program('set_tool_digital_out(1, False)')
    time.sleep(0.7)
    # print("Closed")


def pick_box_from_plane(travel_height):
    a_picking = 0.2
    t_point = H_building.dot([0.0, 0.0, 0.2, 1])
    pos = [t_point[0], t_point[1], t_point[2], -2.91, 1.18, 0]
    rob.movel((pos[0], pos[1], max(travel_height, pos[2]), pos[3], pos[4], pos[5]), v, a_picking)

    # t_point = H_building.dot([0.11, 0.1, 0.115, 1])
    t_point = H_building.dot([0.035, 0.02, 0.045, 1])
    pos = [t_point[0], t_point[1], t_point[2], -2.28, 0.61, -0.55]
    rob.movel((pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]), v, a_picking)


    t_point = H_building.dot([0.01, 0.00, 0.015, 1])
    pos = [t_point[0], t_point[1], t_point[2], -2.28, 0.61, -0.55]
    rob.movel((pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]), v, a_picking)

    close_gripper()

    t_point = H_building.dot([-0.1, -0.1, 0.215, 1])
    # t_point = H_building.dot([0.0, 0.0, 0.2, 1])
    pos = [t_point[0], t_point[1], t_point[2], -2.91, 1.18, 0]
    rob.movel((pos[0], pos[1], max(travel_height, pos[2]), pos[3], pos[4], pos[5]), v, a)



rob = urx.Robot("160.69.69.23")

pos = rob.getl()
print(pos)


# p1 = np.array([0.47385777674956897, 0.4088556229844633, 0.08684120687317282])
# p2 = np.array([1.0155085086282054, -0.660885834542829, 0.08676025571748103])
# p3 = np.array([0.4979209452684969, -0.6809521734628257, 0.08680421672618033])
# p1 = np.array([0.47385777674956897, 0.4088556229844633, 0.2989997563673698 + 0.042])
# p2 = np.array([1.0155085086282054, -0.660885834542829, 0.2989997563673698 + 0.042])
# p3 = np.array([0.4979209452684969, -0.6809521734628257, 0.2989997563673698 + 0.042])

p1 = np.array([0.5403379359301442, -0.42697253272448493, 0.3052654374175694])
p2 = np.array([-0.5452210814556253, -0.9466671292345479, 0.3203002823459069])
p3 = np.array([-0.5511433029844419, -0.42697986096504187, 0.3031129074022326])
H_building = getMatrix(p1, p2, p3)

orientation_x = [-1.18, 2.91, 0.00]
orientation_y = [-2.91, 1.18, 0]


building_seq = []
with open("building_seq.txt", "r") as inputfile:
    building_seq = [ json.loads(i.rstrip("\n"))  for i in inputfile.readlines()]
    print(building_seq)

open_gripper()

v = 1
a = 0.4
point_of_box = H_building.dot([0.0, 0.00, 0.2, 1])
pos_of_box = [point_of_box[0], point_of_box[1], point_of_box[2]] + orientation_y

pos = [point_of_box[0], point_of_box[1], point_of_box[2]] + orientation_y
rob.movel((pos[0], pos[1], pos[2] + 0.2, pos[3], pos[4], pos[5]),v, a)

# print(pos)
# print("Fished")
# rob.stop()
# rob.close()
# exit(0)

# print("picking")
# pick_box(0.2)
#
# print("Fished")
# rob.stop()


# rob.close()
# exit(0)




offset = [0.2, 0.2, 0.012]
print("Placing begun")

for seq in building_seq:

    point = [seq.get('x'), seq.get('y'), seq.get('z')]


    glue = seq.get("glue")
    dx = 0.05 * (glue.get('left') - glue.get('right'))
    dy = 0.05 * (glue.get('down')-glue.get('up') )
    dz = 0.05 * glue.get('bottom')

    print("Placing in point %s and dx: %f, dy: %f, dz: %f" % (point,dx, dy,dz))


    v_temp_0= [point[0] + offset[0], point[1] + offset[1], point[2] + 0.042 + offset[2] * int((dy != 0) and (dx != 0)), 1]
    pos[:3] = H_building.dot(v_temp_0)[0:3]

    if (dy == 0) and (dx != 0):
        pos[3:] = orientation_y
    else:
        pos[3:] = orientation_x

    travel_height = max(pos_of_box[2], pos[2]) + 0.3


    pick_box_from_plane(travel_height)



    # move to position in the same height as went up from box with shifting
    v_temp = v_temp_0.copy()
    v_temp[0] = v_temp_0[0] + dx
    v_temp[1] = v_temp_0[1] + dy
    pos[:3] = H_building.dot(v_temp)[0:3]
    rob.movel((pos[0], pos[1], travel_height, pos[3], pos[4], pos[5]), v, a)

    # move to box position with shifting
    v_temp = v_temp_0.copy()
    v_temp[0] = v_temp_0[0] + dx
    v_temp[1] = v_temp_0[1] + dy
    v_temp[2] = v_temp_0[2] + dz
    pos[:3] = H_building.dot(v_temp)[0:3]
    rob.movel((pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]), v, a)



    # move to box position
    pos[:3] = H_building.dot(v_temp_0)[0:3]
    rob.movel((pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]), v, a)

    time.sleep(0.2)
    open_gripper()


    print("Placed in point %s" % point)


    # move to box upper position
    rob.movel((pos[0], pos[1], travel_height, pos[3], pos[4], pos[5]), v, a)



    # # move to box picking
    # rob.movel((pos_of_box[0], pos_of_box[1], travel_height, pos_of_box[3], pos_of_box[4], pos_of_box[5]), v, a)


    print("Finished with point %s" % point)


print("Placing fished")
rob.stop()
rob.close()
