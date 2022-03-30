import sys
import os
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

NBCOTE = 10
RAYON = 0.4
DT = 1
rayon = 0.2

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    #glOrtho(-1,1,-1,1,1,-1)
    glPushMatrix()
    glColor(0,1,0,1)
    global rayon
    for i in range(11):
        glPushMatrix()
        glTranslate(RAYON*math.sin(math.pi*2*i/NBCOTE), RAYON*math.cos(math.pi*2*i/NBCOTE), 0)
        glutSolidSphere(rayon, 50, 10)
        glPopMatrix()
    
        
    glPopMatrix()
    glutSwapBuffers()

def idle():
    global DT
    glutPostRedisplay()
    #print(DT)
    if ANIM:
        DT+=1
    


def processNormalKeys(key,x,y):
    print(key)
    global ANIM
    if (key[0] == 113):
        os._exit(os.EX_OK)

glutInit(sys.argv)
glutInitWindowSize(800,600)
glutInitDisplayMode(GLUT_RGBA|GLUT_DOUBLE|GLUT_DEPTH)
w=glutCreateWindow(b'my first glut window')
glEnable(GL_DEPTH_TEST)
glClearColor(0.5,0.5,0.5,1)     
glutKeyboardFunc(processNormalKeys)
glutDisplayFunc(display)
glutIdleFunc(idle)
glutMainLoop()