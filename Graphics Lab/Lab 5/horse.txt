from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

legAngle = 0.0

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # Body
    glColor3f(1.0, 0.9, 0.0)        # Yellow
    glBegin(GL_QUADS)
    glVertex2f(165, 200)             # Bottom-left  (connects to legs)
    glVertex2f(335, 200)             # Bottom-right (connects to legs)
    glVertex2f(335, 300)             # Top-right
    glVertex2f(165, 300)             # Top-left
    glEnd()

    # Left leg
    glPushMatrix()
    glTranslatef(180, 200, 0)
    glRotatef(legAngle, 0, 0, 1)
    glColor3f(0.4, 0.7, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(-15,   0)
    glVertex2f( 15,   0)
    glVertex2f( 15, -100)
    glVertex2f(-15, -100)
    glEnd()
    glPopMatrix()

    # Right leg
    glPushMatrix()
    glTranslatef(320, 200, 0)
    glRotatef(legAngle, 0, 0, 1)
    glColor3f(1.0, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(-15,   0)
    glVertex2f( 15,   0)
    glVertex2f( 15, -100)
    glVertex2f(-15, -100)
    glEnd()
    glPopMatrix()

    glutSwapBuffers()

def keyboard(key, x, y):
    global legAngle
    if key in (b'h', b'H'):
        legAngle = 45.0 if legAngle == 0.0 else 0.0
    glutPostRedisplay()

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 0, 500, -1, 1)
    glMatrixMode(GL_MODELVIEW)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Two Legs")
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()