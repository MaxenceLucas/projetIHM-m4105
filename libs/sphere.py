import math

from sympy import npartitions
import libs.geometry as _geo
import numpy as np

try:
    from OpenGL.GL      import *
    from OpenGL.GLU     import *
    from OpenGL.GLUT    import *
except:
    print ('''ERROR: PyOpenGL not installed properly.''')

class sphere:
    def __init__(self, p, r):
        self.position   = p
        self.radius     = r
    
    #This function computes and returns the projection of a sphere position on the screen, AND the projected radius (use Thales)
    #Be careful !!! This function takes the current camera stack !!!
    def project(self, camera):
        #TODO_TODO_TODO
        x = gluProject(self.position[0],self.position[1],self.position[2],glGetDoublev(GL_MODELVIEW_MATRIX),glGetDoublev(GL_PROJECTION_MATRIX),glGetIntegerv(GL_VIEWPORT))

        rad = np.add(self.position, np.dot(self.radius, camera.up))

        rad = gluProject(rad[0],rad[1],rad[2],glGetDoublev(GL_MODELVIEW_MATRIX),glGetDoublev(GL_PROJECTION_MATRIX),glGetIntegerv(GL_VIEWPORT))
        
        self.proj_radius = math.hypot(rad[0]-x[0],rad[1]-x[1])
        
        size = glutGet(GLUT_WINDOW_HEIGHT)
        return [x[0], size-x[1]] , self.proj_radius
