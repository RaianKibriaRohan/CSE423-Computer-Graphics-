from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import random
import math
import time

# Room and game setup variables
room1_x, room1_y, room1_width, room1_depth = -1500, 400, 900, 900
room2_x, room2_y, room2_width, room2_depth = -1500, -1100, 900, 900
room3_x, room3_y, room3_width, room3_depth = 800, -1100, 900, 900
room4_x, room4_y, room4_width, room4_depth = -1800, 2500, 1500, 1500

orange_screen_flag = False
explosive_drums = [(-1100, 50), (-1400, -400), (100, 100)]
crates = [
    (-700, -800, 70), (-700, -1000, 70), (-700, -600, 70), (-700, -400, 70),
    (800, -1100, 70),
    (-1360.821003117057, 968.3919648628456, 70), (-1360, 768.3919648628456, 70),
    (-1360.821003117057, 568.3919648628456, 70),
    (-663.312606397818, 1200.4214978749658, 70), (-863.312606397818, 1200.4214978749658, 70)
]

# Chests for each room
chests = [
    # Room 1
    (-1400, 500, 0), (-1300, 600, 0),
    # Room 2
    (-1400, -1000, 0), (-1300, -900, 0),
    # Room 3
    (900, -1000, 0), (1000, -900, 0),
    # Room 4
    (-1700, 2600, 0), (-1600, 2700, 0)
]

scaling_factor = 1
gun_rotation = 0
game_over = True
enemy2_pos = [0, 0]
terrain_map = {}
tree_positions = []
cam_radius = 600
cam_angle = 0
cam_height = 600
cam_elev = 50
MIN_ELEV_DEG = 15
MAX_ELEV_DEG = 80
fovY = 105

cam_mode = "tp"
BACK_OFFSET = 40
LOOK_DISTANCE = 100
HEAD_HEIGHT = 145

cheat_mode = False
SPIN_SPEED_DEG = 30
cheat_cam_angle = None
gun_follow = False

CHEAT_FIRE_COOLDOWN = 6
cheat_cooldown = 0
AIM_TOLERANCE_DEG = 3

GRID_LENGTH = 500
WALL_THICK = 5
MARGIN_X = 30
MARGIN_FRONT = 57
MARGIN_BACK = 12
enemies = []
player_pos = [0, 0]
player_angle = 0

enemy_scale_factor = 1
enemy_scale_direction = 1
enemy_speed = 2

player_health = 1000
score = 0
player_dead = False
missed_bullets = 0
BULLET_SPEED = 50
BULLET_SIZE = 7
BULLET_LIFE = 60
bullets = []

special_enemies = []
special_enemies_spawned = False

# Boss-related variables
bosses = [
    {'room': 1, 'pos': [-1200, 700], 'health': 100, 'alive': False, 'respawn_timer': 0, 'last_shot': 0, 'death_count': 0},
    {'room': 2, 'pos': [-1200, -800], 'health': 100, 'alive': False, 'respawn_timer': 0, 'last_shot': 0, 'death_count': 0},
    {'room': 3, 'pos': [1100, -800], 'health': 100, 'alive': False, 'respawn_timer': 0, 'last_shot': 0, 'death_count': 0},
    {'room': 4, 'pos': [-1500, 2800], 'health': 100, 'alive': False, 'respawn_timer': 0, 'last_shot': 0, 'death_count': 0}
]
BOSS_BULLET_SPEED = 25
BOSS_BULLET_LIFE = 80
BOSS_SHOOT_INTERVAL = 2
boss_bullets = []
current_room = None

def draw_chest(x, y, z=0, length=70, width=50, height=40, top_height=20):
    glColor3f(0.545, 0.271, 0.075)
    glPushMatrix()
    glTranslatef(x, y, z)
    glBegin(GL_QUADS)
    glVertex3f(-length / 2, -width / 2, 0)
    glVertex3f(length / 2, -width / 2, 0)
    glVertex3f(length / 2, width / 2, 0)
    glVertex3f(-length / 2, width / 2, 0)
    glVertex3f(-length / 2, -width / 2, -height)
    glVertex3f(length / 2, -width / 2, -height)
    glVertex3f(length / 2, width / 2, -height)
    glVertex3f(-length / 2, width / 2, -height)
    glVertex3f(-length / 2, -width / 2, 0)
    glVertex3f(-length / 2, -width / 2, -height)
    glVertex3f(-length / 2, width / 2, -height)
    glVertex3f(-length / 2, width / 2, 0)
    glVertex3f(length / 2, -width / 2, 0)
    glVertex3f(length / 2, -width / 2, -height)
    glVertex3f(length / 2, width / 2, -height)
    glVertex3f(length / 2, width / 2, 0)
    glVertex3f(-length / 2, width / 2, 0)
    glVertex3f(length / 2, width / 2, 0)
    glVertex3f(length / 2, width / 2, -height)
    glVertex3f(-length / 2, width / 2, -height)
    glVertex3f(-length / 2, -width / 2, 0)
    glVertex3f(length / 2, -width / 2, 0)
    glVertex3f(length / 2, -width / 2, -height)
    glVertex3f(-length / 2, -width / 2, -height)
    glEnd()
    glColor3f(0.8, 0.4, 0.2)
    glPushMatrix()
    glTranslatef(x, y, z + height)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), length / 2, length / 2, top_height, 20, 20)
    glPopMatrix()
    glPopMatrix()

def draw_boss(x, y):
    glPushMatrix()
    glTranslatef(x, y, 50)
    glColor3f(0.8, 0.2, 0.2)
    glutSolidSphere(50, 20, 20)
    glColor3f(0.9, 0.9, 0.0)
    glPushMatrix()
    glTranslatef(0, 0, 60)
    glutSolidSphere(15, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(20, 20, 50)
    glutSolidSphere(15, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-20, -20, 50)
    glutSolidSphere(15, 10, 10)
    glPopMatrix()
    glColor3f(0.6, 0.2, 0.2)
    glPushMatrix()
    glTranslatef(50, 0, 0)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 10, 60, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-50, 0, 0)
    glRotatef(-90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 10, 60, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(40, 40, 20)
    glRotatef(45, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 10, 10, 50, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(30, 0, -50)
    gluCylinder(gluNewQuadric(), 10, 10, 60, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(-30, 0, -50)
    gluCylinder(gluNewQuadric(), 10, 10, 60, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 30, -50)
    gluCylinder(gluNewQuadric(), 10, 10, 60, 10, 10)
    glPopMatrix()
    glPopMatrix()

def spawn_boss_bullet(boss):
    px, py = player_pos
    bx, by = boss['pos']
    angle = math.degrees(math.atan2(py - by, px - bx)) - 90
    spawn_x = bx + 20 * math.cos(math.radians(angle + 90))
    spawn_y = by + 20 * math.sin(math.radians(angle + 90))
    boss_bullets.append([spawn_x, spawn_y, angle, BOSS_BULLET_LIFE])

def check_player_in_room():
    global current_room
    px, py = player_pos
    current_room = None
    print(f"Player at ({px}, {py})")
    # Check room1
    room_x, room_y, room_width, room_depth = room1_x, room1_y, room1_width, room1_depth
    if room_x <= px <= room_x + room_width and room_y <= py <= room_y + room_depth:
        current_room = 1
        print("Player in room1")
        for boss in bosses:
            if boss['room'] == 1 and not boss['alive'] and boss['respawn_timer'] <= 0:
                boss['alive'] = True
                boss['health'] = 100
                print(f"Boss in room {boss['room']} spawned at {boss['pos']}")
    # Check other rooms
    elif room2_x <= px <= room2_x + room2_width and room2_y <= py <= room2_y + room2_depth:
        current_room = 2
        print("Player in room2")
    elif room3_x <= px <= room3_x + room3_width and room3_y <= py <= room3_y + room3_depth:
        current_room = 3
        print("Player in room3")
    elif room4_x <= px <= room4_x + room4_width and room4_y <= py <= room4_y + room4_depth:
        current_room = 4
        print("Player in room4")

def update_bosses():
    global enemy_speed
    current_time = time.time()
    for boss in bosses:
        if boss['room'] != 1:
            boss['alive'] = False
            boss['respawn_timer'] = 0
            continue
        print(f"Boss room {boss['room']} - Alive: {boss['alive']}, Health: {boss['health']}, Respawn Timer: {boss['respawn_timer']}")
        if boss['alive']:
            if current_room == boss['room']:  # Only act if player is in the same room
                if current_time - boss['last_shot'] >= BOSS_SHOOT_INTERVAL:
                    spawn_boss_bullet(boss)
                    boss['last_shot'] = current_time
                move_boss_towards_player(boss)
            else:
                print(f"Boss in room {boss['room']} inactive (player not in room)")
        elif boss['respawn_timer'] > 0:
            boss['respawn_timer'] -= 1 / 60
            print(f"Respawn timer for boss in room {boss['room']}: {boss['respawn_timer']}")
            if boss['respawn_timer'] <= 0:
                boss['health'] = 100
                boss['alive'] = True
                boss['respawn_timer'] = 15
                print(f"Boss in room {boss['room']} respawned at {boss['pos']}")
        else:
            boss['respawn_timer'] = 15

def move_boss_towards_player(boss):
    global player_health, player_dead
    if player_health == 0 or not boss['alive']:
        return
    COLLISION_DIST = 50
    bx, by = boss['pos']
    px, py = player_pos
    dx, dy = px - bx, py - by
    dist = math.hypot(dx, dy)
    if dist == 0:
        return
    # Restrict boss movement within room1 boundaries
    room_x_min, room_x_max = room1_x, room1_x + room1_width
    room_y_min, room_y_max = room1_y, room1_y + room1_depth
    step_x = enemy_speed * dx / dist
    step_y = enemy_speed * dy / dist
    bx_new = bx + step_x
    by_new = by + step_y
    # Clamp boss position to room1 boundaries
    bx = max(room_x_min + 50, min(room_x_max - 50, bx_new))  # 50-unit buffer from edges
    by = max(room_y_min + 50, min(room_y_max - 50, by_new))
    if dist < COLLISION_DIST and not player_dead and current_room == boss['room']:
        player_health -= 1
        if player_health <= 0:
            player_health = 0
            player_dead = True
        print("Player hit by boss! Health:", player_health)
    boss['pos'] = [bx, by]

def update_boss_bullets():
    global player_health, player_dead
    keep_list = []
    for b in boss_bullets:
        x, y, ang, life = b
        rad = math.radians(ang + 90)
        x += BOSS_BULLET_SPEED * math.cos(rad)
        y += BOSS_BULLET_SPEED * math.sin(rad)
        life -= 1
        if life <= 0:
            continue
        px, py = player_pos
        if math.hypot(x - px, y - py) < 20 and not player_dead:
            player_health -= 1
            if player_health <= 0:
                player_health = 0
                player_dead = True
            continue
        keep_list.append([x, y, ang, life])
    boss_bullets[:] = keep_list

def draw_room(x, y, width, depth, height, door_width=100, door_height=150):
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    glVertex3f(x, y, 0)
    glVertex3f(x, y, height)
    glVertex3f(x, y + depth, height)
    glVertex3f(x, y + depth, 0)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(x + width, y, 0)
    glVertex3f(x + width, y, height)
    glVertex3f(x + width, y + depth, height)
    glVertex3f(x + width, y + depth, 0)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(x, y + depth, 0)
    glVertex3f(x + width, y + depth, 0)
    glVertex3f(x + width, y + depth, height)
    glVertex3f(x, y + depth, height)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(x, y, 0)
    glVertex3f(x + width - door_width, y, 0)
    glVertex3f(x + width - door_width, y, height)
    glVertex3f(x, y, height)
    glEnd()
    glColor3f(0, 0, 0)
    glBegin(GL_QUADS)
    glVertex3f(x + width - door_width, y, 0)
    glVertex3f(x + width, y, 0)
    glVertex3f(x + width, y, door_height)
    glVertex3f(x + width - door_width, y, door_height)
    glEnd()
    glColor3f(0.662, 0.662, 0.662)
    glBegin(GL_QUADS)
    glVertex3f(x, y, 1)
    glVertex3f(x + width, y, 1)
    glVertex3f(x + width, y + depth, 1)
    glVertex3f(x, y + depth, 1)
    glEnd()

def spawn_enemies():
    global enemies, special_enemies, special_enemies_spawned
    enemies = []
    for i in range(5):
        x = random.randint(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        y = random.randint(-GRID_LENGTH + 50, GRID_LENGTH - 50)
        enemies.append((x, y))
    x = -1465.2414404826753
    y = 774.4560684762663
    for drones in range(10):
        enemies.append((x, y))
        x += 80
        y += 70
    if score >= 10 and not special_enemies_spawned:
        print("Spawning special enemies!")
        special_enemies = []
        for i in range(3):
            x = random.randint(-GRID_LENGTH + 50, GRID_LENGTH - 50)
            y = random.randint(-GRID_LENGTH + 50, GRID_LENGTH - 50)
            special_enemies.append({'pos': (x, y), 'health': 3})
            print(f"Special enemy {i+1} spawned at ({x}, {y})")
        special_enemies_spawned = True
    # Force room1 boss to spawn initially but stay inactive until player enters
    for boss in bosses:
        if boss['room'] == 1:
            boss['alive'] = True
            print(f"Initial boss spawn in room {boss['room']} at {boss['pos']}")

def move_enemies_towards_player():
    room_x_min, room_x_max = -1500, -600
    room_y_min, room_y_max = 400, 1300
    global player_health, player_dead
    if player_health == 0:
        return
    COLLISION_DIST = 35
    for i in range(len(enemies)):
        ex, ey = enemies[i]
        px, py = player_pos
        dx, dy = px - ex, py - ey
        dist = math.hypot(dx, dy)
        if dist == 0:
            continue
        step_x = enemy_speed * dx / dist
        step_y = enemy_speed * dy / dist
        ex += step_x
        ey += step_y
        if dist < COLLISION_DIST and not player_dead:
            player_health -= 1
            if player_health <= 0:
                player_health = 0
                player_dead = True
            print("Player hit! Health:", player_health)
            ex = max(room_x_min + 50, min(room_x_max - 50, ex))
            ey = max(room_y_min + 50, min(room_y_max - 50, ey))
            if player_health <= 0:
                player_health = 0
        enemies[i] = (ex, ey)

def move_special_enemies_towards_player():
    room_x_min, room_x_max = -1500, -600
    room_y_min, room_y_max = 400, 1300
    global player_health, player_dead
    if player_health == 0:
        return
    COLLISION_DIST = 35
    for special_enemy in special_enemies:
        sx, sy = special_enemy['pos']
        px, py = player_pos
        dx, dy = px - sx, py - sy
        dist = math.hypot(dx, dy)
        if dist == 0:
            continue
        step_x = enemy_speed * dx / dist
        step_y = enemy_speed * dy / dist
        sx += step_x
        sy += step_y
        if dist < COLLISION_DIST and not player_dead:
            player_health -= 1
            if player_health <= 0:
                player_health = 0
                player_dead = True
            print("Player hit by special enemy! Health:", player_health)
            sx = max(room_x_min + 50, min(room_x_max - 50, sx))
            sy = max(room_y_min + 50, min(room_y_max - 50, sy))
            if player_health <= 0:
                player_health = 0
        special_enemy['pos'] = (sx, sy)

def draw_enemy_2(x, y, body_radius=50, head_radius=20):
    global scaling_factor
    glPushMatrix()
    glTranslatef(x, y, body_radius)
    glScalef(scaling_factor, scaling_factor, scaling_factor)
    glColor3f(1, 0, 0)
    glutSolidSphere(body_radius, 20, 20)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(x, y, body_radius + head_radius)
    glColor3f(0, 0, 0)
    glutSolidSphere(head_radius, 20, 20)
    glPopMatrix()

def spawn_player_bullet():
    rad = math.radians(player_angle + 90)
    spawn_x = player_pos[0] + 20 * math.cos(rad)
    spawn_y = player_pos[1] + 20 * math.sin(rad)
    bullets.append([spawn_x, spawn_y, player_angle, BULLET_LIFE])
    print("Player Bullet Fired!")

def cheat():
    global enemy_scale_factor, enemy_scale_direction, player_angle, cheat_cooldown
    player_angle = (player_angle + SPIN_SPEED_DEG) % 360
    if cheat_cooldown > 0:
        cheat_cooldown -= 1
    if cheat_cooldown == 0:
        px, py = player_pos
        for ex, ey in enemies:
            angle_to_enemy = (math.degrees(math.atan2(ey - py, ex - px)) - 90) % 360
            diff = min((angle_to_enemy - player_angle) % 360, (player_angle - angle_to_enemy) % 360)
            if diff < AIM_TOLERANCE_DEG:
                spawn_player_bullet()
                cheat_cooldown = CHEAT_FIRE_COOLDOWN
                break

def shrink_expand():
    global enemy_scale_factor, enemy_scale_direction
    enemy_scale_factor += 0.005 * enemy_scale_direction
    if enemy_scale_factor >= 1.2:
        enemy_scale_factor = 1.2
        enemy_scale_direction = -1
    elif enemy_scale_factor <= 0.8:
        enemy_scale_factor = 0.8
        enemy_scale_direction = 1

def animate():
    global enemy_scale_factor, enemy_scale_direction, player_angle, cheat_cooldown
    if player_dead:
        glutPostRedisplay()
        return
    if cheat_mode:
        cheat()
    shrink_expand()
    move_enemies_towards_player()
    move_special_enemies_towards_player()
    check_player_in_room()
    update_bosses()
    update_bullets()
    update_boss_bullets()
    glutPostRedisplay()

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

def third_person_camera():
    rad = math.radians(cam_angle)
    eye_x = cam_radius * math.cos(rad)
    eye_y = cam_radius * math.sin(rad)
    eye_z = cam_radius * math.sin(math.radians(cam_elev))
    gluLookAt(eye_x, eye_y, eye_z, 0, 0, 0, 0, 0, 1)

def first_person_camera():
    global player_pos, player_angle, cheat_mode, cheat_cam_angle, gun_follow
    if cheat_mode:
        view_angle = player_angle if gun_follow else cheat_cam_angle
    else:
        view_angle = player_angle
    dir_rad = math.radians(view_angle + 90)
    dir_x = math.cos(dir_rad)
    dir_y = math.sin(dir_rad)
    eye_x = player_pos[0] - BACK_OFFSET * dir_x
    eye_y = player_pos[1] - BACK_OFFSET * dir_y
    eye_z = HEAD_HEIGHT
    look_x = player_pos[0] + LOOK_DISTANCE * dir_x
    look_y = player_pos[1] + LOOK_DISTANCE * dir_y
    look_z = HEAD_HEIGHT
    gluLookAt(eye_x, eye_y, eye_z, look_x, look_y, look_z, 0, 0, 1)

def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if cam_mode == "tp":
        third_person_camera()
    else:
        first_person_camera()

def update_bullets():
    global bullets, enemies, special_enemies, score, missed_bullets, player_health, player_dead, orange_screen_flag, crates, special_enemies_spawned, enemy_speed
    keep_list = []
    for b in bullets:
        x = b[0]
        y = b[1]
        ang = b[2]
        life = b[3]
        rad = math.radians(ang + 90)
        x = x + BULLET_SPEED * math.cos(rad)
        y = y + BULLET_SPEED * math.sin(rad)
        life = life - 1
        hit_enemy = False
        j = 0
        while j < len(enemies):
            enemy_pos = enemies[j]
            ex = enemy_pos[0]
            ey = enemy_pos[1]
            if math.hypot(x - ex, y - ey) < 28:
                score = score + 1
                rx = random.randint(-GRID_LENGTH + 50, GRID_LENGTH - 50)
                ry = random.randint(-GRID_LENGTH + 50, GRID_LENGTH - 50)
                enemies[j] = (rx, ry)
                hit_enemy = True
                if score >= 10 and not special_enemies_spawned:
                    spawn_enemies()
                break
            j = j + 1
        if not hit_enemy:
            for i, special_enemy in enumerate(special_enemies):
                sx, sy = special_enemy['pos']
                if math.hypot(x - sx, y - sy) < 28:
                    special_enemy['health'] -= 1
                    print(f"Special enemy hit! Health: {special_enemy['health']}")
                    if special_enemy['health'] <= 0:
                        special_enemies.pop(i)
                        score += 5
                        print("Special enemy defeated!")
                    hit_enemy = True
                    break
        if not hit_enemy:
            for boss in bosses:
                if boss['alive']:
                    bx, by = boss['pos']
                    if math.hypot(x - bx, y - by) < 50:
                        boss['health'] -= 10
                        hit_enemy = True
                        if boss['health'] <= 0:
                            boss['alive'] = False
                            boss['respawn_timer'] = 15
                            score += 20
                            if boss['room'] == 1:
                                boss['death_count'] += 1
                                enemy_speed += 0.5
                                print(f"Boss speed increased to {enemy_speed}")
                        break
        if not hit_enemy:
            i = 0
            while i < len(explosive_drums):
                drum_pos = explosive_drums[i]
                drum_x = drum_pos[0]
                drum_y = drum_pos[1]
                if math.hypot(x - drum_x, y - drum_y) < 50:
                    dx = 1500
                    dy = 1500
                    explosive_drums[i] = (dx, dy)
                    hit_enemy = True
                    print("drum hit!")
                    for e in range(len(enemies)):
                        ex = random.randint(-GRID_LENGTH + 50, GRID_LENGTH - 50)
                        ey = random.randint(-GRID_LENGTH + 50, GRID_LENGTH - 50)
                        enemies[e] = (ex, ey)
                        score += 1
                    orange_screen_flag = True
                    break
                i += 1
            p = 0
            while p < len(crates):
                crate_pos = crates[p]
                crate_x = crate_pos[0]
                crate_y = crate_pos[1]
                if math.hypot(x - crate_x, y - crate_y) < 35:
                    cx = 1500
                    cy = 1500
                    crates[p] = (cx, cy, 70)
                    hit_enemy = True
                    print("crate hit!", crates[p])
                p = p + 1
        if not hit_enemy:
            keep_list.append([x, y, ang, life])
    bullets = keep_list

def draw_crate(x, y, z=0):
    crate_size = 70
    glColor3f(199/255, 157/255, 122/255)
    glPushMatrix()
    glTranslatef(x, y, z)
    glBegin(GL_QUADS)
    glVertex3f(-crate_size/2, -crate_size/2, crate_size/2)
    glVertex3f(crate_size/2, -crate_size/2, crate_size/2)
    glVertex3f(crate_size/2, crate_size/2, crate_size/2)
    glVertex3f(-crate_size/2, crate_size/2, crate_size/2)
    glVertex3f(-crate_size/2, -crate_size/2, -crate_size/2)
    glVertex3f(crate_size/2, -crate_size/2, -crate_size/2)
    glVertex3f(crate_size/2, crate_size/2, -crate_size/2)
    glVertex3f(-crate_size/2, crate_size/2, -crate_size/2)
    glVertex3f(-crate_size/2, -crate_size/2, crate_size/2)
    glVertex3f(-crate_size/2, -crate_size/2, -crate_size/2)
    glVertex3f(-crate_size/2, crate_size/2, -crate_size/2)
    glVertex3f(-crate_size/2, crate_size/2, crate_size/2)
    glVertex3f(crate_size/2, -crate_size/2, crate_size/2)
    glVertex3f(crate_size/2, -crate_size/2, -crate_size/2)
    glVertex3f(crate_size/2, crate_size/2, -crate_size/2)
    glVertex3f(crate_size/2, crate_size/2, crate_size/2)
    glVertex3f(-crate_size/2, crate_size/2, crate_size/2)
    glVertex3f(crate_size/2, crate_size/2, crate_size/2)
    glVertex3f(crate_size/2, crate_size/2, -crate_size/2)
    glVertex3f(-crate_size/2, crate_size/2, -crate_size/2)
    glVertex3f(-crate_size/2, -crate_size/2, crate_size/2)
    glVertex3f(crate_size/2, -crate_size/2, crate_size/2)
    glVertex3f(crate_size/2, -crate_size/2, -crate_size/2)
    glVertex3f(-crate_size/2, -crate_size/2, -crate_size/2)
    glEnd()
    glPopMatrix()

def draw_explosive_drum(x, y, z=0):
    radius = 30
    height = 90
    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(x, y, z)
    gluCylinder(gluNewQuadric(), radius, radius, height, 20, 20)
    glPushMatrix()
    glTranslatef(0, 0, height / 2)
    glColor3f(0.0, 0.0, 0.0)
    gluDisk(gluNewQuadric(), 0, radius, 20, 20)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(0, 0, -height / 2)
    glColor3f(0.0, 0.0, 0.0)
    gluDisk(gluNewQuadric(), 0, radius, 20, 20)
    glPopMatrix()
    glPopMatrix()

def draw_walls():
    draw_room(-1500, 400, 900, 900, 250, door_width=100, door_height=150)
    draw_room(-1500, -1100, 900, 900, 250, door_width=100, door_height=150)
    draw_room(800, -1100, 900, 900, 250, door_width=100, door_height=150)
    draw_room(-1800, 2500, 1500, 1500, 250, door_width=100, door_height=150)

def generate_terrain():
    global terrain_map, tree_positions
    tile_size = 50
    grid_multiplier = 7
    grid_range = GRID_LENGTH * grid_multiplier
    tree_positions.clear()
    terrain_map = {}
    pond_size = 300
    pond_origin_x = 400
    pond_origin_y = 200
    pond_tiles = set()
    for i in range(pond_origin_x, pond_origin_x + pond_size * tile_size, tile_size):
        for j in range(pond_origin_y, pond_origin_y + pond_size * tile_size, tile_size):
            pond_tiles.add((i, j))
    path_width = 2
    horizontal_mud_y = 0
    vertical_mud_x = 100
    def is_on_horizontal_path(j):
        return horizontal_mud_y - path_width * tile_size <= j <= horizontal_mud_y + path_width * tile_size
    def is_on_vertical_path(i):
        return vertical_mud_x - path_width * tile_size <= i <= vertical_mud_x + path_width * tile_size
    for i in range(-grid_range, grid_range, tile_size):
        for j in range(-grid_range, grid_range, tile_size):
            pos = (i, j)
            if pos in pond_tiles:
                terrain_type = 'water'
            elif is_on_horizontal_path(j) or is_on_vertical_path(i):
                terrain_type = 'mud'
            else:
                terrain_type = 'grass'
                if random.random() < 0.02:
                    tree_positions.append((i + tile_size // 2, j + tile_size // 2))
            terrain_map[pos] = terrain_type

def draw_bullets():
    glColor3f(1, 0, 0)
    for x, y, i, j in bullets:
        glPushMatrix()
        glTranslatef(x, y, BULLET_SIZE / 2)
        glutSolidCube(BULLET_SIZE)
        glPopMatrix()
    glColor3f(0.5, 0.5, 0.5)
    for x, y, i, j in boss_bullets:
        glPushMatrix()
        glTranslatef(x, y, BULLET_SIZE / 2)
        glutSolidCube(BULLET_SIZE)
        glPopMatrix()

def draw_enemy():
    glPushMatrix()
    glTranslatef(0, 0, 30)
    glScalef(enemy_scale_factor, enemy_scale_factor, enemy_scale_factor)
    glColor3f(1, 0, 0)
    gluSphere(gluNewQuadric(), 30, 15, 15)
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, 0, 30)
    gluSphere(gluNewQuadric(), 15, 10, 10)
    glPopMatrix()
    glPopMatrix()

def draw_special_enemy(x, y, body_size=50, head_radius=25):
    glPushMatrix()
    glTranslatef(x, y, body_size / 2)
    glColor3f(0.7, 0.0, 0.7)
    glScalef(1.5, 1.5, 1.5)
    glutSolidCube(body_size)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(x, y, body_size + head_radius + 5)
    glColor3f(1.0, 1.0, 0.0)
    glutSolidSphere(head_radius, 20, 20)
    glPopMatrix()

def draw_tree(x, y, z=0):
    trunk_height = 200
    trunk_radius = 10
    crown_radius = 50
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0.6, 0, 0.1)
    gluCylinder(gluNewQuadric(), trunk_radius, trunk_radius, trunk_height, 20, 20)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(x, y, z + trunk_height)
    glColor3f(0.0, 0.8, 0.0)
    glutSolidSphere(crown_radius, 20, 20)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(x, y, z + trunk_height + 3)
    glColor3f(0.0, 0.8, 0.0)
    glutSolidSphere(crown_radius * 0.8, 20, 20)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(x, y, z + trunk_height + 5)
    glColor3f(0.0, 0.8, 0.0)
    glutSolidSphere(crown_radius * 0.6, 20, 20)
    glPopMatrix()

def draw_player():
    glPushMatrix()
    if player_dead:
        glColor3f(0, 0, 1)
        glRotatef(-90, 1, 0, 0)
        glTranslatef(0, -40, 0)
    else:
        glColor3f(0, 0, 1)
    glPushMatrix()
    glTranslatef(-20, 0, 0)
    gluCylinder(gluNewQuadric(), 4, 7, 40, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glTranslatef(20, 0, 0)
    gluCylinder(gluNewQuadric(), 4, 7, 40, 10, 10)
    glPopMatrix()
    glTranslatef(0, 0, 40)
    glColor3f(0, 0.6, 0)
    glPushMatrix()
    glScalef(2, 1.2, 2)
    glutSolidCube(20)
    glPopMatrix()
    glColor3f(0.8, 0.8, 0.8)
    glPushMatrix()
    glTranslatef(0, 12, 15)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 8, 4, 45, 10, 10)
    glPopMatrix()
    glColor3f(1, 0.8, 0.6)
    glPushMatrix()
    glTranslatef(-16, 10, 10)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 6, 4, 25, 10, 10)
    glPopMatrix()
    glColor3f(1, 0.8, 0.6)
    glPushMatrix()
    glTranslatef(16, 10, 10)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 6, 4, 25, 10, 10)
    glPopMatrix()
    glColor3f(0, 0, 0)
    glPushMatrix()
    glTranslatef(0, 0, 37)
    gluSphere(gluNewQuadric(), 12, 10, 10)
    glPopMatrix()
    glPopMatrix()

def if_dead():
    global cheat_cooldown, cam_mode, player_pos, player_angle, player_health, player_dead, missed_bullets, score, cheat_mode, cheat_cam_angle, gun_follow, special_enemies, special_enemies_spawned
    cam_mode = "tp"
    cheat_cam_angle = None
    gun_follow = False
    cheat_mode = False
    player_dead = False
    player_pos[:] = [0, 0]
    player_health = 1000
    missed_bullets = 0
    score = 0
    bullets.clear()
    boss_bullets.clear()
    cheat_cooldown = 0
    special_enemies.clear()
    special_enemies_spawned = False
    for boss in bosses:
        boss['alive'] = False
        boss['respawn_timer'] = 0
        boss['health'] = 100
    spawn_enemies()

def cheat_on():
    global cheat_mode, cheat_cam_angle, player_angle
    cheat_mode = not cheat_mode
    if cheat_mode and cam_mode == "fp":
        cheat_cam_angle = player_angle
    else:
        cheat_cam_angle = None

def keyboardListener(key, x, y):
    global cheat_cooldown, cam_mode, player_pos, player_angle, player_health, player_dead, orange_screen_flag, cheat_mode, cheat_cam_angle, gun_follow
    move_speed = 20
    if player_dead:
        if key in (b'r', b'R'):
            if_dead()
        return
    if key in (b'q', b'Q') and orange_screen_flag:
        orange_screen_flag = False
    if key in (b'c', b'C') and not player_dead:
        cheat_on()
    if key in (b'v', b'V') and cheat_mode and cam_mode == "fp":
        gun_follow = not gun_follow
        if gun_follow:
            cheat_cam_angle = None
        else:
            cheat_cam_angle = player_angle
        return
    if key == b'a':
        player_angle = (player_angle + 5) % 360
    elif key == b'd':
        player_angle = (player_angle - 5) % 360
    rad = math.radians(player_angle + 90)
    dx = math.cos(rad) * move_speed
    dy = math.sin(rad) * move_speed
    if key == b'w':
        player_pos[0] += dx
        player_pos[1] += dy
        orange_screen_flag = False
    elif key == b's':
        player_pos[0] -= dx
        player_pos[1] -= dy
        orange_screen_flag = False

def specialKeyListener(key, x, y):
    global cam_angle, cam_elev
    if key == GLUT_KEY_LEFT:
        cam_angle = (cam_angle - 2) % 360
    elif key == GLUT_KEY_RIGHT:
        cam_angle = (cam_angle + 2) % 360
    elif key == GLUT_KEY_UP:
        cam_elev = min(cam_elev + 2, MAX_ELEV_DEG)
    elif key == GLUT_KEY_DOWN:
        cam_elev = max(cam_elev - 2, MIN_ELEV_DEG)
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global cam_mode, cheat_mode, cheat_cam_angle, gun_follow
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not player_dead:
        spawn_player_bullet()
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if cam_mode == "tp":
            cam_mode = "fp"
            if cheat_mode and not gun_follow:
                cheat_cam_angle = player_angle
        else:
            cam_mode = "tp"
            cheat_cam_angle = None
            gun_follow = False
        glutPostRedisplay()

def showScreen():
    global score, player_health, explosive_drums, orange_screen_flag, current_room
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    draw_bullets()
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], 1)
    glRotatef(player_angle, 0, 0, 1)
    draw_player()
    glPopMatrix()
    draw_walls()
    for x in explosive_drums:
        draw_explosive_drum(x[0], x[1], 0)
    for c in crates:
        draw_crate(c[0], c[1], 70)
    for c in chests:
        draw_chest(c[0], c[1], c[2])
    tile_size = 50
    draw_tree(300, -250, 0)
    val_x = 300
    val_y = -250
    c_x = -100
    c_y = -250
    g_x = -100
    g_y = 300
    r_x = 283.1811161232042 + 350
    r_y = 188.05407289332277
    for i in range(10):
        draw_tree(r_x, r_y, 0)
        r_x += 350
    for i in range(17):
        draw_tree(val_x, g_y, 0)
        g_y += 300
    for i in range(10):
        draw_tree(val_x, val_y, 0)
        val_y -= 300
    for i in range(10):
        draw_tree(c_x, c_y, 0)
        c_y -= 300
    if orange_screen_flag:
        glColor3f(1.0, 0.647, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(-1000, -1000)
        glVertex2f(1000, -1000)
        glVertex2f(1000, 1000)
        glVertex2f(-1000, 1000)
        glEnd()
    for (i, j), terrain_type in terrain_map.items():
        if terrain_type == 'grass':
            glColor3f(0.0, 0.6, 0.0)
        elif terrain_type == 'mud':
            glColor3f(0.55, 0.27, 0.07)
        elif terrain_type == 'water':
            glColor3f(0.0, 0.4, 0.7)
        glBegin(GL_QUADS)
        glVertex3f(i, j, 0)
        glVertex3f(i + tile_size, j, 0)
        glVertex3f(i + tile_size, j + tile_size, 0)
        glVertex3f(i, j + tile_size, 0)
        glEnd()
    for enemy_pos in enemies:
        if player_dead:
            break
        glPushMatrix()
        glTranslatef(enemy_pos[0], enemy_pos[1], 0)
        draw_enemy()
        glPopMatrix()
    for special_enemy in special_enemies:
        sx, sy = special_enemy['pos']
        glPushMatrix()
        glTranslatef(sx, sy, 0)
        draw_special_enemy(sx, sy)
        glPopMatrix()
    for boss in bosses:
        if boss['alive']:
            print(f"Drawing boss at {boss['pos']} in room {boss['room']}")
            draw_boss(boss['pos'][0], boss['pos'][1])
    draw_text(10, 770, f"Player Life Remaining: {player_health}")
    if player_dead:
        draw_text(10, 740, "GAME OVER!!! press R to restart")
        draw_text(10, 710, " ")
    else:
        draw_text(10, 740, f"Game Score: {score}")
        draw_text(10, 710, f"Player Bullet Missed: {missed_bullets}")
        if current_room:
            for boss in bosses:
                if boss['room'] == current_room and boss['alive']:
                    draw_text(10, 680, f"Boss Health: {boss['health']}%")
                    break
    glutSwapBuffers()

def main():
    glutInit()
    generate_terrain()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(300, 100)
    glutCreateWindow(b"Boom!!!!")
    glEnable(GL_DEPTH_TEST)
    spawn_enemies()
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(animate)
    glutMainLoop()

if __name__ == "__main__":
    main()