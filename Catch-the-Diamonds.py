from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

catcher_x = 0.0
catcher_target_x = 0.0  
catcher_speed = 0.8
catcher_smooth_factor = 0.099
catcher_y = -0.9  
diamond_x = 0.0
diamond_y = 0.9
diamond_speed = 0.05
score = 0
game_over = False
paused = False
frame_count = 0

seed = 12345
def prng():
    global seed
    seed = (seed * 1103515245 + 12345) & 0x7fffffff
    return seed / 0x7fffffff

diamond_colors = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0), 
                  (1.0, 1.0, 0.0), (1.0, 0.0, 1.0), (0.0, 1.0, 1.0)]
color_index = 0

def draw_line_zone0(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)
    x, y = x1, y1
    points.append((x, y))
    while x < x2:
        if d > 0:
            d += incNE
            y += 1
        else:
            d += incE
        x += 1
        points.append((x, y))
    return points

def find_zone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if abs(dx) >= abs(dy):
        if dx > 0 and dy >= 0:
            return 0
        if dx > 0 and dy < 0:
            return 7
        if dx < 0 and dy <= 0:
            return 4
        if dx < 0 and dy > 0:
            return 3
    else:
        if dx >= 0 and dy > 0:
            return 1
        if dx <= 0 and dy > 0:
            return 2
        if dx < 0 and dy < 0:
            return 5
        if dx > 0 and dy < 0:
            return 6
    return 0

def to_zone0(x, y, zone):
    if zone == 0: 
        return x, y
    elif zone == 1: 
        return y, x
    elif zone == 2: 
        return y, -x
    elif zone == 3: 
        return -x, y
    elif zone == 4: 
        return -x, -y
    elif zone == 5: 
        return -y, -x
    elif zone == 6: 
        return -y, x
    elif zone == 7: 
        return x, -y
    return x, y

def from_zone0(x, y, zone):
    if zone == 0: return x, y
    elif zone == 1: 
        return y, x
    elif zone == 2: 
        return -y, x
    elif zone == 3: 
        return -x, y
    elif zone == 4: 
        return -x, -y
    elif zone == 5: 
        return -y, -x
    elif zone == 6: 
        return y, -x
    elif zone == 7: 
        return x, -y
    return x, y

def draw_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    x1z0, y1z0 = to_zone0(x1, y1, zone)
    x2z0, y2z0 = to_zone0(x2, y2, zone)
    points = draw_line_zone0(x1z0, y1z0, x2z0, y2z0)
    return [from_zone0(px, py, zone) for px, py in points]

def draw_shape(x, y, shape_points, color):
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_POINTS)
    for (x1, y1), (x2, y2) in shape_points:
        points = draw_line(int(x1 * 100 + x * 100), int(y1 * 100 + y * 100), 
                          int(x2 * 100 + x * 100), int(y2 * 100 + y * 100))
        for px, py in points:
            glVertex2f(px / 100.0, py / 100.0)
    glEnd()

diamond_shape = [((-0.04, 0), (0, 0.06)), ((0, 0.06), (0.04, 0)), ((0.04, 0), (0, -0.06)), ((0, -0.06), (-0.04, 0))]
catcher_shape = [((-0.25, 0), (-0.2, 0.12)),   #Left side
                 ((-0.2, 0.12), (0.2, 0.12)),    #Top side
                 ((0.2, 0.12), (0.25, 0)),       #Right side
                 ((0.25, 0), (-0.25, 0))]        #Bottom

left_arrow = [((-0.1, 0), (0, 0.1)), ((0, 0.1), (0, -0.1)), ((-0.1, 0), (0, -0.1))]
play_icon = [((-0.1, -0.1), (-0.1, 0.1)), ((-0.1, 0.1), (0.1, 0)), ((0.1, 0), (-0.1, -0.1))]
pause_icon = [((-0.1, -0.1), (-0.1, 0.1)), ((0.1, -0.1), (0.1, 0.1))]
cross_icon = [((-0.1, -0.1), (0.1, 0.1)), ((-0.1, 0.1), (0.1, -0.1))]


def has_collided(x1, y1, w1, h1, x2, y2, w2, h2):
    return (x1 < x2 + w2 and x1 + w1 > x2 and y1 < y2 + h2 and y1 + h1 > y2)

def reset_game():
    global catcher_x, diamond_x, diamond_y, score, game_over, diamond_speed, color_index, frame_count
    catcher_x = 0.0
    diamond_x = prng() * 1.8 - 0.9
    diamond_y = 0.9
    score = 0
    game_over = False
    diamond_speed = 0.1
    color_index = int(prng() * 6) % 6
    frame_count = 0
    print("Starting Over")

def display():
    global diamond_y, score, game_over, diamond_x, diamond_speed, color_index
    glClear(GL_COLOR_BUFFER_BIT)
    catcher_color = (1.0, 0.0, 0.0) if game_over else (1.0, 1.0, 1.0)
    draw_shape(catcher_x,  catcher_y, catcher_shape, catcher_color)
    if not game_over and not paused:
        draw_shape(diamond_x, diamond_y, diamond_shape, diamond_colors[color_index])
    draw_shape(-0.9, 0.9, left_arrow, (0.0, 1.0, 1.0))
    draw_shape(0.0, 0.9, pause_icon if not paused else play_icon, (1.0, 0.5, 0.0))
    draw_shape(0.9, 0.9, cross_icon, (1.0, 0.0, 0.0))
    glutSwapBuffers()

def update():
    global diamond_y, score, game_over, diamond_x, diamond_speed, frame_count, color_index, catcher_x
    if game_over or paused:
        return
    frame_count += 1
    dt = 0.0160
    diamond_y -= diamond_speed * dt * 0.5
    diamond_speed += 0.00008 * dt

    # Smoothly move the catcher towards the target position
    catcher_x += (catcher_target_x - catcher_x) * catcher_smooth_factor

    if has_collided(catcher_x - 0.25, catcher_y, 0.5, 0.12, diamond_x - 0.08, diamond_y - 0.16, 0.16, 0.32):
        score += 1
        print("Score:", score)
        diamond_x = prng() * 1.8 - 0.9
        diamond_y = 0.9
        color_index = int(prng() * 6) % 6
    elif diamond_y < -0.9:
        game_over = True
        print("Game Over! Score:", score)

    glutPostRedisplay()

def keyboard(key, x, y):
    global catcher_target_x, paused
    if game_over or paused:
        return
    if key == GLUT_KEY_LEFT:
        catcher_target_x = max(catcher_target_x - catcher_speed * 0.2, -0.75)  
    elif key == GLUT_KEY_RIGHT:
        catcher_target_x = min(catcher_target_x + catcher_speed * 0.2, 0.75) 

def mouse(button, state, x, y):
    global paused
    if button != GLUT_LEFT_BUTTON or state != GLUT_UP:
        return
    wx = (x / 500.0) * 2 - 1
    wy = 1 - (y / 500.0) * 2
    if wy > 0.85:
        if -0.95 < wx < -0.85:
            reset_game()
            paused = False
        elif -0.05 < wx < 0.05:
            paused = not paused
        elif 0.85 < wx < 0.95:
            print("Goodbye! Score:", score)
            glutLeaveMainLoop()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutCreateWindow(b"Catch the Diamonds!")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glPointSize(2.0)
    glutDisplayFunc(display)
    glutSpecialFunc(keyboard)
    glutMouseFunc(mouse)
    glutIdleFunc(update)
    glutMainLoop()

if __name__ == "__main__":
    reset_game()
    main()
