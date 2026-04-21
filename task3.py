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
    glPointSize(5)
    glBegin(GL_TRIANGLES)

    glVertex2f(250, 450)
    glVertex2f(400, 300)
    glVertex2f(100, 300)

    glEnd()

    glBegin(GL_LINES)
    

    glVertex2f(140, 300)
    glVertex2f(140, 100)


    glVertex2f(360, 300)
    glVertex2f(360, 100)


    glVertex2f(140, 100)
    glVertex2f(360, 100)


#---Door
    glVertex2f(200, 100)
    glVertex2f(300, 100)

    glVertex2f(200, 100)
    glVertex2f(200, 200)

    glVertex2f(300, 100)

    glVertex2f(300, 200)

    glVertex2f(200, 200)
    glVertex2f(300, 200)


    # ---- Window 1 


    glVertex2f(160, 220)
    glVertex2f(220, 220)

    glVertex2f(160, 220)
    glVertex2f(160, 260)

    glVertex2f(220, 220)
    glVertex2f(220, 260)

    glVertex2f(160, 260)
    glVertex2f(220, 260)


    # ---- Window 2

    glVertex2f(280, 220)
    glVertex2f(340, 220)

    glVertex2f(280, 220)
    glVertex2f(280, 260)

    glVertex2f(340, 220)
    glVertex2f(340, 260)

    glVertex2f(280, 260)
    glVertex2f(340, 260)
   

    glEnd()

    glBegin(GL_POINTS)
    
    glVertex2f(285, 150) 
    glEnd()

    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"Drawing Pixels")
glutDisplayFunc(showScreen)

glutMainLoop()