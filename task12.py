from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W, H = 500, 500
DROP_W = 3
DROP_H = 16
WIND = 4
SPEED = 8

raindrops = []


def make_drops():
    for _ in range(120):
        raindrops.append([random.randint(-50, W), random.randint(0, H + 200)])


def draw_drop(x, y):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + DROP_W, y)
    glVertex2f(x + DROP_W + WIND, y - DROP_H)
    glVertex2f(x + WIND, y - DROP_H)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glColor3f(0.5, 0.8, 1.0)
    for x, y in raindrops:
        draw_drop(x, y)

    glutSwapBuffers()


def update(value):
    for drop in raindrops:
        drop[0] += WIND
        drop[1] -= SPEED

        if drop[1] < -20 or drop[0] > W + 20:
            drop[0] = random.randint(-80, W)
            drop[1] = random.randint(H, H + 150)

    glutPostRedisplay()
    glutTimerFunc(30, update, 0)


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W, 0, H, -1, 1)
    glMatrixMode(GL_MODELVIEW)


make_drops()
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(W, H)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Virtual Rain")

init()
glutDisplayFunc(display)
glutTimerFunc(30, update, 0)
glutMainLoop()
