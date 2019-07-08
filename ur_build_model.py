import urx
import numpy as np
from elementary_transformations import getMatrix
import time
import json


rob = urx.Robot("160.69.69.23")

pos = rob.getl()
print(pos)



# p1 = np.array([0.47385777674956897, 0.4088556229844633, 0.08684120687317282])
# p2 = np.array([1.0155085086282054, -0.660885834542829, 0.08676025571748103])
# p3 = np.array([0.4979209452684969, -0.6809521734628257, 0.08680421672618033])
p1 = np.array([0.47385777674956897, 0.4088556229844633, 0.2989997563673698 + 0.042])
p2 = np.array([1.0155085086282054, -0.660885834542829, 0.2989997563673698 + 0.042])
p3 = np.array([0.4979209452684969, -0.6809521734628257, 0.2989997563673698 + 0.042])
H = getMatrix(p1, p2, p3)

building_seq = []
with open("building_seq.txt", "r") as inputfile:
    building_seq = [ json.loads(i.rstrip("\n"))  for i in inputfile.readlines()]
    print(building_seq)


print("Opening")
# открыть захват
rob.send_program('set_tool_digital_out(0, False)')
rob.send_program('set_tool_digital_out(1, True)')
time.sleep(0.5)
print("Opened")

v = 0.6
a = 0.2
point_of_box = H.dot([1.043, 0.033, 0.0, 1])
pos_of_box = [point_of_box[0], point_of_box[1], point_of_box[2], -2.91, 1.18, 0]

pos = pos_of_box.copy()
rob.movel((pos[0], pos[1], pos[2] + 0.2, pos[3], pos[4], pos[5]),v, a)


# rob.movel((pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]),v, a)

# print("Fished")
# rob.stop()
# rob.close()
# exit(0)


offset = [0.3, 0.15, 0.012]
print("Placing begun")

for seq in building_seq:

    point = [seq.get('x'), seq.get('y'), seq.get('z')]


    glue = seq.get("glue")
    dx = 0.05 * (-glue.get('up') + glue.get('down'))
    dy = 0.05 * (-glue.get('left') + glue.get('right'))
    dz = 0.05 * glue.get('bottom')

    print("Placing in point %s and dx: %f, dy: %f, dz: %f" % (point,dx, dy,dz))

    v_temp = H.dot([point[0]+offset[0], point[1]+offset[1], point[2] + offset[2]*abs(dy/0.05), 1])
    pos[:3] = v_temp[:3]
    travel_height = max(pos_of_box[2], pos[2]) + 0.3

    # move to box
    rob.movel((pos_of_box[0], pos_of_box[1], pos_of_box[2],
               pos_of_box[3], pos_of_box[4], pos_of_box[5]), v, a)

    # pick up box
    print("Closing")
    # закрыть захват
    rob.send_program('set_tool_digital_out(0, True)')
    rob.send_program('set_tool_digital_out(1, False)')
    time.sleep(0.5)
    print("Closed")

    # go up from box
    rob.movel((pos_of_box[0], pos_of_box[1], travel_height,
               pos_of_box[3], pos_of_box[4], pos_of_box[5]), v, a)




    # move to position in the same height as went up from box with shifting
    rob.movel((pos[0]+dx, pos[1]+dy, travel_height, pos[3], pos[4], pos[5]), v, a)


    # move to box position with shifting
    rob.movel((pos[0]+dx, pos[1]+dy, pos[2]+dz, pos[3], pos[4], pos[5]), v, a)


    # move to box position
    rob.movel((pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]), v, a)

    time.sleep(0.5)
#   place box
    print("Opening")
    # открыть захват
    rob.send_program('set_tool_digital_out(0, False)')
    rob.send_program('set_tool_digital_out(1, True)')
    time.sleep(0.1)
    print("Opened")



    print("Placed in point %s" % point)
    # time.sleep(1)

    # move to box upper position
    rob.movel((pos[0], pos[1], travel_height, pos[3], pos[4], pos[5]), v, a)

    # move to box
    rob.movel((pos_of_box[0], pos_of_box[1], travel_height,
               pos_of_box[3], pos_of_box[4], pos_of_box[5]), v, a)

    print("Finished with point %s" % point)
    time.sleep(0.5)

print("Placing fished")
rob.stop()
rob.close()
