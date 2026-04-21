from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

# ─────────────────────────────────────
#  GLOBALS
# ─────────────────────────────────────

posX = 250.0
posY = 250.0
step = 10.0

score     = 0
game_over = False

# ─────────────────────────────────────
#  DOTS  — each dot: [x, y, active]
# ─────────────────────────────────────

dots = []

def make_dots():
    dots.clear()
    for i in range(15):
        x = random.randint(20, 480)
        y = random.randint(20, 480)
        dots.append([x, y, True])

# ─────────────────────────────────────
#  DRAW HELPERS
# ─────────────────────────────────────

def draw_dot(cx, cy):
    glPointSize(12)
    glBegin(GL_POINTS)
    glVertex2f(cx, cy)
    glEnd()

def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))

# ─────────────────────────────────────
#  COLLISION
# ─────────────────────────────────────

def is_touching(ax, ay, bx, by):
    dx = ax - bx
    dy = ay - by
    return math.sqrt(dx*dx + dy*dy) < 20

# ─────────────────────────────────────
#  DISPLAY
# ─────────────────────────────────────

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    if not game_over:

        # -- draw dots --
        glColor3f(1.0, 1.0, 0.0)
        for dot in dots:
            if dot[2]:
                draw_dot(dot[0], dot[1])

        # -- draw player as a GL_QUAD --
        glPushMatrix()
        glTranslatef(posX, posY, 0)

        glColor3f(0.3, 0.6, 1.0)
        glBegin(GL_QUADS)
        glVertex2f(-15, -15)
        glVertex2f( 15, -15)
        glVertex2f( 15,  15)
        glVertex2f(-15,  15)
        glEnd()

        glPopMatrix()

        # -- score text --
        glColor3f(1.0, 1.0, 1.0)
        draw_text(10, 475, "Score: " + str(score))

    else:
        glColor3f(0.2, 0.9, 0.4)
        draw_text(150, 280, "YOU WIN!  Score: " + str(score))
        glColor3f(1.0, 1.0, 1.0)
        draw_text(130, 250, "Press R to restart  |  ESC to quit")

    glutSwapBuffers()

# ─────────────────────────────────────
#  KEYBOARD
# ─────────────────────────────────────

def keyboard(key, x, y):
    global posX, posY, score, game_over

    if not game_over:
        if key == b'w': posY += step
        if key == b's': posY -= step
        if key == b'a': posX -= step
        if key == b'd': posX += step

        # clamp inside window
        if posX < 15:  posX = 15
        if posX > 485: posX = 485
        if posY < 15:  posY = 15
        if posY > 485: posY = 485

        # check collision with each dot
        for dot in dots:
            if dot[2] and is_touching(posX, posY, dot[0], dot[1]):
                dot[2] = False
                score += 1

        if score >= 10:
            game_over = True

    if key == b'r' or key == b'R':
        posX      = 250.0
        posY      = 250.0
        score     = 0
        game_over = False
        make_dots()

    if key == b'\x1b':
        glutLeaveMainLoop()

    glutPostRedisplay()

# ─────────────────────────────────────
#  INIT
# ─────────────────────────────────────

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 0, 500, -1, 1)
    glMatrixMode(GL_MODELVIEW)

# ─────────────────────────────────────
#  MAIN
# ─────────────────────────────────────

make_dots()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Dot Collector - reach 10 points!")

init()

glutDisplayFunc(display)
glutKeyboardFunc(keyboard)

print("WASD to move | R to restart | ESC to quit")

glutMainLoop()