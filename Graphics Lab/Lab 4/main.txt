from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *


# Hardcoded coordinates
X1, Y1, Z1 = -3.0, 0.0, -3.0
X2, Y2, Z2 = 3.0, 6.0, 3.0


# Rotation and Scaling variables
angleX, angleY, angleZ = 0.0, 0.0, 0.0
stepX, stepY, stepZ = 5.0, 5.0, 5.0
Sx, Sy, Sz = 0.1, 0.1, 0.1
scaleX, scaleY, scaleZ = 1.0, 1.0, 1.0


def draw_pyramid_from_points(x1, y1, z1, x2, y2, z2):
    apexX = (x1 + x2) / 2
    apexY = y2
    apexZ = (z1 + z2) / 2


    # Base (Lavender)
    glColor3f(0.7, 0.6, 0.8)
    glBegin(GL_QUADS)
    glVertex3f(x1, y1, z1)
    glVertex3f(x2, y1, z1)
    glVertex3f(x2, y1, z2)
    glVertex3f(x1, y1, z2)
    glEnd()


    glBegin(GL_TRIANGLES)
    # Front face (Peach)
    glColor3f(1.0, 0.7, 0.6)
    glVertex3f(x1, y1, z2)
    glVertex3f(x2, y1, z2)
    glVertex3f(apexX, apexY, apexZ)


    # Back face (Mint)
    glColor3f(0.6, 0.9, 0.7)
    glVertex3f(x1, y1, z1)
    glVertex3f(x2, y1, z1)
    glVertex3f(apexX, apexY, apexZ)


    # Left face (Sky Blue)
    glColor3f(0.6, 0.8, 1.0)
    glVertex3f(x1, y1, z1)
    glVertex3f(x1, y1, z2)
    glVertex3f(apexX, apexY, apexZ)


    # Right face (Light Pink)
    glColor3f(1.0, 0.8, 0.9)
    glVertex3f(x2, y1, z1)
    glVertex3f(x2, y1, z2)
    glVertex3f(apexX, apexY, apexZ)
    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(15, 15, 25, 0, 0, 0, 0, 1, 0)
    glRotatef(angleX, 1, 0, 0)
    glRotatef(angleY, 0, 1, 0)
    glRotatef(angleZ, 0, 0, 1)
    glScalef(scaleX, scaleY, scaleZ)
    draw_pyramid_from_points(X1, Y1, Z1, X2, Y2, Z2)
    glutSwapBuffers()


def keyboard(key, x, y):
    global angleX, angleY, angleZ, scaleX, scaleY, scaleZ


    if key == b'X': angleX += stepX
    elif key == b'x': angleX -= stepX
    elif key == b'Y': angleY += stepY
    elif key == b'y': angleY -= stepY
    elif key == b'Z': angleZ += stepZ
    elif key == b'z': angleZ -= stepZ
    elif key == b'+':
        scaleX += Sx
        scaleY += Sy
        scaleZ += Sz
    elif key == b'-':
        scaleX = max(0.1, scaleX - Sx)
        scaleY = max(0.1, scaleY - Sy)
        scaleZ = max(0.1, scaleZ - Sz)


    glutPostRedisplay()


def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 1.0, 100)
    glMatrixMode(GL_MODELVIEW)




glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"3D Pyramid ")


init()


glutDisplayFunc(display)
glutKeyboardFunc(keyboard)


print("Controls: X/Y/Z to rotate, +/- to scale. Translation disabled.")


glutMainLoop()

