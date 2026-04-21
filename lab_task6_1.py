from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import cos, sin, pi
import random

W, H = 500, 500

pac_x, pac_y = 250, 250
pac_r = 20
step = 12
score = 0
game_over = False

foods = []


def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))


def draw_filled_circle(x, y, radius, sides=100):
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(x, y)
    for i in range(sides + 1):
        theta = 2.0 * pi * i / sides
        glVertex2f(x + radius * cos(theta), y + radius * sin(theta))
    glEnd()


def create_food():
    x = random.randint(20, W - 20)
    y = random.randint(20, H - 20)
    kind = random.choice(["good", "bad"])
    return [x, y, kind]


def reset_foods():
    foods.clear()
    for _ in range(12):
        foods.append(create_food())


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glPointSize(8)
    glBegin(GL_POINTS)
    for x, y, kind in foods:
        if kind == "good":
            glColor3f(0.0, 1.0, 0.0)
        else:
            glColor3f(1.0, 0.0, 0.0)
        glVertex2f(x, y)
    glEnd()

    glColor3f(1.0, 1.0, 0.0)
    draw_filled_circle(pac_x, pac_y, pac_r)

    glColor3f(1.0, 1.0, 1.0)
    draw_text(10, 475, f"Score: {score}")
    draw_text(10, 450, "WASD to move")

    if game_over:
        glColor3f(1.0, 1.0, 0.0)
        draw_text(180, 250, "GAME OVER")
        draw_text(165, 225, "You reached 100")
        draw_text(160, 200, "Press R to restart")

    glutSwapBuffers()


def check_collision():
    global score, game_over

    for food in foods:
        dx = pac_x - food[0]
        dy = pac_y - food[1]
        if dx * dx + dy * dy <= (pac_r + 6) * (pac_r + 6):
            if food[2] == "good":
                score += 10
            else:
                score -= 10
            food[:] = create_food()

    if score >= 100:
        game_over = True


def keyboard(key, x, y):
    global pac_x, pac_y, score, game_over

    if key in (b'r', b'R'):
        pac_x, pac_y = 250, 250
        score = 0
        game_over = False
        reset_foods()
    elif not game_over:
        if key in (b'w', b'W'):
            pac_y = min(H - pac_r, pac_y + step)
        elif key in (b's', b'S'):
            pac_y = max(pac_r, pac_y - step)
        elif key in (b'a', b'A'):
            pac_x = max(pac_r, pac_x - step)
        elif key in (b'd', b'D'):
            pac_x = min(W - pac_r, pac_x + step)
        check_collision()

    glutPostRedisplay()


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glViewport(0, 0, W, H)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, W, 0, H, -1, 1)
    glMatrixMode(GL_MODELVIEW)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(W, H)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Pacman Points Game")

init()
reset_foods()

glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMainLoop()
