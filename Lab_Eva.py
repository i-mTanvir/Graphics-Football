from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Blue quad starts at bottom-left, Red quad starts at top-right
pos1X, pos1Y = 120.0, 0.0
pos2X, pos2Y = 320.0, 450.0

speed = 3.0
SIZE = 50


def draw_quads():
    # Blue quad moves upward.
    glColor3f(0.4, 0.7, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(pos1X, pos1Y)
    glVertex2f(pos1X + SIZE, pos1Y)
    glVertex2f(pos1X + SIZE, pos1Y + SIZE)
    glVertex2f(pos1X, pos1Y + SIZE)
    glEnd()

    # Red quad moves downward.
    glColor3f(1.0, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(pos2X, pos2Y)
    glVertex2f(pos2X + SIZE, pos2Y)
    glVertex2f(pos2X + SIZE, pos2Y + SIZE)
    glVertex2f(pos2X, pos2Y + SIZE)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    draw_quads()
    glutSwapBuffers()


def update(value):
    global pos1Y, pos2Y

    pos1Y += speed
    pos2Y -= speed

    if pos1Y > 500:
        pos1Y = -SIZE

    if pos2Y + SIZE < 0:
        pos2Y = 500

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


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
glutCreateWindow(b"Infinite Vertical Quads")

init()

glutDisplayFunc(display)
glutTimerFunc(16, update, 0)

print("Blue quad rises bottom-to-top | Red quad falls top-to-bottom | Both loop infinitely")

glutMainLoop()
