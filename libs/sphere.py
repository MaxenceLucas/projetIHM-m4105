import math
import libs.geometry as _geo

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
        x = gluProject(*self.position,glGetDoublev(GL_MODELVIEW_MATRIX),glGetDoublev(GL_PROJECTION_MATRIX),glGetIntegerv(GL_VIEWPORT))
        self.proj_position = [x[0], x[1]]
        y = [self.radius*camera.up[0],self.radius*camera.up[1],self.radius*camera.up[2]]
        rad = [x[0]+y[0],x[1]+y[1],x[2]+y[2]]
        rad = gluProject(*rad,glGetDoublev(GL_MODELVIEW_MATRIX),glGetDoublev(GL_PROJECTION_MATRIX),glGetIntegerv(GL_VIEWPORT))
        self.proj_radius = math.hypot(rad[0]-x[0],rad[1]-x[1])
        ret = [x[0],glutGet(GLUT_WINDOW_HEIGHT)-x[1]]
        
        return ret , self.proj_radius
