from OpenGL.GL import *
from OpenGL.GLUT import *
import random

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()

    glColor3f(1.0, 1.0, 1.0) 
    glPointSize(5)
    glBegin(GL_POINTS)

    for _ in range(50):
        x = random.randint(0, 500)
        y = random.randint(0, 500)
        glVertex2f(x, y)

    glEnd()
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Random Pixels")
glutDisplayFunc(showScreen)
glutMainLoop()