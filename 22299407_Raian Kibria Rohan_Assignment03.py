from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import math
import random

# Game state variables
player_pos = [0, 0, 30]
player_angle = 0
player_life = 5
game_score = 0
bullets_missed = 0
game_over = False
cheat_mode = False
cheat_vision = False
camera_mode = 'third'
camera_pos = [0, 500, 500]
fovY = 120
GRID_LENGTH = 600
BULLET_SPEED = 6
ENEMY_SPEED = 0.12
BULLET_LIFETIME = 100
cheat_fire_cooldown = 0

bullets = []
enemies = []
enemy_scale_direction = [1] * 5

def init_enemies():
    global enemies
    enemies = []
    for _ in range(5):
        # Random position on grid edges
        side = random.choice(['left', 'right', 'top', 'bottom'])
        if side == 'left':
            x, y = -GRID_LENGTH, random.uniform(-GRID_LENGTH, GRID_LENGTH)
        elif side == 'right':
            x, y = GRID_LENGTH, random.uniform(-GRID_LENGTH, GRID_LENGTH)
        elif side == 'top':
            x, y = random.uniform(-GRID_LENGTH, GRID_LENGTH), GRID_LENGTH
        else:  # bottom
            x, y = random.uniform(-GRID_LENGTH, GRID_LENGTH), -GRID_LENGTH
        enemies.append([x, y, 30, 1.0])  # z=30, initial scale=1.0

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(player_angle, 0, 0, 1)  # Rotate around z-axis

    # Head (sphere)
    glColor3f(0, 0, 0)  
    glPushMatrix()
    glTranslatef(0, 0, 50)  # head above the body
    gluSphere(gluNewQuadric(), 20, 10, 10)
    glPopMatrix()

    # Body (cuboid)
    glColor3f(0, 0.5, 0)  # Green body color
    glPushMatrix()
    glTranslatef(0, 0, 30)  
    glScalef(1.5, 0.5, 1.5)  
    glutSolidCube(40)
    glPopMatrix()

    # Left Arm (cuboid)
    glColor3f(0.9, 0.7, 0.5)  
    glPushMatrix()
    glTranslatef(-40, 0, 45)  
    glScalef(0.5, 0.25, 1.0)  
    glutSolidCube(40) 
    glPopMatrix()

    # Right Arm (cuboid)
    glColor3f(0.9, 0.7, 0.5)  
    glPushMatrix()
    glTranslatef(40, 0, 45)  
    glScalef(0.5, 0.25, 1.0) 
    glutSolidCube(40)  
    glPopMatrix()

    # Left Leg (cylinder)
    glColor3f(0.0, 0.0, 1.0)  
    glPushMatrix()
    glTranslatef(-15, 0, -30) 
    glRotatef(90, 1, 0, 0)  
    gluCylinder(gluNewQuadric(), 7, 7, 40, 10, 10) 
    glPopMatrix()

    # Right Leg (cylinder)
    glPushMatrix()
    glTranslatef(15, 0, -30)  
    glRotatef(90, 1, 0, 0)  
    gluCylinder(gluNewQuadric(), 7, 7, 40, 10, 10)  
    glPopMatrix()

    # Gun (cylinder)
    glColor3f(0.5, 0.5, 0.5)  
    glPushMatrix()
    glTranslatef(50, 0, 30) 
    glRotatef(90, 0, 1, 0) 
    gluCylinder(gluNewQuadric(), 5, 5, 30, 10, 10)
    glPopMatrix()

    glPopMatrix()

def draw_enemy(x, y, z, scale):
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # Draw the bottom sphere (larger)
    glColor3f(1, 0, 0)  # Red
    glPushMatrix()
    gluSphere(gluNewQuadric(), 25 * scale, 10, 10)  # Larger sphere
    glPopMatrix()

    # Draw the top sphere (smaller)
    glColor3f(0.0, 0.0, 0.0)  # Black for the top part
    glPushMatrix()
    glTranslatef(0, 0, 40 * scale)  # Move up for the top sphere
    gluSphere(gluNewQuadric(), 15 * scale, 10, 10)  # Smaller sphere
    glPopMatrix()

    glPopMatrix()

def draw_bullet(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1.0, 0.0, 0.0)
    gluSphere(gluNewQuadric(), 5, 10, 10) 
    glPopMatrix()
    
def draw_grid():
    glBegin(GL_QUADS)
    # Dynamic grid: divide into smaller quads
    step = GRID_LENGTH / 10
    for i in range(-10, 10):
        for j in range(-10, 10):
            x1 = i * step
            y1 = j * step
            x2 = (i + 1) * step
            y2 = (j + 1) * step
            # Checkerboard pattern
            if (i + j) % 2 == 0:
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.7, 0.5, 0.95)
            glVertex3f(x1, y1, 0)
            glVertex3f(x2, y1, 0)
            glVertex3f(x2, y2, 0)
            glVertex3f(x1, y2, 0)
    glEnd()

    # Boundaries (colored walls)
    height = 100
    
    # Bottom border (white)
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, height)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, height)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # Right border (green)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, height)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # Left border (blue)
    glColor3f(0.0, 0.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, height)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, height)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glEnd()

    # Top border (cyan)
    glColor3f(0.0, 1.0, 1.0)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, height)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, height)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glEnd()

def keyboardListener(key, x, y):
    global player_pos, player_angle, cheat_mode, cheat_vision, game_over, player_life, game_score, bullets_missed
    if game_over and key == b'r':
        # Reset game
        player_life = 5
        game_score = 0
        bullets_missed = 0
        game_over = False
        player_pos = [0, 0, 30]
        player_angle = 0
        cheat_mode = False
        cheat_vision = False
        init_enemies()
        return
    if game_over:
        return

    # Move forward (W) with boundary check
    if key == b'w':
        rad = math.radians(player_angle)
        new_x = player_pos[0] + 5 * math.cos(rad)
        new_y = player_pos[1] + 5 * math.sin(rad)
        
        # Boundary check: Ensure player stays within the grid
        if abs(new_x) <= GRID_LENGTH and abs(new_y) <= GRID_LENGTH:
            player_pos[0] = new_x
            player_pos[1] = new_y

    # Move backward (S) with boundary check
    if key == b's':
        rad = math.radians(player_angle)
        new_x = player_pos[0] - 5 * math.cos(rad)
        new_y = player_pos[1] - 5 * math.sin(rad)
        
        # Boundary check: Ensure player stays within the grid
        if abs(new_x) <= GRID_LENGTH and abs(new_y) <= GRID_LENGTH:
            player_pos[0] = new_x
            player_pos[1] = new_y

    # Rotate gun left (A)
    if key == b'a':
        player_angle += 5

    # Rotate gun right (D)
    if key == b'd':
        player_angle -= 5

    # Toggle cheat mode (C)
    if key == b'c':
        cheat_mode = not cheat_mode

    # Toggle gun following (V) - only in first-person mode when cheat mode is active
    if key == b'v' and cheat_mode and camera_mode == 'first':
        cheat_vision = not cheat_vision

def specialKeyListener(key, x, y):
    global camera_pos
    x, y, z = camera_pos
    if key == GLUT_KEY_UP:
        y += 10
    if key == GLUT_KEY_DOWN:
        y = max(50, y - 10)  # Prevent camera from going too low
    if key == GLUT_KEY_LEFT:
        angle = math.atan2(y, x) + math.radians(5)
        radius = math.sqrt(x*x + y*y)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
    if key == GLUT_KEY_RIGHT:
        angle = math.atan2(y, x) - math.radians(5)
        radius = math.sqrt(x*x + y*y)
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
    camera_pos = [x, y, z]

def mouseListener(button, state, x, y):
    global camera_mode, bullets, game_over
    if game_over:
        return
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Fire bullet
        rad = math.radians(player_angle)
        bx = player_pos[0] + 50 * math.cos(rad)  # Start at gun tip
        by = player_pos[1] + 50 * math.sin(rad)
        bullets.append([bx, by, 30, player_angle, BULLET_LIFETIME])
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        camera_mode = 'first' if camera_mode == 'third' else 'third'

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if camera_mode == 'first':
        # First-person: camera follows gun
        rad = math.radians(player_angle)
        # Offset to move camera angle to the right (subtract 10 degrees)
        camera_rad = math.radians(player_angle - 10)  # Shift 10 degrees to the right
        if cheat_mode and cheat_vision:
            # Position camera at gun tip, looking along gun direction
            x = player_pos[0] + 20 * math.cos(camera_rad)  # Adjusted with camera_rad
            y = player_pos[1] + 20 * math.sin(camera_rad)
            z = player_pos[2]  # Gun height
            tx = player_pos[0] + 100 * math.cos(camera_rad)  # Look further along adjusted direction
            ty = player_pos[1] + 100 * math.sin(camera_rad)
            tz = player_pos[2]
        else:
            # Standard first-person view
            x = player_pos[0] - 100 * math.cos(camera_rad)  # Behind player, adjusted with camera_rad
            y = player_pos[1] - 100 * math.sin(camera_rad)
            z = player_pos[2] + 50
            tx = player_pos[0] + 100 * math.cos(camera_rad)  # Look ahead, adjusted with camera_rad
            ty = player_pos[1] + 100 * math.sin(camera_rad)
            tz = player_pos[2]
        gluLookAt(x, y, z, tx, ty, tz, 0, 0, 1)
    else:
        # Third-person
        x, y, z = camera_pos
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)

def update_game():
    global bullets, enemies, player_life, bullets_missed, game_score, game_over, enemy_scale_direction, player_angle, cheat_fire_cooldown
    if game_over:
        return
    # Update bullets
    new_bullets = []
    for bullet in bullets:
        bx, by, bz, angle, lifetime = bullet
        rad = math.radians(angle)
        bx += BULLET_SPEED * math.cos(rad)
        by += BULLET_SPEED * math.sin(rad)
        lifetime -= 1
        if lifetime > 0 and abs(bx) < GRID_LENGTH and abs(by) < GRID_LENGTH:
            new_bullets.append([bx, by, bz, angle, lifetime])
        else:
            bullets_missed += 1
            if bullets_missed >= 10:
                game_over = True
    bullets = new_bullets

    # Update enemies
    for i, enemy in enumerate(enemies):
        ex, ey, ez, scale = enemy
        # Move toward player
        dx = player_pos[0] - ex
        dy = player_pos[1] - ey
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            ex += ENEMY_SPEED * dx / dist
            ey += ENEMY_SPEED * dy / dist
        # Update scale (shrink/expand)
        scale += 0.02 * enemy_scale_direction[i]  # Adjusted as per previous request
        if scale > 1.5:
            enemy_scale_direction[i] = -1
            scale = 1.5
        elif scale < 0.5:
            enemy_scale_direction[i] = 1
            scale = 0.5
        enemies[i] = [ex, ey, ez, scale]

    # Check collisions
    new_enemies = enemies[:]
    for bullet in bullets:
        bx, by, bz = bullet[:3]
        for i, enemy in enumerate(enemies):
            ex, ey, ez, scale = enemy
            dist = math.sqrt((bx - ex)**2 + (by - ey)**2 + (bz - ez)**2)
            if dist < 20 * scale:  # Hit detection
                game_score += 1
                # Respawn enemy
                side = random.choice(['left', 'right', 'top', 'bottom'])
                if side == 'left':
                    x, y = -GRID_LENGTH, random.uniform(-GRID_LENGTH, GRID_LENGTH)
                elif side == 'right':
                    x, y = GRID_LENGTH, random.uniform(-GRID_LENGTH, GRID_LENGTH)
                elif side == 'top':
                    x, y = random.uniform(-GRID_LENGTH, GRID_LENGTH), GRID_LENGTH
                else:
                    x, y = random.uniform(-GRID_LENGTH, GRID_LENGTH), -GRID_LENGTH
                new_enemies[i] = [x, y, 30, 1.0]
                enemy_scale_direction[i] = 1
                bullets.remove(bullet)
                break
    enemies = new_enemies

    # Enemy and player clash
    for enemy in enemies:
        ex, ey, ez = enemy[:3]
        dist = math.sqrt((player_pos[0] - ex)**2 + (player_pos[1] - ey)**2 + (player_pos[2] - ez)**2)
        if dist < 40:
            player_life -= 1
            if player_life <= 0:
                game_over = True
            # Respawn enemy
            side = random.choice(['left', 'right', 'top', 'bottom'])
            if side == 'left':
                x, y = -GRID_LENGTH, random.uniform(-GRID_LENGTH, GRID_LENGTH)
            elif side == 'right':
                x, y = GRID_LENGTH, random.uniform(-GRID_LENGTH, GRID_LENGTH)
            elif side == 'top':
                x, y = random.uniform(-GRID_LENGTH, GRID_LENGTH), GRID_LENGTH
            else:
                x, y = random.uniform(-GRID_LENGTH, GRID_LENGTH), -GRID_LENGTH
            enemies[enemies.index(enemy)] = [x, y, 30, 1.0]

    # Cheat mode: auto-rotate and fire only at enemies within line of sight
    if cheat_mode:
        player_angle += 2  # Continuous rotation
        # Decrease cooldown
        if cheat_fire_cooldown > 0:
            cheat_fire_cooldown -= 1
        # Check for enemies in line of sight
        rad = math.radians(player_angle)
        px, py = player_pos[0], player_pos[1]
        for enemy in enemies:
            ex, ey = enemy[:2]
            # Vector from player to enemy
            dx, dy = ex - px, ey - py
            # Angle to enemy
            enemy_angle = math.degrees(math.atan2(dy, dx)) % 360
            # Check if enemy is in line of sight (within 2 degrees for precision)
            if abs((player_angle % 360) - enemy_angle) < 2 and cheat_fire_cooldown == 0:
                # Fire bullet
                bx = px + 50 * math.cos(rad)
                by = py + 50 * math.sin(rad)
                bullets.append([bx, by, 30, player_angle, BULLET_LIFETIME])
                cheat_fire_cooldown = 30  # Set cooldown to prevent rapid firing
                break  # Fire one bullet at the first visible enemy

def idle():
    update_game()
    glutPostRedisplay()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    draw_grid()
    draw_player()
    for enemy in enemies:
        draw_enemy(*enemy)
    for bullet in bullets:
        draw_bullet(bullet[0], bullet[1], bullet[2])
    # Display game info
    draw_text(10, 770, f"Player Life Remaining: {player_life}")
    draw_text(10, 740, f"Game Score: {game_score}")
    draw_text(10, 710, f"Player Bullets Missed: {bullets_missed}")
    if game_over:
        draw_text(400, 400, "Game Over! Press R to Restart")
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"Bullet Frenzy")
    glEnable(GL_DEPTH_TEST)  # Enable depth testing
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    init_enemies()
    glutMainLoop()

if __name__ == "__main__":
    main()