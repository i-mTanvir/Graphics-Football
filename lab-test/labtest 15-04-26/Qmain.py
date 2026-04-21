from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Blue quad starts at bottom-left, Red quad starts at top-right
pos1X, pos1Y = (here),   0.0      # Blue — left lane, bottom
pos2X, pos2Y = (here), 450.0      # Red  — right lane, top

speed = 3.0
SIZE = 50                         # Quad size

def draw_quads():
    # Quad 1 — Blue, travels bottom → top
    glColor3f(0.4, 0.7, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(pos1X,        pos1Y)
    glVertex2f(pos1X + SIZE, #   )
    glVertex2f(pos1X + #, pos1Y + SIZE)
    glVertex2f(pos1X,        pos1Y +#  )
    glEnd()

    # Quad 2 — Red, travels top → bottom
    glColor3f(1.0, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(pos2X,        pos2Y)
    glVertex2f(pos2X +#, pos2Y)
    glVertex2f(pos2X + SIZE, pos2Y + SIZE)
    glVertex2f(pos2X,        pos2Y + #)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    draw_quads()
    glutSwapBuffers()

def update(value):
    global pos1X, pos1Y, pos2X, pos2Y

    # Move blue quad upward
    

    # Move red quad downward
    

    # Blue reaches top → wrap back to bottom


    # Red reaches bottom → wrap back to top

    glutPostRedisplay()
    # glutTimerFunc#(, , 0)


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
#glutTimerFunc#(, , 0)

print("Blue quad rises bottom→top | Red quad falls top→bottom | Both loop infinitely")

glutMainLoop()