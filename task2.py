from OpenGL.GL import *
from OpenGL.GLUT import *


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
    glColor3f(1.0, 0.0, 1.0)  

    glLineWidth(5)
    glBegin(GL_LINES)

    #T
    glVertex2f(150, 300)
    glVertex2f(250, 300)

    glVertex2f(200, 300)
    glVertex2f(200, 200)

    #M
    glVertex2f(300, 200)
    glVertex2f(300, 300)

    glVertex2f(300, 300)
    glVertex2f(350, 240)

    glVertex2f(350, 240)
    glVertex2f(400, 300)

    glVertex2f(400, 300)
    glVertex2f(400, 200)

    #1
    glVertex2f(200, 150)
    glVertex2f(200, 100)

    #3

    glVertex2f(250, 150)
    glVertex2f(290, 150)

    glVertex2f(250, 125)
    glVertex2f(290, 125)

    glVertex2f(250, 100)
    glVertex2f(290, 100)

    glVertex2f(290, 150)
    glVertex2f(290, 100)

    #9
    glVertex2f(320, 150)
    glVertex2f(360, 150)

    glVertex2f(320, 150)
    glVertex2f(320, 125)

    glVertex2f(360, 150)
    glVertex2f(360, 100)

    glVertex2f(320, 125)
    glVertex2f(360, 125)

    #8
    glVertex2f(390, 150)
    glVertex2f(430, 150)

    glVertex2f(390, 125)
    glVertex2f(430, 125)

    glVertex2f(390, 100)
    glVertex2f(430, 100)

    glVertex2f(390, 150)
    glVertex2f(390, 100)

    glVertex2f(430, 150)
    glVertex2f(430, 100)

    glEnd()

    glutSwapBuffers()


    

    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Drawing Pixels")
glutDisplayFunc(showScreen)

glutMainLoop()