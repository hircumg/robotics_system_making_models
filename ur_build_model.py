import urx
import numpy as np
from elementary_transformations import getMatrix
import time
import json


rob = urx.Robot("160.69.69.23")

pos = rob.getl()
print(pos)

# pos[3:] = [-1.57, 0, 0] # forward
# pos[3:] = [-3.14, 0, 0] # down



p1 = np.array([0.47385777674956897, 0.4088556229844633, 0.08684120687317282])
p2 = np.array([1.0155085086282054, -0.660885834542829, 0.08676025571748103])
p3 = np.array([0.4979209452684969, -0.6809521734628257, 0.08680421672618033])
H = getMatrix(p1, p2, p3)

building_seq = []
with open("building_seq.txt", "r") as inputfile:
    building_seq = [ json.loads(i.rstrip("\n"))  for i in inputfile.readlines()]
    print(building_seq)



v = 0.6
a = 0.2
point_of_box = H.dot([1, 0, 0.1, 1])
pos_of_box = [point_of_box[0], point_of_box[1], point_of_box[2], -3.14, 0, 0]

pos = pos_of_box.copy()
rob.movel((pos[0], pos[1], pos[2] + 0.2, pos[3], pos[4], pos[5]),v, a)





offset = [0.3, 0.15]
print("Placing begun")

for seq in building_seq:
    point = [seq.get('x'), seq.get('y'), seq.get('z')]
    print("Placing in point %s" %point)
    v_temp = H.dot([point[0]+offset[0], point[1]+offset[1], point[2], 1])
    pos[:3] = v_temp[:3]
    travel_heigt = max(pos_of_box[2], pos[2]) + 0.3

    # move to box
    rob.movel((pos_of_box[0], pos_of_box[1], pos_of_box[2],
               pos_of_box[3], pos_of_box[4], pos_of_box[5]), v, a)

    # pick up box


    # go up from box
    rob.movel((pos_of_box[0], pos_of_box[1], travel_heigt,
               pos_of_box[3], pos_of_box[4], pos_of_box[5]), v, a)

    # move to position in the same height as went up from box
    rob.movel((pos[0], pos[1], travel_heigt, pos[3], pos[4], pos[5]), v, a)

    # move to box position
    rob.movel((pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]), v, a)


#   place box

    print("Placed in point %s" % point)
    time.sleep(1.5)

    # move to box upper position
    rob.movel((pos[0], pos[1], travel_heigt, pos[3], pos[4], pos[5]), v, a)

    # move to box
    rob.movel((pos_of_box[0], pos_of_box[1], travel_heigt,
               pos_of_box[3], pos_of_box[4], pos_of_box[5]), v, a)

    print("Finished with point %s" % point)

print("Placing fished")
rob.stop()
rob.close()
