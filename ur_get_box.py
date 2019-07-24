import urx
import numpy as np
from elementary_transformations import getMatrix
import time


def open_gripper():
    # print("Opening")
    # open gripper
    time.sleep(0.1)
    rob.send_program('set_tool_digital_out(0, False)')
    rob.send_program('set_tool_digital_out(1, True)')
    time.sleep(0.2)
    # print("Opened")

def close_gripper():
    # print("Closing")
    # close gripper
    rob.send_program('set_tool_digital_out(0, True)')
    rob.send_program('set_tool_digital_out(1, False)')
    time.sleep(0.7)
    # print("Closed")


def catch_the_box(box_point):
    plane_location = H_kinect.dot([0.9, 0, 0.4, 1])
    pos = [plane_location[0], plane_location[1], plane_location[2]] + orientation_y
    rob.movel((pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]), v, a)


    # move to the box position
    pos[:3] = H_kinect.dot([box_point[0], box_point[1], box_point[2], 1])[:3]
    rob.movel((pos[0], pos[1], plane_location[2], pos[3], pos[4], pos[5]), v, a)



    # pick up the box
    pos[:3] = H_kinect.dot([box_point[0], box_point[1], box_point[2] - 0.1, 1])[:3]
    rob.movel((pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]), v, a)

    # close_gripper()


    # move to the transfer height
    pos[:3] = H_kinect.dot([box_point[0], box_point[1], box_point[2], 1])[:3]
    rob.movel((pos[0], pos[1], plane_location[2], pos[3], pos[4], pos[5]), v, a)


    # move to the incline plane position
    pos[:3] = H_kinect.dot([0.9, -0.10, 0.4, 1])[:3]
    pos[3:] = [-2.28, 0.61, -0.55]
    rob.movel((pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]), v, a)


    # place in the incline plane
    pos[:3] = H_kinect.dot([0.95, -0.09, 0.09, 1])[:3]
    rob.movel((pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]), v, a)

    # open_gripper()

    # go upper
    pos[:3] = H_kinect.dot([0.9, 0, 0.4, 1])[:3]
    pos[3:] = orientation_y
    rob.movel((pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]), v, a)










rob = urx.Robot("160.69.69.23")

# pos = rob.getl()
# print(pos)


p1 = np.array([0.32387277860560276, -0.5778972312437127, 0.30890229320791185])
p2 = np.array([-0.6478244775281674, -0.9379818644945974, 0.3176667810315073])
p3 = np.array([-0.6478208024938641, -0.5779228733848542, 0.3130699793990853])
H_building = getMatrix(p1, p2, p3)

orientation_x = [-1.18, 2.91, 0.00]
orientation_y = [-2.91, 1.18, 0]

open_gripper()

v = 1
a = 0.1

point_of_kinect = np.array([0.278, 0.25, 1.03, 1])
point_in_kinect = np.array([-0.12, 0.12, 0.8, 1])

t_point = [round(point_of_kinect[0] + point_in_kinect[0], 2),
           round(point_of_kinect[1] - point_in_kinect[1], 2),
           round(point_of_kinect[2] - point_in_kinect[2], 2), 1]


print(t_point)

catch_the_box(t_point)



print("Box location finished finished")
rob.stop()
rob.close()
exit(0)