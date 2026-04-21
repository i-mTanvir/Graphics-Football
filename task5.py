from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Scale state
scaleX, scaleY = 1.0, 1.0
step = 0.5

def draw_triangle():
    glColor3f(0.0, 0.6, 0.6)   # Teal
    glBegin(GL_TRIANGLES)
    glVertex2f(250, 400)        # apex
    glVertex2f(80, 120)
    glVertex2f(420, 120)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glScalef(scaleX, scaleY, 1.0)
    draw_triangle()
    glutSwapBuffers()

def keyboard(key, x, y):
    global scaleX, scaleY
    if key == b'+':
        scaleX += step
        scaleY += step
    if key == b'-':
        scaleX = max(0.1, scaleX - step)
        scaleY = max(0.1, scaleY - step)
    glutPostRedisplay()

def init():
    glClearColor(0.05, 0.05, 0.1, 1.0)
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b'Exp 1 - 2D Triangle Scale')
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
print('Press + to scale up, - to scale down')
glutMainLoop()