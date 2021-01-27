# Some ideas about the function output

# function returns the trajectory in general form
trajectory = [cmd1,cmd2,...] # etc.

# point representation
p = [x,y,z,a,b,c]       # or
p = [x,y,z]             # for constant orientation

# linear motion
cmd = {
  'type': 'lin',          # motion type
  'proc': True/False,     # True in case of a tool contact
  'points': [p1,p2,...]   # list of points
}

# circular motion
cmd = {
  'type': 'circ',
  'proc': True/False,
  'points': [p1,p2],       # use 3 points prepresentation
  'full' : True/False      # False - stop in the last point, True - full circle
}

# spline
cmd = {
  'type': 'spline',
  'proc': True/False,
  'points': [p1,p2,...]   # all required intermediate points
}

# repeat N times
cmd = {
  'type': 'loop',
  'iter': N,              # number of iterations
  'do': [cmd1,cmd2,...]
}


# p = {'p1': (x1,y1,z1), 'p2': (x2,y2,z2)}
# trajectory = [{'type':'lin', 'points': ['p1','p2','p1'],...}]
