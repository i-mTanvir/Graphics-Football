from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import random

# ─────────────────────────────────────
#  GLOBALS
# ─────────────────────────────────────

paddleX   = 220.0      # left edge of the paddle
paddleR   = 280.0      # right edge of the paddle
paddleY   = 30.0       # fixed height of the paddle from the bottom
step      = 15.0       # how many pixels the paddle moves per key press

spriteW   = 200         # width  to draw the sprite on screen
spriteH   = 60         # height to draw the sprite on screen
tex_id    = None       # will hold the loaded texture ID

score     = 0          # starts at 0, increases by 10 each catch
game_over = False      # False = still playing, True = show win screen

# ─────────────────────────────────────
#  TEXTURE LOADER
# ─────────────────────────────────────

def load_texture(filename):
    img  = Image.open(filename).convert("RGBA")   # open PNG, force RGBA (includes transparency)
    img  = img.transpose(Image.FLIP_TOP_BOTTOM)   # OpenGL reads pixels bottom-up so we flip
    data = img.tobytes()                          # convert image to raw bytes OpenGL can read

    tid = glGenTextures(1)                        # ask OpenGL for a texture slot
    glBindTexture(GL_TEXTURE_2D, tid)             # select that slot

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                 img.width, img.height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, data)  # upload the pixel data to OpenGL

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)  # no blur when shrinking
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)  # no blur when stretching (keeps pixel art sharp)

    return tid                                    # return the ID so we can use it later

# ─────────────────────────────────────
#  DRAW SPRITE
#  draws the PNG texture onto a quad at position x, y
# ─────────────────────────────────────

def draw_sprite(tid, x, y, w, h):
    glEnable(GL_TEXTURE_2D)                       # turn on texture mode
    glBindTexture(GL_TEXTURE_2D, tid)             # select our texture

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x,     y)      # bottom-left  of image → bottom-left  of quad
    glTexCoord2f(1, 0); glVertex2f(x + w, y)      # bottom-right of image → bottom-right of quad
    glTexCoord2f(1, 1); glVertex2f(x + w, y + h)  # top-right    of image → top-right    of quad
    glTexCoord2f(0, 1); glVertex2f(x,     y + h)  # top-left     of image → top-left     of quad
    glEnd()

    glDisable(GL_TEXTURE_2D)                      # turn off texture mode so other drawing is not affected

# ─────────────────────────────────────
#  FALLING POINTS
#  each point: [x, y, active]
# ─────────────────────────────────────

points = []

def spawn_point():
    x = random.randint(10, 490)               # random horizontal position
    points.append([float(x), 500.0, True])    # starts at y=500 (top of window)

def make_points():
    points.clear()
    for i in range(5):
        x = random.randint(10, 490)
        points.append([float(x), 500.0, True])   # all start from top

# ─────────────────────────────────────
#  DRAW HELPERS
# ─────────────────────────────────────

def draw_text(x, y, text):
    glRasterPos2f(x, y)                       # set where the text starts on screen
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))  # draw each character one by one

# ─────────────────────────────────────
#  DISPLAY
# ─────────────────────────────────────

def display():
    glClear(GL_COLOR_BUFFER_BIT)              # wipe the screen black every frame
    glLoadIdentity()                          # reset the transformation matrix

    if not game_over:

        # -- draw the paddle as the sprite image --
        glColor3f(1.0, 1.0, 1.0)             # set color to white so the sprite shows its real colors
        draw_sprite(tex_id, paddleX, paddleY, spriteW, spriteH)

        # -- draw all active falling points --
        glColor3f(1.0, 1.0, 0.0)             # yellow color
        glPointSize(10)                       # each point is 10 pixels wide
        
        # for p in points:
        #     if p[2]:                          # only draw if the point is still active
        #         glBegin(GL_POINTS)
        #         glVertex2f(p[0], p[1])        # draw at the point's current x, y position
        #         glEnd()

        for p in points:
            if p[2]:
                draw_sprite(tex_id, p[0] - 15, p[1] - 15, 30, 30)

        # -- score text top left --
        glColor3f(1.0, 1.0, 1.0)             # white color
        draw_text(10, 475, "Score: " + str(score) + " / 100")
        draw_text(10, 455, "A / D to move")

    else:
        # -- win screen --
        glColor3f(0.2, 0.9, 0.4)
        draw_text(150, 280, "YOU WIN!  Score: " + str(score))
        glColor3f(1.0, 1.0, 1.0)
        draw_text(120, 250, "Press R to restart  |  ESC to quit")

    glutSwapBuffers()                         # show the finished frame on screen

# ─────────────────────────────────────
#  UPDATE  — called automatically every 16ms by glutTimerFunc
# ─────────────────────────────────────

def update(value):
    global score, game_over

    if not game_over:

        for p in points:
            if not p[2]:                      # skip points that are already inactive
                continue

            p[1] -= 2.0                       # move the point DOWN by 2 pixels each frame

            # -- check if point lands on the paddle --
            if (p[1] <= paddleY + spriteH and # point has reached paddle height
                p[0] >= paddleX and           # point is right of paddle left edge
                p[0] <= paddleR):             # point is left of paddle right edge
                p[2] = False                  # deactivate the point
                score += 10                   # add 10 to the score

            # -- check if point fell off the bottom of the screen --
            elif p[1] < 0:
                p[2] = False                  # deactivate it, no penalty

        # remove inactive points from the list
        new_list = []
        for p in points:
            if p[2]:
                new_list.append(p)
        points[:] = new_list

        # spawn new points if less than 4 are falling
        if len(points) < 4:
            spawn_point()

        # check if player has reached 100 points
        if score >= 100:
            game_over = True

    glutTimerFunc(16, update, 0)              # call update() again after 16ms
    glutPostRedisplay()                       # tell GLUT to call display() again

# ─────────────────────────────────────
#  KEYBOARD
# ─────────────────────────────────────

def keyboard(key, x, y):
    global paddleX, paddleR, score, game_over

    if not game_over:
        if key == b'a':
            paddleX -= step                   # move left edge left
            paddleR -= step                   # move right edge left (both move together)
        if key == b'd':
            paddleX += step                   # move left edge right
            paddleR += step                   # move right edge right (both move together)

        # clamp paddle so it never goes off screen
        if paddleX < 0:   paddleX = 0;   paddleR = float(spriteW)         # hit left wall
        if paddleR > 500: paddleR = 500; paddleX = 500.0 - float(spriteW) # hit right wall

    if key == b'r' or key == b'R':            # restart the game
        paddleX   = 220.0
        paddleR   = 280.0
        score     = 0
        game_over = False
        make_points()

    if key == b'\x1b':                        # ESC key — quit
        glutLeaveMainLoop()

    glutPostRedisplay()                       # redraw after any key press

# ─────────────────────────────────────
#  INIT  — same as all your other files
# ─────────────────────────────────────

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)         # black background
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 0, 500, -1, 1)            # 2D coords: (0,0) bottom-left, (500,500) top-right
    glMatrixMode(GL_MODELVIEW)

    # enable transparency so the PNG background shows as see-through
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

# ─────────────────────────────────────
#  MAIN
# ─────────────────────────────────────

make_points()                                 # fill the points list before anything starts

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Catch the Points - reach 100!")

init()

tex_id = load_texture("ali.png")             # load ali.png — must be in the same folder as this file

glutDisplayFunc(display)                      # GLUT calls display() when screen needs drawing
glutKeyboardFunc(keyboard)                    # GLUT calls keyboard() when a key is pressed
glutTimerFunc(16, update, 0)                  # GLUT calls update() after 16ms to start the loop

print("A / D to move  |  R to restart  |  ESC to quit")

glutMainLoop()                                # hand control to GLUT — runs forever