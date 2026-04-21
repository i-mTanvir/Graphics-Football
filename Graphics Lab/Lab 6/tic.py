from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image

# ─────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────

WINDOW_SIZE  = 500          # window is 500x500 pixels
CELL_SIZE    = WINDOW_SIZE // 3   # each cell is ~166x166 pixels
SPRITE_SIZE  = 120          # X and O sprites drawn 120x120 inside each cell
SPRITE_OFF   = (CELL_SIZE - SPRITE_SIZE) // 2  # offset to center sprite inside cell

# ─────────────────────────────────────
#  GLOBALS
# ─────────────────────────────────────

board   = [[0,0,0],[0,0,0],[0,0,0]]  # 3x3 grid, 0=empty 1=X 2=O
turn    = 1                           # 1 = X's turn, 2 = O's turn
winner  = 0                           # 0=playing 1=X won 2=O won 3=draw

cur1X, cur1Y = 0, 2    # Player 1 cursor starts top-left  (col=0, row=2)
cur2X, cur2Y = 2, 0    # Player 2 cursor starts bot-right (col=2, row=0)

tex_x = None            # texture ID for X sprite
tex_o = None            # texture ID for O sprite

# ─────────────────────────────────────
#  TEXTURE LOADER
# ─────────────────────────────────────

def load_texture(filename):
    img  = Image.open(filename).convert("RGBA")   # open image, force 4 channels (RGBA)
    img  = img.transpose(Image.FLIP_TOP_BOTTOM)   # flip vertically — OpenGL reads bottom-up
    data = img.tobytes()                          # convert to raw bytes for OpenGL

    tid = glGenTextures(1)                        # reserve a texture slot in GPU memory
    glBindTexture(GL_TEXTURE_2D, tid)             # select that slot as active

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA,
                 img.width, img.height,
                 0, GL_RGBA, GL_UNSIGNED_BYTE, data)  # upload pixel data to GPU

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)  # sharp when shrinking
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)  # sharp when stretching

    return tid                                    # return ID so we can use it later

# ─────────────────────────────────────
#  DRAW SPRITE
#  draws a PNG texture at pixel position (x,y) with size (w,h)
# ─────────────────────────────────────

def draw_sprite(tid, x, y, w, h):
    glEnable(GL_TEXTURE_2D)                       # turn on texture mode
    glBindTexture(GL_TEXTURE_2D, tid)             # select the texture to use

    glBegin(GL_QUADS)                             # start drawing a rectangle
    glTexCoord2f(0, 0); glVertex2f(x,     y    )  # bottom-left  corner
    glTexCoord2f(1, 0); glVertex2f(x + w, y    )  # bottom-right corner
    glTexCoord2f(1, 1); glVertex2f(x + w, y + h)  # top-right    corner
    glTexCoord2f(0, 1); glVertex2f(x,     y + h)  # top-left     corner
    glEnd()

    glDisable(GL_TEXTURE_2D)                      # turn off texture mode

# ─────────────────────────────────────
#  DRAW TEXT
#  draws a string at pixel position (x,y)
# ─────────────────────────────────────

def draw_text(x, y, text):
    glRasterPos2f(x, y)                           # move the drawing pen to (x,y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))  # draw each character

# ─────────────────────────────────────
#  DRAW GRID
#  draws 2 vertical and 2 horizontal lines to make the 3x3 grid
# ─────────────────────────────────────

def draw_grid():
    glColor3f(1.0, 1.0, 1.0)                      # white lines
    glLineWidth(3.0)                              # 3 pixels thick

    glBegin(GL_LINES)

    # vertical line 1 — divides column 0 and column 1
    glVertex2f(CELL_SIZE,     0          )
    glVertex2f(CELL_SIZE,     WINDOW_SIZE)

    # vertical line 2 — divides column 1 and column 2
    glVertex2f(CELL_SIZE * 2, 0          )
    glVertex2f(CELL_SIZE * 2, WINDOW_SIZE)

    # horizontal line 1 — divides row 0 and row 1
    glVertex2f(0,           CELL_SIZE    )
    glVertex2f(WINDOW_SIZE, CELL_SIZE    )

    # horizontal line 2 — divides row 1 and row 2
    glVertex2f(0,           CELL_SIZE * 2)
    glVertex2f(WINDOW_SIZE, CELL_SIZE * 2)

    glEnd()

# ─────────────────────────────────────
#  DRAW CURSOR
#  draws a colored rectangle border around a cell (col, row)
# ─────────────────────────────────────

def draw_cursor(col, row, r, g, b, active):
    if active:
        glColor3f(r, g, b)        # bright color when it is this player's turn
    else:
        glColor3f(r*0.3, g*0.3, b*0.3)   # dark dim color when it is NOT this player's turn

    glLineWidth(4.0)              # thick border so cursor is easy to see

    # calculate pixel position of this cell's bottom-left corner
    px = col * CELL_SIZE          # pixel x of left edge of cell
    py = row * CELL_SIZE          # pixel y of bottom edge of cell

    glBegin(GL_LINE_LOOP)         # LINE_LOOP draws connected lines that close back to start
    glVertex2f(px + 4,            py + 4           )   # bottom-left  with small inset
    glVertex2f(px + CELL_SIZE - 4, py + 4          )   # bottom-right with small inset
    glVertex2f(px + CELL_SIZE - 4, py + CELL_SIZE-4)   # top-right    with small inset
    glVertex2f(px + 4,             py + CELL_SIZE-4)   # top-left     with small inset
    glEnd()

# ─────────────────────────────────────
#  CHECK WINNER
#  checks all rows, columns, and diagonals for a winner
# ─────────────────────────────────────

def check_winner():
    global winner

    # check all 3 rows — if all 3 cells in a row are the same non-zero value
    for row in range(3):
        if board[0][row] == board[1][row] == board[2][row] != 0:
            winner = board[0][row]   # set winner to 1 (X) or 2 (O)
            return

    # check all 3 columns — if all 3 cells in a column are the same non-zero value
    for col in range(3):
        if board[col][0] == board[col][1] == board[col][2] != 0:
            winner = board[col][0]
            return

    # check diagonal top-left to bottom-right: (0,2) (1,1) (2,0)
    if board[0][2] == board[1][1] == board[2][0] != 0:
        winner = board[0][2]
        return

    # check diagonal top-right to bottom-left: (2,2) (1,1) (0,0)
    if board[2][2] == board[1][1] == board[0][0] != 0:
        winner = board[2][2]
        return

    # check for draw — if no cell is empty (all non-zero) and no winner found above
    if all(board[c][r] != 0 for c in range(3) for r in range(3)):
        winner = 3   # 3 means draw

# ─────────────────────────────────────
#  RESET GAME
#  resets everything back to the starting state
# ─────────────────────────────────────

def reset_game():
    global board, turn, winner, cur1X, cur1Y, cur2X, cur2Y

    board   = [[0,0,0],[0,0,0],[0,0,0]]  # clear all cells
    turn    = 1                           # X always goes first
    winner  = 0                           # no winner yet

    cur1X, cur1Y = 0, 2   # Player 1 cursor back to top-left
    cur2X, cur2Y = 2, 0   # Player 2 cursor back to bottom-right

# ─────────────────────────────────────
#  DISPLAY — called every frame to draw the screen
# ─────────────────────────────────────

def display():
    glClear(GL_COLOR_BUFFER_BIT)    # wipe screen black
    glLoadIdentity()                # reset transformation matrix

    if winner == 0:                 # ── GAME STILL IN PROGRESS ──

        draw_grid()                 # draw the 3x3 white grid lines

        # loop through every cell in the board
        for col in range(3):
            for row in range(3):
                # calculate pixel position to draw sprite at center of cell
                px = col * CELL_SIZE + SPRITE_OFF   # x pixel = cell left edge + centering offset
                py = row * CELL_SIZE + SPRITE_OFF   # y pixel = cell bottom edge + centering offset

                if board[col][row] == 1:            # cell contains X
                    glColor3f(1.0, 1.0, 1.0)        # white so sprite shows true colors
                    draw_sprite(tex_x, px, py, SPRITE_SIZE, SPRITE_SIZE)

                elif board[col][row] == 2:          # cell contains O
                    glColor3f(1.0, 1.0, 1.0)        # white so sprite shows true colors
                    draw_sprite(tex_o, px, py, SPRITE_SIZE, SPRITE_SIZE)

        # draw Player 1 cursor in BLUE — bright if P1's turn, dim if not
        draw_cursor(cur1X, cur1Y, 0.3, 0.6, 1.0, turn == 1)

        # draw Player 2 cursor in RED — bright if P2's turn, dim if not
        draw_cursor(cur2X, cur2Y, 1.0, 0.3, 0.3, turn == 2)

        # draw turn indicator text at top of screen
        glColor3f(1.0, 1.0, 0.0)                    # yellow text
        if turn == 1:
            draw_text(10, 480, "Player 1 (X) — WASD to move, F to place")
        else:
            draw_text(10, 480, "Player 2 (O) — IJKL to move, H to place")

    else:                           # ── GAME OVER SCREEN ──

        if winner == 1:
            glColor3f(0.3, 0.6, 1.0)               # blue for X wins
            draw_text(150, 300, "Player 1 (X) WINS!")
        elif winner == 2:
            glColor3f(1.0, 0.3, 0.3)               # red for O wins
            draw_text(150, 300, "Player 2 (O) WINS!")
        else:
            glColor3f(1.0, 1.0, 0.0)               # yellow for draw
            draw_text(180, 300, "IT'S A DRAW!")

        glColor3f(1.0, 1.0, 1.0)                   # white text
        draw_text(130, 260, "Press R to restart  |  ESC to quit")

        # still draw the final board state behind the message
        draw_grid()

        for col in range(3):
            for row in range(3):
                px = col * CELL_SIZE + SPRITE_OFF
                py = row * CELL_SIZE + SPRITE_OFF
                if board[col][row] == 1:
                    glColor3f(1.0, 1.0, 1.0)
                    draw_sprite(tex_x, px, py, SPRITE_SIZE, SPRITE_SIZE)
                elif board[col][row] == 2:
                    glColor3f(1.0, 1.0, 1.0)
                    draw_sprite(tex_o, px, py, SPRITE_SIZE, SPRITE_SIZE)

    glutSwapBuffers()               # show the finished frame — swap back buffer to front

# ─────────────────────────────────────
#  KEYBOARD — called every time a key is pressed
# ─────────────────────────────────────

def keyboard(key, x, y):
    global cur1X, cur1Y, cur2X, cur2Y, turn, winner

    if winner == 0:     # only accept movement/placement if game is still going

        # ── PLAYER 1 CONTROLS (WASD + F) ──

        if key == b'w':                  # move cursor UP
            cur1Y = min(cur1Y + 1, 2)    # increase row, clamp max at 2

        if key == b's':                  # move cursor DOWN
            cur1Y = max(cur1Y - 1, 0)    # decrease row, clamp min at 0

        if key == b'a':                  # move cursor LEFT
            cur1X = max(cur1X - 1, 0)    # decrease col, clamp min at 0

        if key == b'd':                  # move cursor RIGHT
            cur1X = min(cur1X + 1, 2)    # increase col, clamp max at 2

        if key == b'f':                  # PLACE X
            if turn == 1:                # only works on Player 1's turn
                if board[cur1X][cur1Y] == 0:       # only if cell is empty
                    board[cur1X][cur1Y] = 1         # place X on the board
                    check_winner()                  # check if this move won the game
                    if winner == 0:                 # if game still going
                        turn = 2                    # swap to Player 2's turn

        # ── PLAYER 2 CONTROLS (IJKL + H) ──

        if key == b'i':                  # move cursor UP
            cur2Y = min(cur2Y + 1, 2)

        if key == b'k':                  # move cursor DOWN
            cur2Y = max(cur2Y - 1, 0)

        if key == b'j':                  # move cursor LEFT
            cur2X = max(cur2X - 1, 0)

        if key == b'l':                  # move cursor RIGHT
            cur2X = min(cur2X + 1, 2)

        if key == b'h':                  # PLACE O
            if turn == 2:                # only works on Player 2's turn
                if board[cur2X][cur2Y] == 0:       # only if cell is empty
                    board[cur2X][cur2Y] = 2         # place O on the board
                    check_winner()                  # check if this move won the game
                    if winner == 0:                 # if game still going
                        turn = 1                    # swap to Player 1's turn

    # ── GLOBAL KEYS — work any time ──

    if key == b'r' or key == b'R':       # R = restart
        reset_game()

    if key == b'\x1b':                   # ESC = quit
        glutLeaveMainLoop()

    glutPostRedisplay()                  # tell GLUT to redraw the screen

# ─────────────────────────────────────
#  INIT — one-time OpenGL setup
# ─────────────────────────────────────

def init():
    glClearColor(0.05, 0.05, 0.05, 1.0)  # very dark grey background (not pure black)
    glViewport(0, 0, WINDOW_SIZE, WINDOW_SIZE)
    glMatrixMode(GL_PROJECTION)           # switch to projection matrix
    glLoadIdentity()
    glOrtho(0, WINDOW_SIZE, 0, WINDOW_SIZE, -1, 1)  # 2D coords (0,0)=bottom-left
    glMatrixMode(GL_MODELVIEW)            # switch back to modelview matrix

    glEnable(GL_BLEND)                            # enable transparency
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # standard alpha blending

# ─────────────────────────────────────
#  MAIN
# ─────────────────────────────────────

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)     # double buffered RGB window
glutInitWindowSize(WINDOW_SIZE, WINDOW_SIZE)    # 500x500 window
glutInitWindowPosition(100, 100)                # position on screen
glutCreateWindow(b"Tic Tac Toe - P1: WASD+F  P2: IJKL+H")  # window title

init()                          # run OpenGL setup

tex_x = load_texture("ali.png")  # load X sprite — must be in same folder
tex_o = load_texture("apple.png")  # load O sprite — must be in same folder

glutDisplayFunc(display)        # register display callback
glutKeyboardFunc(keyboard)      # register keyboard callback

print("Player 1 (X): WASD to move, F to place")
print("Player 2 (O): IJKL to move, H to place")
print("R to restart | ESC to quit")

glutMainLoop()                  # hand control to GLUT — runs forever