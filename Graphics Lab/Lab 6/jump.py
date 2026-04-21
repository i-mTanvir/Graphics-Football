from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image

posX, posY = 200.0, 0.0
GROUND_Y = 0.0
step = 10.0
tex_id = None
spriteW, spriteH = 100, 100

# Jump state
velY = 0.0
isJumping = False
JUMP_FORCE = 15.0
GRAVITY = -0.8

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

    glColor3f(1.0, 1.0, 1.0)
    draw_sprite(tex_id, posX, posY, spriteW, spriteH)

    glutSwapBuffers()

# ─────────────────────────────────────
#  PHYSICS TIMER  (called every 16 ms ≈ 60 fps)
# ─────────────────────────────────────

def update(value):
    global posY, velY, isJumping

    if isJumping:
        velY += GRAVITY       # apply gravity each frame
        posY += velY

        if posY <= GROUND_Y:  # landed
            posY = GROUND_Y
            velY = 0.0
            isJumping = False

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)   # schedule next frame

# ─────────────────────────────────────
#  KEYBOARD
# ─────────────────────────────────────

def keyboard(key, x, y):
    global velY, isJumping

    if key == b'w':   # jump only when grounded
        velY = JUMP_FORCE
        isJumping = True

    # a / d still move horizontally if you want to keep them
    global posX
    if key == b'a': posX -= step
    if key == b'd': posX += step
    posX = posX % 500

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

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# ─────────────────────────────────────
#  MAIN
# ─────────────────────────────────────

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Apple Sprite - W to jump")

init()

tex_id = load_texture("apple.png")

glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutTimerFunc(16, update, 0)    # kick off the physics loop

print("W to jump, A/D to move")

glutMainLoop()