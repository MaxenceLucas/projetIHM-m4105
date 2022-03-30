import sys
import os
import math
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

NBCOTE = 10
RAYON = 0.3
DT = 1
ANIM = True

def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    
    glColor(0,1,0,1)
    glOrtho(-1,1,-1,1,1,-1)
    #annimation


    glPushMatrix()
    glLineWidth(10)
    glColor(0,1,0,1)
    glRotate(18,0,0,1)
    glBegin(GL_LINE_STRIP)
    for i in range(NBCOTE+1):
        glVertex(RAYON*math.sin(math.pi*2*i/NBCOTE),RAYON*math.cos(math.pi*2*i/NBCOTE),0)
    glEnd()
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
    if (key[0]== 97):
        if ANIM:
            ANIM = False
        else:
            ANIM = True

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