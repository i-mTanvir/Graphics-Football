from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image

posX, posY = 0.0, 0.0
step = 10.0
tex_id = None
spriteW, spriteH = 100, 100  # size of the apple sprite

# ─────────────────────────────────────
#  TEXTURE LOADER
# ─────────────────────────────────────

def load_texture(filename):
    img  = Image.open(filename).convert("RGBA")
    img  = img.transpose(Image.FLIP_TOP_BOTTOM)
    data = img.tobytes()

    tid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tid)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                 img.width, img.height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    return tid

# ─────────────────────────────────────
#  DRAW SPRITE
# ─────────────────────────────────────

def draw_sprite(tid, x, y, w, h):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, tid)

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x,     y)
    glTexCoord2f(1, 0); glVertex2f(x + w, y)
    glTexCoord2f(1, 1); glVertex2f(x + w, y + h)
    glTexCoord2f(0, 1); glVertex2f(x,     y + h)
    glEnd()

    glDisable(GL_TEXTURE_2D)

# ─────────────────────────────────────
#  DISPLAY
# ─────────────────────────────────────

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    glColor3f(1.0, 1.0, 1.0)                      # white so sprite shows true colors
    draw_sprite(tex_id, posX, posY, spriteW, spriteH)

    glutSwapBuffers()

# ─────────────────────────────────────
#  KEYBOARD
# ─────────────────────────────────────

def keyboard(key, x, y):
    global posX, posY

    if key == b'w': posY += step
    if key == b's': posY -= step
    if key == b'a': posX -= step
    if key == b'd': posX += step

    posX = posX % 500
    posY = posY % 500

    glutPostRedisplay()

# ─────────────────────────────────────
#  INIT
# ─────────────────────────────────────

def init():
    glClearColor(1.0, 5.0, 0.0, 1.0)
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 0, 500, -1, 1)
    glMatrixMode(GL_MODELVIEW)

    # enable transparency for PNG files
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# ─────────────────────────────────────
#  MAIN
# ─────────────────────────────────────

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Apple Sprite - WASD to move")

init()

tex_id = load_texture("apple.png")    # <-- put your apple PNG here

glutDisplayFunc(display)
glutKeyboardFunc(keyboard)

print("WASD to move")

glutMainLoop()