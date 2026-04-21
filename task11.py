from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# position of 2 quads
x1, y1 = -180, -180   # bottom-left quad
x2, y2 = 180, 180     # top-right quad

# movement speed
dx1, dy1 = 2, 2
dx2, dy2 = -2, -2

# rotation angle
angle = 0

# quad size
size = 30


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # black background
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-200, 200, -200, 200)


def draw_quad(x, y, r, g, b, ang):
    glPushMatrix()

    # move quad to position
    glTranslatef(x, y, 0)

    # rotate clockwise
    glRotatef(ang, 0, 0, 1)

    # draw quad
    glColor3f(r, g, b)
    glBegin(GL_QUADS)
    glVertex2f(-size/2, -size/2)
    glVertex2f(size/2, -size/2)
    glVertex2f(size/2, size/2)
    glVertex2f(-size/2, size/2)
    glEnd()

    glPopMatrix()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # quad 1: blue
    draw_quad(x1, y1, 0.3, 0.7, 1.0, angle)

    # quad 2: red
    draw_quad(x2, y2, 1.0, 0.3, 0.3, angle)

    glFlush()


def update(value):
    global x1, y1, x2, y2, dx1, dy1, dx2, dy2, angle

    # move quads diagonally
    x1 += dx1
    y1 += dy1

    x2 += dx2
    y2 += dy2

    # when quad1 reaches top-right corner, reverse to bottom-left
    if x1 >= 180 and y1 >= 180:
        dx1 = -2
        dy1 = -2

    # when quad1 reaches bottom-left corner, reverse again
    if x1 <= -180 and y1 <= -180:
        dx1 = 2
        dy1 = 2

    # when quad2 reaches bottom-left corner, reverse to top-right
    if x2 <= -180 and y2 <= -180:
        dx2 = 2
        dy2 = 2

    # when quad2 reaches top-right corner, reverse again
    if x2 >= 180 and y2 >= 180:
        dx2 = -2
        dy2 = -2

    # bonus: clockwise rotation all time
    angle -= 3
    if angle < -360:
        angle += 360

    glutPostRedisplay()
    glutTimerFunc(20, update, 0)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(600, 600)
    glutInitWindowPosition(200, 100)
    glutCreateWindow(b"Problem 2 - Two Moving Quads")

    init()
    glutDisplayFunc(display)
    glutTimerFunc(20, update, 0)

    glutMainLoop()


main()
