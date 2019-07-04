import numpy as np
from elementary_transformations import rx,ry,rz,tx,ty,tz 


p1 = np.array([0.47385777674956897, 0.4088556229844633, 0.08684120687317282])
p3 = np.array([0.4979209452684969, -0.6809521734628257, 0.08680421672618033])
p2 = np.array([1.0155085086282054, -0.660885834542829, 0.08676025571748103])
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

print(angle_x / np.pi * 180)
print(angle_y / np.pi * 180) 
print(angle_z / np.pi * 180) 
print(translation)