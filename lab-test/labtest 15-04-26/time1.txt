from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

posX = 250.0   # Centered horizontally
posY = 250.0   # Starts at top of screen
speedY = -3.0  # Falls downward (negative Y)

def draw_quad():
    glColor3f(0.4, 0.7, 1.0)
    glBegin(GL_QUADS)
    glVertex2f(  0,   0)
    glVertex2f( 50,   0)
    glVertex2f( 50,  50)
    glVertex2f(  0,  50)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glTranslatef(posX, posY, 0)
    draw_quad()

    glutSwapBuffers()

def update(value):
    global posY, speedY

    posY += speedY               # Move quad down each fram
    if posY <= 0:                   # Hit the floor — bounce back up
        speedY = abs(speedY)
        # posY = posY % 500

    if posY >=400:                 # Hit the ceiling — fall back down
        speedY = -abs(speedY)
        # posY = posY % 500

    glutPostRedisplay()
    glutTimerFunc(30, update, 0)    # Call update again in 16ms (~60fps)

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
glutCreateWindow(b"Example 6 - Falling Quad")

init()
glutDisplayFunc(display)
glutTimerFunc(16, update, 0)        # Kick off the first timer call

print("Quad falls and bounces automatically")
glutMainLoop()