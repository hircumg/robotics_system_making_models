from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt
from meshdiff import *
from plotting import plot_mesh
# cube = mesh.Mesh.from_file('Models/cube.stl')
cube = mesh.Mesh.from_file('Models/box_100.stl')
# pyramid = mesh.Mesh.from_file('Models/pyramid.stl')
pyramid = mesh.Mesh.from_file('Models/model1.stl')
#pyramid = mesh.Mesh.from_file('Models/small.stl')
# pyramid = mesh.Mesh.from_file('Models/cone.stl')
plot_mesh(cube)
plot_mesh(pyramid)

#import pdb; pdb.set_trace() 

meshDiff = MeshDiff()
meshDiff.loadStl(cube,external=True)
meshDiff.loadStl(pyramid,external=False) 


obj = meshDiff.eval()
plot_mesh(obj)

# # plot
# figure = plt.figure()
# axes = mplot3d.Axes3D(figure)
# axes.add_collection3d(mplot3d.art3d.Poly3DCollection(obj.vectors))
# scale = obj.points.flatten('F')
# axes.auto_scale_xyz(scale, scale, scale)
# plt.show()
