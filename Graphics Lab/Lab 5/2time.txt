from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

posX, posY = 0.0, 0.0
step = 10.0

def draw_quads():
    # Blue quad
    glColor3f(0.4, 0.7, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(100,  100)
    glVertex2f(200,  100)
    glVertex2f(200,  200)
    glVertex2f(100,  200)
    glEnd()

    # Red quad
    glColor3f(1.0, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(250,  100)
    glVertex2f(350,  100)
    glVertex2f(350,  200)
    glVertex2f(250,  200)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(posX, posY, 0)         # Apply translation FIRST
    # glRotatef(angleZ, 0, 0, 1)          # Then rotation

    draw_quads()
    glutSwapBuffers()

def keyboard(key, x, y):
    global angleZ, posX, posY           # Declare globals to modify them

    if key == b'w': posY += step
    if key == b's': posY -= step
    if key == b'a': posX -= step
    if key == b'd': posX += step


    posX = posX % 500
    posY = posY % 500


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
glutCreateWindow(b"Example 1 - Move & Rotate 2D Quad")

init()

glutDisplayFunc(display)
glutKeyboardFunc(keyboard)

print("WASD to move | Z/z to rotate CW/CCW")

glutMainLoop()