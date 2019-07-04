import urx
import numpy as np
from elementary_transformations import rx,ry,rz,tx,ty,tz
import time

rob = urx.Robot("160.69.69.23")

pos = rob.getl()
print(pos)

# pos[3:] = [-1.57, 0, 0] # forward
# pos[3:] = [-3.14, 0, 0] # down



p1 = np.array([0.47385777674956897, 0.4088556229844633, 0.08684120687317282])
p2 = np.array([1.0155085086282054, -0.660885834542829, 0.08676025571748103])
p3 = np.array([0.4979209452684969, -0.6809521734628257, 0.08680421672618033])

# p1 = np.array([-0.614, -0.281, -0.210])
# p2 = np.array([-0.559, -0.290, -0.025])
# p3 = np.array([-0.637, -0.109, -0.095])

translation = tx(p1[0]).dot(ty(p1[1])).dot(tz(p1[2]))

x_new = p3 - p1
x_new = x_new / np.linalg.norm(x_new)
x_old = np.array([1,0,0])

angle_z = np.arctan2(x_new[1], x_new[0])

rz_current = rz(angle_z)[0:3, 0:3]
vector_current = rz_current.dot(x_old)

angle_y = np.arctan2(-x_new[2], np.sqrt(x_new[0]**2 + x_new[1]**2))

ry_current = ry(angle_y)[0:3, 0:3]

y_new = p2 - p1
y_new = y_new / np.linalg.norm(y_new)

angle_x= np.arctan2(y_new[2], np.sqrt(y_new[0]**2 + y_new[1]**2))

# print(angle_x / np.pi * 180)
# print(angle_y / np.pi * 180)
# print(angle_z / np.pi * 180)
# print(translation)

rotation = rx(angle_x).dot(ry(angle_y)).dot(rz(angle_z))
H = translation.dot(rotation)
# print(H)







v = 0.5
a = 0.2
point_of_box = H.dot([1, 0, 0.1, 1])
pos_of_box = [point_of_box[0], point_of_box[1], point_of_box[2], -3.14, 0, 0]

pos = pos_of_box.copy()
rob.movel((pos[0], pos[1], pos[2] + 0.2, pos[3], pos[4], pos[5]),v, a)




# v_0 = H.dot([0, 0, 0.1, 1])
# pos[:3] = v
# rob.movel((pos[0],pos[1], pos[2], pos[3], pos[4], pos[5]),v, a, wait=False)
# while rob.getForce() < 50:
#     time.sleep(0.01)
#     if not rob.is_program_running():
#         break
# rob.stopl()
# exit(0)

# v_0 = H.dot([0, 0, 0.1, 1])
# v_1 = H.dot([1, 0, 0.1, 1])

# print(v_0)
# print(v_1)






# pos = [v_0[0], v_0[1], v_0[2], -3.14, 0, 0]


# pos[:3] = v_1[:3]
# rob.movel((pos[0],pos[1], pos[2], pos[3], pos[4], pos[5]),v, a)


building_seq = [[0.0,0.2,0.1],
                [0.1,0.2,0.1],
                [0.0,0.1,0.1],
                [0.1,0.1,0.1],
                [0.0,0.0,0.1],
                [0.1,0.0,0.1],
                [0.0,0.2,0.2]]

building_seq = [[0.0,0.2,0.1],
                [0.1,0.2,0.1]]

print("Placing begun")

for point in building_seq:
    print("Placing in point %s" %point)
    v_temp = H.dot([point[0], point[1], point[2], 1])
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
    time.sleep(3)

    # move to box upper position
    rob.movel((pos[0], pos[1], travel_heigt, pos[3], pos[4], pos[5]), v, a)

    # move to box
    rob.movel((pos_of_box[0], pos_of_box[1], travel_heigt,
               pos_of_box[3], pos_of_box[4], pos_of_box[5]), v, a)

    print("Finished with point %s" % point)

print("Placing fished")
rob.stop()
rob.close()
