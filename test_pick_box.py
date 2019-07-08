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



# p1 = np.array([0.47385777674956897, 0.4088556229844633, 0.08684120687317282])
# p2 = np.array([1.0155085086282054, -0.660885834542829, 0.08676025571748103])
# p3 = np.array([0.4979209452684969, -0.6809521734628257, 0.08680421672618033])
p1 = np.array([0.47385777674956897, 0.4088556229844633, 0.2989997563673698])
p2 = np.array([1.0155085086282054, -0.660885834542829, 0.2989997563673698])
p3 = np.array([0.4979209452684969, -0.6809521734628257, 0.2989997563673698])
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
a = 0.05
point_of_box = H.dot([1.043, 0.033, 0.01, 1])
pos_of_box = [point_of_box[0], point_of_box[1], point_of_box[2], -2.91, 1.18, 0]



pos = pos_of_box.copy()
rob.movel((pos[0], pos[1], pos[2] + 0.2, pos[3], pos[4], pos[5]),v, a)


rob.movel((pos[0], pos[1], pos[2], pos[3], pos[4], pos[5]),v, a)


print("Closing")
# закрыть захват
rob.send_program('set_tool_digital_out(0, True)')
rob.send_program('set_tool_digital_out(1, False)')
time.sleep(0.5)
print("Closed")


rob.movel((pos[0], pos[1], pos[2] + 0.2, pos[3], pos[4], pos[5]),v, a)



print("Fished")
rob.stop()
rob.close()
exit(0)