from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt
from meshdiff import *

cube = mesh.Mesh.from_file('Models/cube.stl')
#pyramid = mesh.Mesh.from_file('Models/pyramid.stl')
#pyramid = mesh.Mesh.from_file('Models/small.stl')
pyramid = mesh.Mesh.from_file('Models/cone.stl')

#import pdb; pdb.set_trace() 

meshDiff = MeshDiff()
meshDiff.loadStl(cube,external=True)
meshDiff.loadStl(pyramid,external=False) 

obj = meshDiff.eval()

# plot
figure = plt.figure()
axes = mplot3d.Axes3D(figure)
axes.add_collection3d(mplot3d.art3d.Poly3DCollection(obj.vectors))
scale = obj.points.flatten(-1)
axes.auto_scale_xyz(scale, scale, scale)
plt.show()
