from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
from OpenGL.GLU import *
from importlib import import_module
import random

# Window size
window_width = 800
window_height = 600

# Bird
bird_x = 130.0
bird_y = 300.0
bird_width = 72.0
bird_height = 56.0
bird_velocity_y = 0.0
bird_texture = None

# Game values
gravity = -0.48
jump_force = 8.4
pipe_speed = 2.2
pipe_width = 95.0
pipe_gap = 220.0
pipe_distance = 280.0
score = 0
game_over = False
pipes = []


def load_texture(filename):
    try:
        Image = import_module("PIL.Image")
    except ModuleNotFoundError as exc:
        raise RuntimeError("Install Pillow first: pip install pillow") from exc

    image = Image.open(filename).convert("RGBA")
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    image_data = image.tobytes()

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA,
        image.width, image.height,
        0, GL_RGBA, GL_UNSIGNED_BYTE, image_data
    )
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    return texture_id


def draw_rectangle(x, y, width, height):
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()


def draw_text(x, y, message):
    glRasterPos2f(x, y)
    for ch in message:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))


def draw_bird():
    angle = bird_velocity_y * 3.5
    angle = max(-35.0, min(25.0, angle))

    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, bird_texture)

    glPushMatrix()
    glTranslatef(bird_x + bird_width / 2, bird_y + bird_height / 2, 0)
    glRotatef(angle, 0, 0, 1)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(-bird_width / 2, -bird_height / 2)
    glTexCoord2f(1, 0); glVertex2f( bird_width / 2, -bird_height / 2)
    glTexCoord2f(1, 1); glVertex2f( bird_width / 2,  bird_height / 2)
    glTexCoord2f(0, 1); glVertex2f(-bird_width / 2,  bird_height / 2)
    glEnd()

    glPopMatrix()
    glDisable(GL_TEXTURE_2D)


def create_pipe(start_x):
    gap_center_y = random.randint(150, window_height - 150)
    return {
        "x": float(start_x),
        "gap_center_y": float(gap_center_y),
        "counted": False
    }


def reset_game():
    global bird_y, bird_velocity_y, score, game_over, pipes

    bird_y = 300.0
    bird_velocity_y = 0.0
    score = 0
    game_over = False

    pipes = []
    for i in range(3):
        pipes.append(create_pipe(window_width + i * pipe_distance))


def check_collision(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2):
    return ax1 < bx2 and ax2 > bx1 and ay1 < by2 and ay2 > by1


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Sky
    glColor3f(0.53, 0.82, 0.98)
    draw_rectangle(0, 0, window_width, window_height)

    # Pipes
    glColor3f(0.16, 0.68, 0.22)
    for pipe in pipes:
        bottom_height = pipe["gap_center_y"] - pipe_gap / 2
        top_y = pipe["gap_center_y"] + pipe_gap / 2
        top_height = window_height - top_y

        draw_rectangle(pipe["x"], 0, pipe_width, bottom_height)
        draw_rectangle(pipe["x"], top_y, pipe_width, top_height)

    # Bird
    glColor3f(1.0, 1.0, 1.0)
    draw_bird()

    # Score text
    draw_text(20, window_height - 35, f"Score: {score}")
    draw_text(20, window_height - 60, "Press SPACE or W to jump")

    # Game over text
    if game_over:
        glColor4f(0.0, 0.0, 0.0, 0.45)
        draw_rectangle(0, 0, window_width, window_height)

        glColor3f(1.0, 0.95, 0.2)
        draw_text(window_width / 2 - 70, window_height / 2 + 25, "GAME OVER")

        glColor3f(1.0, 1.0, 1.0)
        draw_text(window_width / 2 - 90, window_height / 2 - 5, f"Final Score: {score}")
        draw_text(window_width / 2 - 115, window_height / 2 - 35, "Press R to restart")

    glutSwapBuffers()


def update(value):
    global bird_y, bird_velocity_y, score, game_over

    if not game_over:
        bird_velocity_y += gravity
        bird_y += bird_velocity_y

        bird_left = bird_x + 10
        bird_bottom = bird_y + 8
        bird_right = bird_x + bird_width - 10
        bird_top = bird_y + bird_height - 8

        if bird_bottom <= 0 or bird_top >= window_height:
            game_over = True

        for pipe in pipes:
            pipe["x"] -= pipe_speed

            if pipe["x"] + pipe_width < bird_x and pipe["counted"] is False:
                pipe["counted"] = True
                score += 1

            if pipe["x"] + pipe_width < 0:
                farthest_x = max(item["x"] for item in pipes)
                pipe["x"] = farthest_x + pipe_distance
                pipe["gap_center_y"] = float(random.randint(150, window_height - 150))
                pipe["counted"] = False

            bottom_height = pipe["gap_center_y"] - pipe_gap / 2
            top_y = pipe["gap_center_y"] + pipe_gap / 2

            hit_bottom_pipe = check_collision(
                bird_left, bird_bottom, bird_right, bird_top,
                pipe["x"], 0, pipe["x"] + pipe_width, bottom_height
            )

            hit_top_pipe = check_collision(
                bird_left, bird_bottom, bird_right, bird_top,
                pipe["x"], top_y, pipe["x"] + pipe_width, window_height
            )

            if hit_bottom_pipe or hit_top_pipe:
                game_over = True

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)


def keyboard(key, x, y):
    global bird_velocity_y

    if key in (b' ', b'w', b'W'):
        if not game_over:
            bird_velocity_y = jump_force

    elif key in (b'r', b'R'):
        reset_game()

    elif key == b'\x1b':
        glutLeaveMainLoop()

    glutPostRedisplay()


def init():
    glClearColor(0.48, 0.78, 0.96, 1.0)
    glViewport(0, 0, window_width, window_height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, window_width, 0, window_height, -1, 1)

    glMatrixMode(GL_MODELVIEW)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(100, 60)
glutCreateWindow(b"Lab Task 6 - Basic Flappy Bird")

init()
bird_texture = load_texture("bird.png")
reset_game()

glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutTimerFunc(16, update, 0)

print("SPACE/W: jump  |  R: restart  |  ESC: quit")

glutMainLoop()
