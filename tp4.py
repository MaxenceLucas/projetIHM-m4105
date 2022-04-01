#!/usr/bin/env python3

import sys
import time
import math
import random

from sympy import true

import libs.camera      as _cam
import libs.sphere      as _sph
import libs.geometry    as _geo

try:
    from OpenGL.GL      import *
    from OpenGL.GLU     import *
    from OpenGL.GLUT    import *
except:
    print ('''ERROR: PyOpenGL not installed properly.''')

################################################################################
# GLOBAL VARS

camera          = _cam.camera([0, 0, 1], [0, 0, 0])#main camera
starting_time   = time.time()                       #starting time of course
mouse           = [0, 0]                            #mouse current position
animation       = False                             #(des)activating animation (juste for fun)
spheres         = []                                #list of the spheres to select

#  VARS GLOBAL PROJET
NB_CLICK = 0
CLICKS = []
RADIUS_CIRCLE = 0.5
RADIUS_SPHERE = 0.1
IND_POINTING_SPHERE = 0
IND_CURRENT_POINTING_SPHERE = 0
SPHERE_CLICKED = True
SEQUENCE_IND = [2, 6, 0, 4, 8, 3, 9, 5, 1, 7]
SEQUENCE_CURRENT_IND = 0
################################################################################
# SETUPS

def stopApplication():
    os._exit(os.EX_OK)


def setupScene():
    '''OpenGL and Scene objects settings
    '''
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (0., 100., 100., 1.))    
    glLightfv(GL_LIGHT0, GL_AMBIENT,(.1, .1, .1, 1.))
    glLightfv(GL_LIGHT0, GL_DIFFUSE,(.7, .7, .7, 1.))
    
    glEnable(GL_CULL_FACE)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_NORMALIZE)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT,GL_AMBIENT_AND_DIFFUSE)
    glEnable(GL_DEPTH_TEST)
    glClearColor(.4, .4, .4, 1)
    
    global spheres
    spheres = create_spheres()


################################################################################
# COMPUTATIONS

def create_spheres():
    '''Create the spheres to select: 3d position and radius
    '''
    #TODO_TODO_TODO
    s = []  
    for i in range(10):
        posSphere = [RADIUS_CIRCLE*math.sin(math.pi*2*i/10), RADIUS_CIRCLE*math.cos(math.pi*2*i/10), 0]
        s.append(_sph.sphere(posSphere, RADIUS_SPHERE))

    return s


def closest_sphere(sphs, cam, m):
    '''Returns the index of the sphere (in list 'sphs') whose projection is the closest to the 2D position 'm'
    '''
    #TODO_TODO_TODO
    min = float("inf")
    i=0
    save = 0
    for sphere in sphs:
        sph = sphere.project(cam)
        val = math.hypot(sph[0][0]-mouse[0],sph[0][1]-mouse[1])
        if val < min :
            save = i
            min = val
        i+=1
    return save


################################################################################
# DISPLAY FUNCS

def display_frame():
    '''Display an orthonormal frame + a wire cube
    '''
    #TODO_TODO_TODO
    glColor(1,1,1,1)
    glutWireCube(10)
    
    glBegin(GL_LINES)
    glColor(1, 0, 0, 1)
    glVertex(0, 0, 0)
    glVertex(100, 0 ,0)
    glEnd()
    pass


def display_scene(sphs):
    '''display of the whole scene, mainly the spheres (in white)
    '''
    #TODO_TODO_TODO
    #TODO_TODO_TODO
    #TODO_TODO_TODO
    i = 0
    for sphere in sphs:
        if IND_POINTING_SPHERE == i:
            glColor(0, 1, 0, 1)
        else:
            glColor(0.5, 0.5, 0.5, 1)
            
        glPushMatrix()
        glTranslate(*sphere.position)
        glutSolidSphere(sphere.radius,10,10)
        glPopMatrix()
        i += 1
    
    


def display_2d_disc(p2d, r, c):
    '''Display a disc on a 2d position of the screen
    '''
    w, h = glutGet(GLUT_WINDOW_WIDTH), glutGet(GLUT_WINDOW_HEIGHT)
    glDisable(GL_LIGHTING)
    glPushMatrix()
    reshape_ortho(w, h)
    glLoadIdentity()
    glTranslate(p2d[0], p2d[1], -1)
    glColor(*c)
    glScale(1, 1, 0.000001)
    glutSolidSphere(r, 20, 20)
    glEnable(GL_LIGHTING)
    reshape_persp(w, h)
    glPopMatrix()


def display_bubble(sphere, pos_2d, color):
    '''display the bubble, i.e display a 2d transparent disc that encompasses the mouse and
        the 2d projection of the sphere
    '''
    #TODO_TODO_TODO
    global camera
    sph=sphere.project(camera)
    #droite = [pos_2d[0]+sph[0][0],pos_2d[0]+sph[0][1]]
    centre = [(pos_2d[0]+sph[0][0])/2,(pos_2d[1]+sph[0][1])/2]
    r = math.hypot(centre[0]-pos_2d[0],centre[1]-pos_2d[1])
    display_2d_disc(centre,r,color)

    


def display():
    '''Global Display function
    '''
    
    glClear (GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity ()             # clear the matrix 
    
    ###############
    #Point of View
    gluLookAt ( camera.position[0], camera.position[1], camera.position[2], 
                camera.viewpoint[0], camera.viewpoint[1], camera.viewpoint[2], 
                camera.up[0], camera.up[1], camera.up[2])
    
    ###############
    #Frame
    display_frame()
    display_scene(spheres)
    global IND_CURRENT_POINTING_SPHERE
    IND_CURRENT_POINTING_SPHERE = closest_sphere(spheres, camera, mouse)
    display_bubble(spheres[IND_CURRENT_POINTING_SPHERE], mouse, [0, 2, 0, .2])
    #interactions()
    #print(SPHERE_CLICKED)
    glutSwapBuffers()


def reshape_ortho (w, h):
    '''Orthogonal matrix for the projection
        Also called by windows rescaling events
    '''
    glViewport (0, 0, w, h)
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity ()
    glOrtho(0, 800, 600, 0, camera.near, camera.far)
    glMatrixMode (GL_MODELVIEW)


def reshape_persp (w, h):
    '''Perspective matrix for the projection
        Called by windows rescaling events
    '''
    glViewport (0, 0, w, h)
    glMatrixMode (GL_PROJECTION)
    glLoadIdentity ()
    gluPerspective(60.0,float(w)/float(h),camera.near,camera.far)
    glMatrixMode (GL_MODELVIEW)


def idle():
    '''Called when opengl has nothing else to do ...
    '''
    if animation:
        t = time.time()
        dt = t - starting_time
        x = 10*math.cos(dt*math.pi/2.)
        z = 10*math.sin(dt*math.pi/2.)
        camera.position[0] = x
        camera.position[2] = z
    glutPostRedisplay() 
 
 
################################################################################
## INTERACTION FUNCS

def keyboard(key, x, y):
    '''Called when a keyboard ascii key is pressed
    '''
    if key == b'\x1b':
        stopApplication()
    elif key == b'a':
        global animation
        animation = not animation
    else:
        print ("key", key)


def mouse_clicks(button, state, x, y):
    '''Called when a mouse's button is pressed or released
    button is in [GLUT_LEFT_BUTTON, GLUT_MIDDLE_BUTTON, GLUT_RIGHT_BUTTON],
    state is in [GLUT_DOWN, GLUT_UP]
    '''
    global mouse
    global NB_CLICK
    NB_CLICK += 1
    mouse = [x, y]
    interactionsNearest()
    glutPostRedisplay()


def mouse_active(x, y):
    '''Called when mouse moves while on of its button is pressed
    '''
    global mouse
    mouse = [x, y]
    glutPostRedisplay()


def mouse_passive(x, y):
    '''Called when mouse hovers over the window
    '''
    global mouse
    mouse =[x, y]
    glutPostRedisplay()

###############################################################################
# PROJET AJOUT 
def randomizePointedSphere():
    global IND_POINTING_SPHERE
    global SPHERE_CLICKED
    global SEQUENCE_CURRENT_IND
    global SEQUENCE_IND
    global NB_CLICK

    if SPHERE_CLICKED == True and NB_CLICK%2==0:
        
        IND_POINTING_SPHERE = SEQUENCE_IND[SEQUENCE_CURRENT_IND]
        SPHERE_CLICKED = False
        SEQUENCE_CURRENT_IND += 1
        if SEQUENCE_CURRENT_IND > 9:
            SEQUENCE_CURRENT_IND = 0
        
        
    
def interactionsNearest():
    global SPHERE_CLICKED
    global IND_POINTING_SPHERE
    if IND_CURRENT_POINTING_SPHERE == IND_POINTING_SPHERE:
        CLICKS.append(True)
    else:
        CLICKS.append(False)
    SPHERE_CLICKED = True
    #print(IND_CURRENT_POINTING_SPHERE, IND_POINTING_SPHERE)
    randomizePointedSphere()

def interactionsOnSphere():
    global SPHERE_CLICKED
    global IND_POINTING_SPHERE
    global mouse
    if clickOnSphere(mouse,IND_POINTING_SPHERE):
        CLICKS.append(True)
    else:
        CLICKS.append(False)
    SPHERE_CLICKED = True
    randomizePointedSphere()

def clickOnSphere(mouse,indexSphere):
    global spheres
    global camera
    sph = spheres[indexSphere].project(camera) 
    hyp = math.hypot(sph.pos[0][0]-mouse[0], sph.pos[0][0]-mouse[1])
    if (hyp < sph[1]):
        return True
    else:
        return False

    
    
################################################################################
# MAIN

print("Commands:")
print("\ta:\tanimation")
print("\tesc:\texit")

glutInit(sys.argv)
glutInitDisplayString(b'double rgba depth')
glutInitWindowSize (800, 600)
glutInitWindowPosition (0, 0)
glutCreateWindow(b'Bubble')

setupScene()

######

#####

glutDisplayFunc(display)
glutReshapeFunc(reshape_persp)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse_clicks)
glutMotionFunc(mouse_active)
glutPassiveMotionFunc(mouse_passive)
glutIdleFunc(idle)
glutMainLoop()
