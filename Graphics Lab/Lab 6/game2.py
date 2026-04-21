from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# ─────────────────────────────────────
#  GLOBALS
# ─────────────────────────────────────

paddleX   = 220.0      # left edge of the paddle
paddleR   = 280.0      # right edge of the paddle
paddleY   = 30.0       # fixed height of the paddle from the bottom
step      = 15.0       # how many pixels the paddle moves per key press

score     = 0          # starts at 0, increases by 10 each catch
game_over = False      # False = still playing, True = show win screen

# ─────────────────────────────────────
#  FALLING POINTS
#  each point is stored as: [x, y, active]
#  x      = horizontal position
#  y      = vertical position (starts at top, falls down)
#  active = True means still on screen, False means gone
# ─────────────────────────────────────

points = []            # empty list, filled by make_points()

def spawn_point():
    x = random.randint(10, 490)        # random horizontal position
    points.append([float(x), 500.0, True])  # starts at y=500 (top of window)

def make_points():
    points.clear()                     # wipe any old points first
    for i in range(5):
        x = random.randint(10, 490)    # random x position
        y = random.randint(100, 490)   # random y so they are spread out at start
        points.append([float(x), float(y), True])

# ─────────────────────────────────────
#  DRAW HELPERS
# ─────────────────────────────────────

def draw_text(x, y, text):
    glRasterPos2f(x, y)                # set where the text starts on screen
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))  # draw each character one by one

# ─────────────────────────────────────
#  DISPLAY
# ─────────────────────────────────────

def display():
    glClear(GL_COLOR_BUFFER_BIT)       # wipe the screen black every frame
    glLoadIdentity()                   # reset the transformation matrix

    if not game_over:

        # -- draw the paddle as a horizontal line --
        glColor3f(0.3, 0.6, 1.0)      # blue color
        glLineWidth(4.0)               # make the line 4 pixels thick
        glBegin(GL_LINES)
        glVertex2f(paddleX, paddleY)   # left end of paddle
        glVertex2f(paddleR,  paddleY)  # right end of paddle
        glEnd()

        # -- draw all active falling points --
        glColor3f(1.0, 1.0, 0.0)      # yellow color
        glPointSize(10)                # each point is 10 pixels wide
        for p in points:
            if p[2]:                   # only draw if the point is still active
                glBegin(GL_POINTS)
                glVertex2f(p[0], p[1]) # draw at the point's current x, y position
                glEnd()

        # -- score text top left --
        glColor3f(1.0, 1.0, 1.0)      # white color
        draw_text(10, 475, "Score: " + str(score) + " / 100")
        draw_text(10, 455, "A / D to move")

    else:
        # -- win screen --
        glColor3f(0.2, 0.9, 0.4)
        draw_text(150, 280, "YOU WIN!  Score: " + str(score))
        glColor3f(1.0, 1.0, 1.0)
        draw_text(120, 250, "Press R to restart  |  ESC to quit")

    glutSwapBuffers()                  # show the finished frame on screen

# ─────────────────────────────────────
#  UPDATE  — called automatically every 16ms by glutTimerFunc
# ─────────────────────────────────────

def update(value):
    global score, game_over

    if not game_over:

        for p in points:
            if not p[2]:               # skip points that are already inactive
                continue

            p[1] -= 2.0                # move the point DOWN by 2 pixels each frame
                                       # y=0 is the bottom, so subtracting moves it down

            # -- check if point lands on the paddle --
            if (p[1] <= paddleY + 5 and    # point has reached paddle height
                p[0] >= paddleX and        # point is right of paddle left edge
                p[0] <= paddleR):          # point is left of paddle right edge
                p[2] = False               # deactivate the point (disappear)
                score += 10                # add 10 to the score

            # -- check if point fell off the bottom of the screen --
            elif p[1] < 0:
                p[2] = False               # deactivate it, no penalty

        # remove all inactive points from the list
        new_list = []
        for p in points:
            if p[2]:
                new_list.append(p)
        points[:] = new_list

        # keep 4 points falling at all times — spawn new ones from the top
        while len(points) < 4:
            spawn_point()

        # check if player has reached 100 points
        if score >= 100:
            game_over = True

    glutTimerFunc(16, update, 0)       # call update() again after 16ms (keeps the loop going)
    glutPostRedisplay()                # tell GLUT to call display() again

# ─────────────────────────────────────
#  KEYBOARD
# ─────────────────────────────────────

def keyboard(key, x, y):
    global paddleX, paddleR, score, game_over

    if not game_over:
        if key == b'a':
            paddleX -= step            # move left edge left
            paddleR -= step            # move right edge left (both move together)
        if key == b'd':
            paddleX += step            # move left edge right
            paddleR += step            # move right edge right (both move together)

        # clamp paddle so it never goes off screen
        if paddleX < 0:   paddleX = 0;   paddleR = 60.0   # hit left wall
        if paddleR > 500: paddleR = 500; paddleX = 440.0  # hit right wall

    if key == b'r' or key == b'R':     # restart the game
        paddleX   = 220.0
        paddleR   = 280.0
        score     = 0
        game_over = False
        make_points()

    if key == b'\x1b':                 # ESC key — quit
        glutLeaveMainLoop()

    glutPostRedisplay()                # redraw after any key press

# ─────────────────────────────────────
#  INIT  — same as all your other files
# ─────────────────────────────────────

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)  # black background
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, 500, 0, 500, -1, 1)    # 2D coords: (0,0) bottom-left, (500,500) top-right
    glMatrixMode(GL_MODELVIEW)

# ─────────────────────────────────────
#  MAIN
# ─────────────────────────────────────

make_points()                          # fill the points list before anything starts

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Catch the Points - reach 100!")

init()

glutDisplayFunc(display)               # GLUT calls display() when screen needs drawing
glutKeyboardFunc(keyboard)             # GLUT calls keyboard() when a key is pressed
glutTimerFunc(16, update, 0)           # GLUT calls update() after 16ms to start the loop

print("A / D to move  |  R to restart  |  ESC to quit")

glutMainLoop()                         # hand control to GLUT — runs forever