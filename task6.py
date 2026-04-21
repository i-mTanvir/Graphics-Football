from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

X1, Y1, Z1 = -3.0, 0.0, -3.0
X2, Y2, Z2 =  3.0, 6.0,  3.0

angleX, angleY, angleZ = 0.0, 0.0, 0.0
stepAngle = 5.0
Sx, Sy, Sz = 0.1, 0.1, 0.1
scaleX, scaleY, scaleZ = 1.0, 1.0, 1.0

def draw_cube(x1, y1, z1, x2, y2, z2):
    bl=(x1,y1,z1); br=(x2,y1,z1); tr=(x2,y1,z2); tl=(x1,y1,z2)
    top_bl=(x1,y2,z1); top_br=(x2,y2,z1)
    top_tr=(x2,y2,z2); top_tl=(x1,y2,z2)

    # Bottom face — Deep Teal
    glColor3f(0.0, 0.45, 0.45)
    glBegin(GL_QUADS)
    glVertex3f(*bl); glVertex3f(*br); glVertex3f(*tr); glVertex3f(*tl)
    glEnd()

    # Front face — Aqua
    glColor3f(0.2, 0.8, 0.8)
    glBegin(GL_QUADS)
    glVertex3f(*tl); glVertex3f(*tr); glVertex3f(*top_tr); glVertex3f(*top_tl)
    glEnd()

    # Back face — Sea Green
    glColor3f(0.2, 0.7, 0.5)
    glBegin(GL_QUADS)
    glVertex3f(*bl); glVertex3f(*br); glVertex3f(*top_br); glVertex3f(*top_bl)
    glEnd()

    # Left face — Steel Blue
    glColor3f(0.3, 0.55, 0.75)
    glBegin(GL_QUADS)
    glVertex3f(*bl); glVertex3f(*tl); glVertex3f(*top_tl); glVertex3f(*top_bl)
    glEnd()

    # Right face — Mint
    glColor3f(0.5, 0.9, 0.75)
    glBegin(GL_QUADS)
    glVertex3f(*br); glVertex3f(*tr); glVertex3f(*top_tr); glVertex3f(*top_br)
    glEnd()

    # Top face — Pale Cyan
    glColor3f(0.7, 0.95, 0.95)
    glBegin(GL_QUADS)
    glVertex3f(*top_bl); glVertex3f(*top_br); glVertex3f(*top_tr); glVertex3f(*top_tl)
    glEnd()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    gluLookAt(12, 12, 22, 0, 0, 0, 0, 1, 0)
    glRotatef(angleX, 1, 0, 0)
    glRotatef(angleY, 0, 1, 0)
    glRotatef(angleZ, 0, 0, 1)
    glScalef(scaleX, scaleY, scaleZ)
    draw_cube(X1, Y1, Z1, X2, Y2, Z2)
    glutSwapBuffers()

def keyboard(key, x, y):
    global angleX, angleY, angleZ, scaleX, scaleY, scaleZ
    if key == b'X': angleX += stepAngle
    elif key == b'x': angleX -= stepAngle
    elif key == b'Y': angleY += stepAngle
    elif key == b'y': angleY -= stepAngle
    elif key == b'Z': angleZ += stepAngle
    elif key == b'z': angleZ -= stepAngle
    elif key == b'+':
        scaleX += Sx; scaleY += Sy; scaleZ += Sz
    elif key == b'-':
        scaleX = max(0.1, scaleX - Sx)
        scaleY = max(0.1, scaleY - Sy)
        scaleZ = max(0.1, scaleZ - Sz)
    glutPostRedisplay()

def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.03, 0.05, 0.08, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1.0, 1.0, 100)
    glMatrixMode(GL_MODELVIEW)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(500, 500)
glutInitWindowPosition(150, 150)
glutCreateWindow(b'Exp 2 - 3D Cube Blues & Greens')
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
print('X/Y/Z: rotate  |  +/-: scale')
glutMainLoop()