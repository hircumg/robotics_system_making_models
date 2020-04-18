# Generate difference between two STL objects
# Assumptions:
# - internal mesh is less or equal to external one 
# - different shapes can have different edges with the same group of verteces

import numpy as np
from stl import mesh

SMALL = 1E-5        # zero threshold
SMALL1 = 1+SMALL    # auxiliary constant

class Vertex:

  def __init__(self,p):
    self.v = p[:]          # [x,y,z]
    self.opposit = False   # lie on opposit triangle
    self.closest = None    # closest opposit vertex
    self.around = []       # triangles around this point
    self.ind = None        # ID
    self.original = True   # mark vertices on the border

  # check if 2 verteces close to each other
  def equal(self,obj):
    return self.absDist(obj) < SMALL

  # find sum of absolut differences for each coordinate
  def absDist(self,obj):
    if isinstance(obj,Vertex):
      obj = obj.v
    return np.sum(np.abs(obj-self.v))

  # set new closest vertex and update connection to opposit shape
  def updateClosest(self,v):
    self.closest = v
    self.opposit = False
    if v.hasOpposit(self):
      self.opposit = True

  # check if the given vertex lie in one of triangles
  def hasOpposit(self,v):
    for tr in self.around:
      if tr.isInside(v):
        return tr
    return None
  
  # get vertices around the current
  def circle(self):
    lst = []
    for tr in self.around:
      for v in tr.vert:
        if not (v.ind == self.ind or v in lst):
          lst.append(v)
    return lst
    
  # find list of triangles or exact triangle (if 3 verteces are given)
  def getTriangle(self,v2,v3=None):
    #lst = [t for t in self.around if t.indexOf(v2)]
    lst = [t for t in self.around if t in v2.around]
    if v3:
      for t in lst:
        if t.indexOf(v3) != None:
          return t
      else:
        return None
    return lst
    
  # check if verteces are at the same edge
  def isEdge(self,v):
    for tr in self.around:
      if tr.indexOf(v) is not None:
        return True
    return False

  # check if the vertex is between common and non-common triangles
#  def commonBorder(self):
#    lst = [t for t in self.around if t.common]
#    return 0 < len(lst) < len(self.around)
#    
  # number of common triangles around this vertex
  def numCommon(self):
    n = 0
    for tr in self.around:
      if tr.common: n += 1
    return n
    
class Triangle:

  def __init__(self, n, vs):
    self.normal = n
    self.vert = vs
    self.ind = None
    self.common = False


  # check if the vertex belongs to triangle
  # TODO: change algorithm to make it less dependent from SMALL value
  def isInside(self,x):
    if isinstance(x,Vertex):
      x = x.v
    v0,v1,v2 = self.vert
    s0 = np.abs(np.cross(v1.v - v0.v, v2.v - v0.v))
    if np.sum(s0) < SMALL: return False   # in fact, just line
    s1 = np.abs(np.cross(x - v0.v, x - v1.v))
    s2 = np.abs(np.cross(x - v1.v, x - v2.v))
    s3 = np.abs(np.cross(x - v2.v, x - v0.v))
    return abs(np.sum(s1+s2+s3-s0)) < SMALL
    
  # triangle area
  def area(self):
    v0,v1,v2 = self.vert
    return 0.5*np.linalg.norm(np.cross(v1.v - v0.v, v2.v - v0.v))
  
  # change sequence of verteces
  def changeOrientation(self):
    self.vert[1], self.vert[2] = self.vert[2], self.vert[1]
    return self 
    
  # find index of vertex in triangle list
  def indexOf(self,v):
    for i,val in enumerate(self.vert):
      if val.ind == v.ind: 
        return i
    return None
    
  # check if 2 or 3 verteces has the same position
  def isDegenerate(self):
    v0, v1, v2 = self.vert 
    return v0.absDist(v1) < SMALL or v1.absDist(v2) < SMALL or v2.absDist(v0) < SMALL
  
  # check intersection in plane
  def _trIntersection(self,tr):
    # check normals
    if np.sum(np.abs(self.normal-tr.normal)) > SMALL:
      return False   # not parallel
    # check distance between planes
    if abs(self.normal.dot(tr.vert[0].v-self.vert[0].v)) > SMALL:
      return False   # in it the same plane
    # check if they are inside (each other)
    p1,p2,p3 = self.vert
    c1 = (p1.v + p2.v + p3.v) / 3
    if tr.isInside(c1):
      return True
    q1,q2,q3 = tr.vert
    c2 = (q1.v + q2.v + q3.v) / 3
    if self.isInside(c2):
      return True
    # check intersection
    for xx in ((p1,p2),(p2,p3),(p3,p1)):
      for yy in ((q1,q2),(q2,q3),(q3,q1)):
        if self._lineIntersection(xx[0],xx[1],yy[0],yy[1]):
          return True
    return False

  # show in form of matrix (for debug)
  def matrix(self):
    return np.array([self.vert[0].v,self.vert[1].v,self.vert[2].v])

  # check if 2 segments have point of intersection
  def _lineIntersection(self,p1,p2,q1,q2):
    v1 = np.cross(p2.v-p1.v,q1.v-p2.v)
    v2 = np.cross(p2.v-p1.v,q2.v-p2.v)
    v3 = np.cross(q2.v-q1.v,p1.v-q2.v)
    v4 = np.cross(q2.v-q1.v,p2.v-q2.v)
    # check only for intersection
    return v1.dot(v2) < -SMALL and v3.dot(v4) < -SMALL 

  # check if the triangle lie on the opposit shape
  def check(self,v):
    self.common = False
    for tr in v.around:
      if self._trIntersection(tr):
        self.common = True
        return tr
    return None

class MeshDiff:

  def __init__(self):
    # external mesh
    self.exT = []
    self.exV = []
    # internal mesh
    self.inT = []
    self.inV = []
    
  def loadStl(self,stl,external=True):
    goalT = self.exT if external else self.inT
    goalV = self.exV if external else self.inV
    # read data
    for d in stl.data:
      # d is [normale,verteces,etc]
      trig = Triangle(d[0],[None,None,None])
      # add verteces
      for i,v in enumerate(d[1]):  
        # compare with verteces in dict
        for k in goalV:
          if k.equal(v):
            trig.vert[i] = k
            k.around.append(trig)
            break
        else: # not found
          vnew = Vertex(v)
          vnew.around.append(trig)
          goalV.append(vnew)
          trig.vert[i] = vnew
      # add triangle
      goalT.append(trig)
    # save ID
    for i,v in enumerate(goalT):
      v.ind = i
    for i,v in enumerate(goalV):
      v.ind = i
      
  # find closest vertex in list
  def _closestVertex(self,v0,vlst):
    vmin = None
    dmin = 1E20
    for vv in vlst:
      d = vv.absDist(v0)
      if d < dmin:
        dmin = d
        vmin = vv
        if dmin < SMALL: 
          break
    return vmin 
  
  # find closest vertex and triangle for each element
  def _findClosest(self):
    # compare internal mesh
    for v in self.inV:
      vmin = self._closestVertex(v,self.exV)
      v.updateClosest(vmin)
      vprev = vmin.closest
      if vprev == None or vmin.absDist(v) < vmin.absDist(vprev):
        vmin.updateClosest(v)
    # compare external mesh
    for v in self.exV:
      if v.closest == None:
        vmin = self._closestVertex(v,self.inV) 
        v.updateClosest(vmin)
    # check triangles
    for tr in self.inT:
      if tr.vert[0].opposit and tr.vert[1].opposit and tr.vert[2].opposit:
        for v in tr.vert:
          t = tr.check(v.closest)
          if t:
            t.common = True
            break
    for tr in self.exT:
      if tr.vert[0].opposit and tr.vert[1].opposit and tr.vert[2].opposit:
        for v in tr.vert:
          if not tr.common and tr.check(v.closest):
            break
    
  # make edges at the external shape  
  def _alignBorder(self,lst):
    vExPrev= None     # previous external vertex
    for vin in lst:            
      vex = vin.closest
      # add vertex if need
      if not vin.equal(vex):
        vex = self._newVertexExt(vin)   # insert new vertex near the given point     
      # edge
      if vExPrev:
        self._makeEdgeExt(vExPrev,vex)      
      vExPrev = vex
        
  # make new vertex at the external shape  
  def _newVertexExt(self,vin,triang=None,pos=None):
    # update 
    tr = vin.closest.hasOpposit(vin) if triang is None else triang
    v0, v1, v2 = tr.vert
    v = Vertex(vin.v if pos is None else pos)
    # first replace
    t1 = Triangle(tr.normal,[v,v0,v1])
    t1.ind = tr.ind; self.exT[tr.ind] = t1
    # other append
    t2 = Triangle(tr.normal,[v,v1,v2])
    t2.ind = len(self.exT); self.exT.append(t2)
    t3 = Triangle(tr.normal,[v,v2,v0])
    t3.ind = len(self.exT); self.exT.append(t3)
    # process vertex info
    v0.around.remove(tr);  v0.around += [t1,t3]
    v1.around.remove(tr);  v1.around += [t1,t2]
    v2.around.remove(tr);  v2.around += [t2,t3]
    # add vertex
    v.ind = len(self.exV)
    v.around = [t1,t2,t3]
    self.exV.append(v)
    v.updateClosest(vin)
    if triang is None and pos is None:
      vin.updateClosest(v)
    # check status and remove empty
    lst = (t1,t2,t3)
    for t in lst:
      if t.area() < SMALL:
        self._removeEmptyEx(t)
    for t in lst:
      if not t.common:
        for w in t.vert:
          if t.check(w.closest):
            break
    return v

  # delete triangle with empty area using rotation
  def _removeEmptyEx(self,tr0):
    if tr0.isDegenerate():
      #for v in tr0.vert:
      #  v.around.remove(tr0)
      return  # remove from list later
    v0, v1, v2 = tr0.vert
    if abs(v0.absDist(v1) + v0.absDist(v2) - v1.absDist(v2)) < SMALL:
      self._rotateTriangesEx(v1,v2)
    elif abs(v1.absDist(v0) + v1.absDist(v2) - v0.absDist(v2)) < SMALL:
      self._rotateTriangesEx(v2,v0)
    else:
      self._rotateTriangesEx(v0,v1)

  # change (rotate) internal edge for two adjacent triangles
  def _rotateTriangesEx(self,v1,v2):
    tr1, tr2 = v1.getTriangle(v2)
    # not on edge
    v01 = [v for v in tr1.vert if v.ind != v1.ind and v.ind != v2.ind][0]
    v02 = [v for v in tr2.vert if v.ind != v1.ind and v.ind != v2.ind][0]
    # first triangle
    ind = tr1.indexOf(v1) 
    tr1.vert[ind] = v02
    v1.around.remove(tr1)
    ind = tr2.indexOf(v2)
    tr2.vert[ind] = v01
    v2.around.remove(tr2)
    v01.around.append(tr2)
    v02.around.append(tr1)
    # update 
    for v in tr1.vert:
      if tr1.check(v.closest):
        break
    for v in tr2.vert:
      if tr2.check(v.closest):
        break

  # connect verteces at the external shape with edges
  # TODO: remove degenerate triangles - ?
  def _makeEdgeExt(self,vBeg,vEnd):
    vPrev = vBeg 
    group = [vBeg]  # intermediate verteces at the same surface
    while not vPrev.isEdge(vEnd):
      # find closest
      l1 = vPrev.circle()
      l1.sort(key=lambda x: -self._angleCos(vPrev,x,vEnd))
      vNext = l1[0]
      # already at the line
      if self._distToLine(vBeg,vEnd,vNext) < SMALL:
        vPrev = vNext
        group.append(vPrev)
        continue
      # intersection with edges
      vv = self._opposit(vPrev,vNext)
      for v in vv:
        point = self._getLineIntersection(vBeg,vEnd,vNext,v)
        # found intersection with edge
        if point is not None:
          tr = v.getTriangle(vPrev,vNext)
          vPrev = self._newVertexExt(vNext.closest,tr,point)
          group.append(vPrev)
          break
      else:
        # move verteces in all intermediate triangles
        if len(group) > 1:
          last = group[-1]
          for v in group[1:-1]:
            v.v = last.v
        group = []
        vPrev = vNext
    # update intermediate triangles
    if len(group) > 1:
      last = vEnd
      for v in group[1:]:
        v.v = last.v


#      point = self._getLineIntersection(vBeg,vEnd,vNext,vv[0])
#      # intersection with first edge
#      if point is not None:
#        tr = vv[0].getTriangle(vPrev,vNext)
#        vPrev = self._newVertexExt(vNext.closest,tr,point)
#        continue 
#      point = self._getLineIntersection(vBeg,vEnd,vNext,vv[1])
#      # intersection with second edge
#      if point is not None:
#        tr = vv[1].getTriangle(vPrev,vNext)
#        vPrev = self._newVertexExt(vNext.closest,tr,point)
#        continue 
      # find nothing, go further 
      #vPrev = vNext
  
  # find distance from point to line in space
  def _distToLine(self,xa,xb,x):
    xa, xb, x = xa.v, xb.v, x.v
    p = xb - xa
    return np.linalg.norm(np.cross(xa-x,p)) / np.linalg.norm(p)
   
  # find cosine between two vectors (x0x1 and x0x2)
  def _angleCos(self,x0,x1,x2):
    vec1 = x1.v - x0.v
    vec2 = x2.v - x0.v
    denom = np.linalg.norm(vec1)*np.linalg.norm(vec2)    
    return vec1.dot(vec2) / denom if denom > SMALL else 0 
    
  # find list of verteces that belong to triangles adjacent with edge
  def _opposit(self,v1,v2,v3=None):
    lst = v1.getTriangle(v2)
    return [v for v in lst[0].vert + lst[1].vert if v not in (v1,v2,v3)]

  # check if two lines have intersection and find its point
  def _getLineIntersection(self,a1,a2,b1,b2):
    p1 = a2.v - a1.v
    p2 = b2.v - b1.v
    dv = b1.v - a1.v
    i0,i1,i2,d = None,None,None,None
    for v in ((0,1,2),(0,2,1),(1,2,0)):
      i0, i1, i2 = v
      d = -p1[i0]*p2[i1] + p1[i1]*p2[i0]
      if abs(d) > SMALL:
        break
    else:
      return None
    # intersection in plane
    t1 = (-dv[i0]*p2[i1]+dv[i1]*p2[i0]) / d
    t2 = (p1[i0]*dv[i1]-p1[i1]*dv[i0]) / d
    # check intersection
    if -SMALL < t1 < SMALL1 and -SMALL < t2 < SMALL1:
      # check third coordinate
      if abs(p2[i2]*t2 - p1[i2]*t1 + dv[i2]) < SMALL:
        return a1.v + p1*t1
    return None
       
  # find sequence of verteces on the border between common and non common triangles  
  def _findContour(self,anchor):
    v_list = [] # internal vertices
    ai = anchor.ind
    tr = None
    # find initial triangle
    for t in anchor.around:
      if t.common:
        tr = t
        break 
    vedge, vprev = [v for v in tr.vert if v.ind != anchor.ind]
    while True:
      vnext = self._opposit(anchor,vedge,vprev)[0]
      t = anchor.getTriangle(vedge,vnext) 
      if t.common:
        vedge, vprev = vnext, vedge
      else:
        v_list.append(vedge)
        vedge.original = False
        anchor,vedge,vprev = vedge,vprev,anchor
        if anchor.ind == ai:
          break
    return v_list

  # generate difference between the two given meshes   
  def eval(self):
    # find closest points
    self._findClosest() 
    # first, processing of the common triangles
    for v in self.inV:
      if v.original and 0 < v.numCommon() < len(v.around):
        vLst = self._findContour(v)
        self._alignBorder(vLst)
    # next, standalone verteces
    for v in self.inV:
      if v.original and v.opposit and v.numCommon() == 0:
        # add vertex if need
        if not v.equal(v.closest):
          self._newVertexExt(v)
    # remove common and empty triangles  
    self.exT = [tr for tr in self.exT if not tr.common and not tr.isDegenerate()] 
    # remove and change orientation
    self.inT = [tr.changeOrientation() for tr in self.inT if not tr.common and not tr.isDegenerate()]
    # build shape 
    full = self.exT + self.inT
    #full = self.exT
    difference = mesh.Mesh(np.zeros(len(full), dtype=mesh.Mesh.dtype))
    for i,tr in enumerate(full):
      for j in range(3):
        difference.vectors[i][j] = tr.vert[j].v[:] 
    difference.update_normals()
    return difference
    
    
  
