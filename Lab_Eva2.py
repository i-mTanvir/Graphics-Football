from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

posX = 0.0
angleZ = 0.0
step = 10.0


def draw_G():
    glColor3f(0.4, 0.9, 1.0)
    glLineWidth(3.0)
    glBegin(GL_LINES)

    # Top horizontal bar
    glVertex2f(270, 350)
    glVertex2f(200, 350)

    # Left top curve to spine
    glVertex2f(200, 350)
    glVertex2f(175, 325)

    # Vertical spine
    glVertex2f(175, 325)
    glVertex2f(175, 175)

    # Left bottom curve
    glVertex2f(175, 175)
    glVertex2f(200, 150)

    # Bottom horizontal bar
    glVertex2f(200, 150)
    glVertex2f(270, 150)

    # Right bottom curve
    glVertex2f(270, 150)
    glVertex2f(300, 175)

    # Right vertical (lower half only)
    glVertex2f(300, 175)
    glVertex2f(300, 250)

    # Middle horizontal spur
    glVertex2f(300, 250)
    glVertex2f(240, 250)

    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(250 + posX, 250, 0)
    glRotatef(angleZ, 0, 0, 1)
    glTranslatef(-250, -250, 0)

    draw_G()
    glutSwapBuffers()


def keyboard(key, x, y):
    global posX, angleZ

    if key == b'a':
        posX -= step
        angleZ += 30.0

    if key == b'd':
        posX += step
        angleZ -= 30.0

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
glutCreateWindow(b"Letter G - GL_LINES Move & Rotate")

init()

glutDisplayFunc(display)
glutKeyboardFunc(keyboard)

print("A = move left + rotate | D = move right + rotate | Like a rolling tire")

glutMainLoop()
