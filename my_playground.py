from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLUT import (
    GLUT_BITMAP_HELVETICA_12,
    GLUT_BITMAP_HELVETICA_18,
    GLUT_BITMAP_TIMES_ROMAN_24,
)
from OpenGL.GLU import *
import math
import time

W, H = 1024, 576
FIELD_LEFT, FIELD_RIGHT, FIELD_TOP, FIELD_BOTTOM = 78, 946, 524, 52
FIELD_MID_X, FIELD_MID_Y = (FIELD_LEFT + FIELD_RIGHT) // 2, (FIELD_TOP + FIELD_BOTTOM) // 2
GOAL_WIDTH, GOAL_HEIGHT, GOAL_MID_Y = 34, 128, FIELD_MID_Y
GOAL_A_X, GOAL_B_X = FIELD_LEFT, FIELD_RIGHT

ball = {
    'x':   float(FIELD_MID_X),
    'y':   float(FIELD_MID_Y),
    'r':   10,
    'vx':  0.0,   # velocity x
    'vy':  0.0,   # velocity y
    'friction': 0.93,   # speed decay per frame
}

def make_players():
    return [
        {'x': FIELD_RIGHT - 31,  'y': FIELD_MID_Y,       'team': 'R', 'key': ''},
        {'x': FIELD_RIGHT - 187, 'y': FIELD_MID_Y + 75,  'team': 'R', 'key': '7'},
        {'x': FIELD_RIGHT - 187, 'y': FIELD_MID_Y,       'team': 'R', 'key': '8'},
        {'x': FIELD_RIGHT - 187, 'y': FIELD_MID_Y - 75,  'team': 'R', 'key': '9'},
        {'x': FIELD_LEFT  + 31,  'y': FIELD_MID_Y,       'team': 'B', 'key': ''},
        {'x': FIELD_LEFT  + 187, 'y': FIELD_MID_Y + 75,  'team': 'B', 'key': '1'},
        {'x': FIELD_LEFT  + 187, 'y': FIELD_MID_Y,       'team': 'B', 'key': '2'},
        {'x': FIELD_LEFT  + 187, 'y': FIELD_MID_Y - 75,  'team': 'B', 'key': '3'},
    ]

players = make_players()
RED_KEY_TO_INDEX  = {b'7': 1, b'8': 2, b'9': 3}
BLUE_KEY_TO_INDEX = {b'1': 5, b'2': 6, b'3': 7}

score_a, score_b, game_time, last_tick = 0, 0, 180, time.time()
paused, game_over = False, False
goal_flash_timer, goal_flash_team = 0, ''
keys_held, special_keys_held = set(), set()
active_red_index, active_blue_index = None, None

PLAYER_SPEED = 3.8
PLAYER_R     = 12            # collision radius

GK_RED_IDX  = 0    # index of Red  GK in players[]
GK_BLUE_IDX = 4    # index of Blue GK in players[]

# Each GK has its own bounce direction (+1 = up, -1 = down)
gk_dir = [1, -1]          # [red_dir, blue_dir]
GK_BASE_SPEED    = 1.0    # normal patrol speed (px/frame)

# GK is clamped to the goal opening ± a small margin
_GK_HALF  = GOAL_HEIGHT // 2 - PLAYER_R    # half patrol range
GK_Y_MIN  = FIELD_MID_Y - _GK_HALF
GK_Y_MAX  = FIELD_MID_Y + _GK_HALF

def draw_circle(cx, cy, r, filled=True, segments=40):
    if filled:
        glBegin(GL_POLYGON)
    else:
        glBegin(GL_LINE_LOOP)
    for i in range(segments):
        angle = 2 * math.pi * i / segments
        glVertex2f(cx + r * math.cos(angle), cy + r * math.sin(angle))
    glEnd()

def draw_rect(x, y, w, h):
    glBegin(GL_QUADS)
    glVertex2f(x,     y)
    glVertex2f(x + w, y)
    glVertex2f(x + w, y + h)
    glVertex2f(x,     y + h)
    glEnd()

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

def draw_text_large(x, y, text):
    draw_text(x, y, text, GLUT_BITMAP_TIMES_ROMAN_24)

def draw_field():
    glColor3f(0.12, 0.58, 0.12)
    draw_rect(0, 0, W, H)
    glColor3f(0.10, 0.52, 0.10)
    stripe_w = (FIELD_RIGHT - FIELD_LEFT) // 8
    for i in range(0, 8, 2):
        draw_rect(FIELD_LEFT + i * stripe_w, FIELD_BOTTOM,
                  stripe_w, FIELD_TOP - FIELD_BOTTOM)
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2.5)
    glBegin(GL_LINE_LOOP)
    glVertex2f(FIELD_LEFT,  FIELD_BOTTOM)
    glVertex2f(FIELD_RIGHT, FIELD_BOTTOM)
    glVertex2f(FIELD_RIGHT, FIELD_TOP)
    glVertex2f(FIELD_LEFT,  FIELD_TOP)
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(FIELD_MID_X, FIELD_BOTTOM)
    glVertex2f(FIELD_MID_X, FIELD_TOP)
    glEnd()
    glLineWidth(2.0)
    draw_circle(FIELD_MID_X, FIELD_MID_Y, 47, filled=False, segments=50)
    glColor3f(1.0, 1.0, 1.0)
    draw_circle(FIELD_MID_X, FIELD_MID_Y, 4, filled=True)
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2.0)
    pb_h = 126; pb_w = 63
    glBegin(GL_LINE_LOOP)
    glVertex2f(FIELD_LEFT,        FIELD_MID_Y - pb_h//2)
    glVertex2f(FIELD_LEFT + pb_w, FIELD_MID_Y - pb_h//2)
    glVertex2f(FIELD_LEFT + pb_w, FIELD_MID_Y + pb_h//2)
    glVertex2f(FIELD_LEFT,        FIELD_MID_Y + pb_h//2)
    glEnd()
    glBegin(GL_LINE_LOOP)
    glVertex2f(FIELD_RIGHT,         FIELD_MID_Y - pb_h//2)
    glVertex2f(FIELD_RIGHT - pb_w,  FIELD_MID_Y - pb_h//2)
    glVertex2f(FIELD_RIGHT - pb_w,  FIELD_MID_Y + pb_h//2)
    glVertex2f(FIELD_RIGHT,         FIELD_MID_Y + pb_h//2)
    glEnd()

def draw_goalposts():
    gb, gt = GOAL_MID_Y - GOAL_HEIGHT // 2, GOAL_MID_Y + GOAL_HEIGHT // 2
    for x, w in [(GOAL_A_X, -GOAL_WIDTH), (GOAL_B_X, GOAL_WIDTH)]:
        glColor3f(1.0, 1.0, 1.0); glLineWidth(4.0)
        glBegin(GL_LINE_STRIP)
        for v in [(x+w, gb), (x, gb), (x, gt), (x+w, gt)]: glVertex2f(*v)
        glEnd()
        glColor3f(0.85, 0.85, 0.85); glLineWidth(1.0)
        for ny in range(gb, gt, 12):
            glBegin(GL_LINES); glVertex2f(x+w, ny); glVertex2f(x, ny); glEnd()

def draw_players():
    for i, p in enumerate(players):
        is_red_active  = (i == active_red_index)
        is_blue_active = (i == active_blue_index)
        is_active      = is_red_active or is_blue_active

        # Shadow
        glColor3f(0.05, 0.35, 0.05)
        draw_circle(p['x'] + 3, p['y'] - 3, PLAYER_R, filled=True, segments=20)

        # Body colour
        if p['team'] == 'R':
            glColor3f(0.85, 0.10, 0.10)
        else:
            glColor3f(0.05, 0.25, 0.85)
        draw_circle(p['x'], p['y'], PLAYER_R, filled=True, segments=20)

        # Active ring colour: yellow for red-team selection, cyan for blue-team selection
        if is_red_active:
            glColor3f(1.0, 1.0, 0.0)    # yellow
            glLineWidth(3.0)
            draw_circle(p['x'], p['y'], PLAYER_R + 4, filled=False, segments=24)
            glLineWidth(1.0)
        elif is_blue_active:
            glColor3f(0.0, 1.0, 1.0)    # cyan
            glLineWidth(3.0)
            draw_circle(p['x'], p['y'], PLAYER_R + 4, filled=False, segments=24)
            glLineWidth(1.0)
        else:
            glColor3f(1.0, 1.0, 1.0)
            glLineWidth(1.5)
            draw_circle(p['x'], p['y'], PLAYER_R, filled=False, segments=20)
            glLineWidth(1.0)

        # Key label inside player
        glColor3f(1.0, 1.0, 1.0)
        draw_text(p['x'] - 5, p['y'] - 5, p['key'], GLUT_BITMAP_HELVETICA_12)

def draw_ball():
    bx, by, br = ball['x'], ball['y'], ball['r']
    glColor3f(0.05, 0.35, 0.05)
    draw_circle(bx + 3, by - 3, br, filled=True)
    glColor3f(1.0, 1.0, 1.0)
    draw_circle(bx, by, br, filled=True)
    glColor3f(0.1, 0.1, 0.1)
    draw_circle(bx, by, br * 0.45, filled=True)
    for a in range(0, 360, 72):
        rad = math.radians(a)
        px = bx + br * 0.65 * math.cos(rad)
        py = by + br * 0.65 * math.sin(rad)
        draw_circle(px, py, br * 0.25, filled=True)

def draw_hud():
    # Top bar
    glColor3f(0.08, 0.08, 0.08)
    draw_rect(0, H - 45, W, 45)

    glColor3f(0.85, 0.20, 0.20)
    draw_text(20, H - 28, "RED TEAM", GLUT_BITMAP_HELVETICA_18)

    glColor3f(1.0, 1.0, 1.0)
    score_str = f"{score_b}  :  {score_a}"
    draw_text(W//2 - 35, H - 28, score_str, GLUT_BITMAP_TIMES_ROMAN_24)

    glColor3f(0.30, 0.55, 1.00)
    draw_text(W - 135, H - 28, "BLUE TEAM", GLUT_BITMAP_HELVETICA_18)

    # Bottom bar
    glColor3f(0.12, 0.12, 0.12)
    draw_rect(0, 0, W, 30)

    mins = int(game_time) // 60
    secs = int(game_time) % 60
    timer_str = f"TIME  {mins:01d}:{secs:02d}"
    glColor3f(1.0, 0.25, 0.25) if game_time <= 30 else glColor3f(0.80, 1.00, 0.80)
    draw_text(W//2 - 45, 8, timer_str, GLUT_BITMAP_HELVETICA_18)

    # Controls hint
    glColor3f(0.55, 0.55, 0.55)
    draw_text(8, 8, "7-9:Red(Arrows)  1-3:Blue(WASD)  P:Pause  R:Restart",
              GLUT_BITMAP_HELVETICA_12)

    # Red active player indicator (yellow)
    if active_red_index is not None:
        p = players[active_red_index]
        glColor3f(1.0, 1.0, 0.0)
        draw_text(W - 310, 8, f"RED #{p['key']}",
                  GLUT_BITMAP_HELVETICA_12)

    # Blue active player indicator (cyan)
    if active_blue_index is not None:
        p = players[active_blue_index]
        glColor3f(0.0, 1.0, 1.0)
        draw_text(W - 160, 8, f"BLUE #{p['key']}",
                  GLUT_BITMAP_HELVETICA_12)

    if paused and not game_over:
        glColor3f(1.0, 0.85, 0.0)
        draw_text(W//2 - 45, H - 28, "|| PAUSED", GLUT_BITMAP_HELVETICA_18)

def draw_goal_flash():
    global goal_flash_timer, goal_flash_team
    if goal_flash_timer <= 0:
        return
    alpha = min(1.0, goal_flash_timer / 60.0)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    if goal_flash_team == 'B':
        glColor4f(0.0, 0.2, 0.9, 0.35 * alpha)
    else:
        glColor4f(0.9, 0.1, 0.0, 0.35 * alpha)
    draw_rect(0, 0, W, H)
    glDisable(GL_BLEND)

    glColor3f(1.0, 1.0, 0.0)
    draw_text(W//2 - 55, H//2 + 10, "G O A L !", GLUT_BITMAP_TIMES_ROMAN_24)
    if goal_flash_team == 'B':
        glColor3f(0.4, 0.7, 1.0)
        draw_text(W//2 - 60, H//2 - 20, "BLUE TEAM SCORES!", GLUT_BITMAP_HELVETICA_18)
    else:
        glColor3f(1.0, 0.4, 0.4)
        draw_text(W//2 - 58, H//2 - 20, "RED TEAM SCORES!", GLUT_BITMAP_HELVETICA_18)
    goal_flash_timer -= 1

def draw_game_over():
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(0.0, 0.0, 0.0, 0.72)
    draw_rect(0, 0, W, H)
    glDisable(GL_BLEND)

    glColor3f(1.0, 0.85, 0.0)
    draw_text(W//2 - 75, H//2 + 60, "FULL TIME !", GLUT_BITMAP_TIMES_ROMAN_24)
    glColor3f(1.0, 1.0, 1.0)
    draw_text(W//2 - 70, H//2 + 20,
              f"RED  {score_b}  :  {score_a}  BLUE", GLUT_BITMAP_TIMES_ROMAN_24)

    if score_b > score_a:
        glColor3f(1.0, 0.4, 0.4)
        draw_text(W//2 - 65, H//2 - 20, "RED TEAM WINS!", GLUT_BITMAP_TIMES_ROMAN_24)
    elif score_a > score_b:
        glColor3f(0.4, 0.7, 1.0)
        draw_text(W//2 - 70, H//2 - 20, "BLUE TEAM WINS!", GLUT_BITMAP_TIMES_ROMAN_24)
    else:
        glColor3f(0.9, 0.9, 0.9)
        draw_text(W//2 - 50, H//2 - 20, "IT'S A DRAW!", GLUT_BITMAP_TIMES_ROMAN_24)

    glColor3f(0.70, 0.70, 0.70)
    draw_text(W//2 - 75, H//2 - 65, "Press  R  to play again", GLUT_BITMAP_HELVETICA_18)

def update_goalkeepers():
    """Bounce GKs up/down inside the goal bar automatically
    at a constant speed."""
    for slot, idx in enumerate([GK_RED_IDX, GK_BLUE_IDX]):
        p = players[idx]
        spd = GK_BASE_SPEED

        # Move in current direction
        p['y'] += spd * gk_dir[slot]

        # Bounce at goal-bar limits
        if p['y'] >= GK_Y_MAX:
            p['y'] = GK_Y_MAX
            gk_dir[slot] = -1
        elif p['y'] <= GK_Y_MIN:
            p['y'] = GK_Y_MIN
            gk_dir[slot] = 1

        # GK also deflects the ball if they touch it
        check_player_ball_collision(p, 0, spd * gk_dir[slot])

def reset_positions():
    global players, active_red_index, active_blue_index
    ball['x']  = float(FIELD_MID_X)
    ball['y']  = float(FIELD_MID_Y)
    ball['vx'] = 0.0
    ball['vy'] = 0.0
    players = make_players()
    active_red_index  = None
    active_blue_index = None

def reset_game():
    global score_a, score_b, game_time, game_over, paused
    global goal_flash_timer, goal_flash_team
    score_a = 0; score_b = 0
    game_time = 3 * 60
    game_over = False
    paused    = False
    goal_flash_timer = 0
    goal_flash_team  = ''
    reset_positions()

def _apply_movement(p, dx, dy):
    """Shared: move player by (dx,dy), clamp to field, kick ball."""
    if dx != 0 and dy != 0:   # diagonal normalise
        dx *= 0.7071
        dy *= 0.7071
    nx = max(FIELD_LEFT  + PLAYER_R, min(FIELD_RIGHT  - PLAYER_R, p['x'] + dx))
    ny = max(FIELD_BOTTOM + PLAYER_R, min(FIELD_TOP   - PLAYER_R, p['y'] + dy))
    p['x'], p['y'] = nx, ny
    if dx != 0 or dy != 0:
        check_player_ball_collision(p, dx, dy)

def update_movements():
    if active_red_index is not None:
        dx = (GLUT_KEY_RIGHT in special_keys_held) - (GLUT_KEY_LEFT in special_keys_held)
        dy = (GLUT_KEY_UP in special_keys_held) - (GLUT_KEY_DOWN in special_keys_held)
        _apply_movement(players[active_red_index], dx * PLAYER_SPEED, dy * PLAYER_SPEED)
    if active_blue_index is not None:
        dx = (b'd' in keys_held) - (b'a' in keys_held)
        dy = (b'w' in keys_held) - (b's' in keys_held)
        _apply_movement(players[active_blue_index], dx * PLAYER_SPEED, dy * PLAYER_SPEED)

def check_player_ball_collision(p, pdx, pdy):
    bx, by = ball['x'], ball['y']
    dist = math.hypot(bx - p['x'], by - p['y'])
    touch_dist = PLAYER_R + ball['r']

    if dist <= touch_dist:
        if dist == 0:
            # Avoid division by zero: push ball straight up
            nx, ny = 0.0, 1.0
        else:
            nx = (bx - p['x']) / dist
            ny = (by - p['y']) / dist

        # kick strength proportional to player speed (+ a base impulse)
        spd = math.hypot(pdx, pdy)
        kick = spd * 1.5 + 2.25

        ball['vx'] = nx * kick
        ball['vy'] = ny * kick

        # Immediately separate ball so it doesn't stay inside player
        overlap = touch_dist - dist + 1
        ball['x'] = bx + nx * overlap
        ball['y'] = by + ny * overlap

def update_ball():
    ball['x'] += ball['vx']
    ball['y'] += ball['vy']

    # Apply friction
    ball['vx'] *= ball['friction']
    ball['vy'] *= ball['friction']

    # Stop tiny drift
    if abs(ball['vx']) < 0.05: ball['vx'] = 0.0
    if abs(ball['vy']) < 0.05: ball['vy'] = 0.0

    br = ball['r']

    # Bounce off side walls
    if ball['x'] - br < FIELD_LEFT:
        ball['x'] = FIELD_LEFT + br
        ball['vx'] = abs(ball['vx']) * 0.7
    if ball['x'] + br > FIELD_RIGHT:
        ball['x'] = FIELD_RIGHT - br
        ball['vx'] = -abs(ball['vx']) * 0.7

    # Bounce off top/bottom walls
    if ball['y'] - br < FIELD_BOTTOM:
        ball['y'] = FIELD_BOTTOM + br
        ball['vy'] = abs(ball['vy']) * 0.7
    if ball['y'] + br > FIELD_TOP:
        ball['y'] = FIELD_TOP - br
        ball['vy'] = -abs(ball['vy']) * 0.7

def check_goal():
    global score_a, score_b, goal_flash_timer, goal_flash_team
    bx, by, br = ball['x'], ball['y'], ball['r']
    gy_bot = GOAL_MID_Y - GOAL_HEIGHT // 2
    gy_top = GOAL_MID_Y + GOAL_HEIGHT // 2

    # Ball enters left goal (Blue's net) → Red scores
    if bx - br <= GOAL_A_X and gy_bot <= by <= gy_top:
        score_b += 1
        goal_flash_timer = 90
        goal_flash_team  = 'R'
        reset_positions()
        return

    # Ball enters right goal (Red's net) → Blue scores
    if bx + br >= GOAL_B_X and gy_bot <= by <= gy_top:
        score_a += 1
        goal_flash_timer = 90
        goal_flash_team  = 'B'
        reset_positions()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    draw_field()
    draw_goalposts()
    draw_players()
    draw_ball()
    draw_hud()
    draw_goal_flash()

    if game_over:
        draw_game_over()

    glutSwapBuffers()

def update(value):
    global game_time, game_over, last_tick

    if not paused and not game_over:
        now = time.time()
        dt  = now - last_tick
        last_tick = now

        update_movements()
        update_goalkeepers()
        update_ball()
        check_goal()

        game_time -= dt
        if game_time <= 0:
            game_time = 0
            game_over = True
    else:
        last_tick = time.time()

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def keyboard_down(key, x, y):
    global paused, game_over, active_red_index, active_blue_index
    keys_held.add(key)

    # Select Red player (keys 0-3)
    if key in RED_KEY_TO_INDEX:
        active_red_index = RED_KEY_TO_INDEX[key]

    # Select Blue player (keys 5-8)
    if key in BLUE_KEY_TO_INDEX:
        active_blue_index = BLUE_KEY_TO_INDEX[key]

    if key == b'p':
        if not game_over:
            paused = not paused

    if key == b'r':
        reset_game()

    if key == b'\x1b':   # ESC
        import sys; sys.exit(0)

def keyboard_up(key, x, y):
    keys_held.discard(key)

def special_down(key, x, y):
    special_keys_held.add(key)

def special_up(key, x, y):
    special_keys_held.discard(key)

def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, W, 0, H)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(W, H)
glutInitWindowPosition(100, 60)
glutCreateWindow(b"DIU Football Game  -  Computer Graphics Lab")

init()

glutDisplayFunc(display)
glutKeyboardFunc(keyboard_down)
glutKeyboardUpFunc(keyboard_up)
glutSpecialFunc(special_down)
glutSpecialUpFunc(special_up)
glutTimerFunc(16, update, 0)

print("=" * 58)
print("  DIU FOOTBALL GAME  –  4 vs 4   (2-Player Mode)")
print("-" * 58)
print("  PLAYER 1  –  RED  TEAM")
print("    Select : 7  8  9")
print("    Move   : Arrow keys  (↑ ↓ ← →)")
print("  PLAYER 2  –  BLUE TEAM")
print("    Select : 1  2  3")
print("    Move   : W A S D")
print("  * GKs auto-patrol the goal automatically")
print("  P : Pause / Resume     R : Restart     ESC : Quit")
print("=" * 58)

glutMainLoop()
