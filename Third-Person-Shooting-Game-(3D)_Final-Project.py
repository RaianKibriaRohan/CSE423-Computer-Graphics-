from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math


cam_orbit_angle = 0
boss_active = False
boss_pos = [0, 0]
boss_health = 150
boss_max_health = 150
boss_size = 3.0
boss_angle = 0
boss_fire_cooldown = 1
boss_fire_rate = 3
boss_bullets = []
BOSS_BULLET_SPEED = 40
BOSS_BULLET_SIZE = 15
BOSS_BULLET_LIFE = 25
BOSS_BULLET_COLOR = (1.0, 0.5, 0.0)
boss_defeated = False

ultimate_active = False
ultimate_timer = 0
ULTIMATE_DURATION = 150
ultimate_cooldown = 0
ULTIMATE_COOLDOWN = 900
normal_move_speed = 25

explosion_effects = []
EXPLOSION_DURATION = 60

health_packs = []

player_in_room = False
player_in_water = False
ammo_packs = []
rooms = [(-1500, -1100, 900, 900), (800, -1100, 900, 900), (-2200, 1800, 1500, 1500)]
key_states = {b'w': False, b'a': False, b's': False, b'd': False}

room4_x, room4_y, room4_width, room4_depth = -1800, 2500, 1500, 1500
orange_screen_flag = False
explosive_drums = [(-1100, 50), (-1400, -400), (100, 100),
                   (-2064.7779086129917,1942.35205192705),
                   (-767.8478392443643,2771.1602691850376)]
crates =[
    (-700, -800, 70),
    (-700, -1000, 70),
    (-700, -600, 70),
    (-700, -400, 70),
    (-2050, 3180)]

for k in range(4):
    crates.append((crates[-1][0] + 300, crates[-1][1]))

factor = 200
for l in range(3):
    crates.append((950, -250 - factor))
    factor += 200

current_weapon = 1
handgun_ammo = 200
automatic_ammo = 100
handgun_fire_rate = 10
automatic_fire_rate = 2

enemy_respawn_timer = 0
ENEMY_RESPAWN_DELAY = 30
MAX_ENEMIES = 11
previous_location = []
left_mouse_pressed = False
fire_cooldown = 0
FIRE_RATE = 1
previous_location = []
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

BACK_OFFSET = 40
LOOK_DISTANCE = 100
HEAD_HEIGHT = 145

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
enemy_speed = 10
Object_collision = False
player_health = 100
player_key = 0
score = 0
player_dead = False
missed_bullets = 0
BULLET_SPEED = 70
BULLET_SIZE = 7
BULLET_LIFE = 25
bullets = []


def initialize_health_packs():
    global health_packs
    health_packs.clear()


    for room in rooms:
        room_x, room_y, width, depth = room

        health_pack_x = room_x + width - 130
        health_pack_y = room_y + depth - 130
        health_packs.append((health_pack_x, health_pack_y))

def draw_health_pack(x, y, z=70):
    glPushMatrix()
    glTranslatef(x, y, z)


    glColor3f(1.0, 1.0, 1.0)  # White
    glutSolidCube(30)


    glColor3f(1.0, 0.0, 0.0)  # Red
    glBegin(GL_QUADS)

    glVertex3f(-15, -5, 15.1)
    glVertex3f(15, -5, 15.1)
    glVertex3f(15, 5, 15.1)
    glVertex3f(-15, 5, 15.1)

    glVertex3f(-5, -15, 15.1)
    glVertex3f(5, -15, 15.1)
    glVertex3f(5, 15, 15.1)
    glVertex3f(-5, 15, 15.1)
    glEnd()

    glPopMatrix()

def draw_boss(x, y, angle=0):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glRotatef(angle, 0, 0, 1)
    glScalef(boss_size, boss_size, boss_size)


    glColor3f(0.7, 0.0, 0.0)
    glutSolidSphere(30, 20, 20)

    glColor3f(0.3, 0.3, 0.3)
    for i in range(8):
        glPushMatrix()
        angle_rad = math.radians(i * 45)
        glTranslatef(math.cos(angle_rad) * 20, math.sin(angle_rad) * 20, 0)
        glScalef(15, 15, 8)
        glutSolidCube(1)
        glPopMatrix()


    glPushMatrix()
    glTranslatef(0, 25, 0)


    glColor3f(1.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(-10, 0, 5)
    glutSolidSphere(5, 8, 8)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(10, 0, 5)
    glutSolidSphere(5, 8, 8)
    glPopMatrix()


    glColor3f(0.0, 0.0, 0.0)
    glPushMatrix()
    glTranslatef(0, -8, 5)
    glScalef(20, 3, 3)
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()


    glPushMatrix()
    glTranslatef(30, 0, 0)
    glColor3f(0.1, 0.1, 0.1)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 8, 30, 8, 4)
    glPopMatrix()

    glPopMatrix()

def spawn_boss():
    global boss_active, boss_pos, boss_health, boss_angle


    for room in rooms:
        room_x, room_y, width, depth = room

        if (room_x <= player_pos[0] <= room_x + width and
            room_y <= player_pos[1] <= room_y + depth):
            boss_pos[0] = room_x + width/2
            boss_pos[1] = room_y + depth/2
            break
    else:

        if (room4_x <= player_pos[0] <= room4_x + room4_width and
            room4_y <= player_pos[1] <= room4_y + room4_depth):
            boss_pos[0] = room4_x + room4_width/2
            boss_pos[1] = room4_y + room4_depth/2

    boss_health = boss_max_health
    boss_angle = random.randint(0, 359)
    boss_active = True

def boss_shoot():
    global boss_bullets


    shoot_angle = random.randint(0, 359)
    rad = math.radians(shoot_angle)


    boss_bullets.append([boss_pos[0], boss_pos[1], shoot_angle, BOSS_BULLET_LIFE])

def update_boss_bullets():
    global boss_bullets, player_health, player_dead

    keep_list = []
    for b in boss_bullets:
        x, y, angle, life = b
        rad = math.radians(angle + 90)
        x = x + BOSS_BULLET_SPEED * math.cos(rad)
        y = y + BOSS_BULLET_SPEED * math.sin(rad)
        life = life - 1

        if math.hypot(player_pos[0] - x, player_pos[1] - y) < 30:
            player_health -= 20
            if player_health <= 0:
                player_dead = True
        else:
            if life > 0:
                keep_list.append([x, y, angle, life])

    boss_bullets = keep_list

def draw_boss_bullets():
    glColor3f(*BOSS_BULLET_COLOR)
    for x, y, angle, life in boss_bullets:
        glPushMatrix()
        glTranslatef(x, y, BOSS_BULLET_SIZE/2)
        glutSolidSphere(BOSS_BULLET_SIZE/2, 8, 8)
        glPopMatrix()

def update_bullets():
    global bullets, enemies, missed_bullets, player_dead, boss_health, boss_defeated
    global score, explosive_drums, explosion_effects, orange_screen_flag, player_health

    keep_list = []
    for i in range(len(bullets)):
        x, y, angle, life = bullets[i]
        rad = math.radians(angle + 90)
        x += BULLET_SPEED * math.cos(rad)
        y += BULLET_SPEED * math.sin(rad)
        life -= 1

        hit_enemy = False
        hit_boss = False
        exploded = False
        hit_crate = False


        for j in range(len(enemies)-1, -1, -1):
            if len(enemies[j]) >= 6:  # Check if enemy has health info
                enemy_x, enemy_y, enemy_type, enemy_scale, enemy_angle, enemy_health = enemies[j]
                if math.hypot(enemy_x - x, enemy_y - y) < 30 * enemy_scale:
                    # Reduce enemy health by 1
                    enemy_health -= 1

                    if enemy_health <= 0:
                        enemies.pop(j)
                        score += 1
                    else:
                        enemies[j] = (enemy_x, enemy_y, enemy_type, enemy_scale, enemy_angle, enemy_health)

                    hit_enemy = True
                    break
            elif len(enemies[j]) >= 4:
                enemy_x, enemy_y, enemy_type, enemy_scale = enemies[j][:4]
                if math.hypot(enemy_x - x, enemy_y - y) < 30 * enemy_scale:
                    if enemy_type == 'red':
                        enemy_health = 10
                    elif enemy_type == 'purple':
                        enemy_health = 5
                    else:
                        enemy_health = 2

                    if enemy_health <= 0:
                        enemies.pop(j)
                        score += 1
                    else:
                        enemy_angle = enemies[j][4] if len(enemies[j]) > 4 else 0
                        enemies[j] = (enemy_x, enemy_y, enemy_type, enemy_scale, enemy_angle, enemy_health)

                    hit_enemy = True
                    break

        if boss_active and math.hypot(boss_pos[0] - x, boss_pos[1] - y) < 50 * boss_size:
            boss_health -= 1
            if boss_health <= 0:
                boss_defeated = True
                score += 100
            hit_boss = True


        for k in range(len(explosive_drums)-1, -1, -1):
            if math.hypot(explosive_drums[k][0] - x, explosive_drums[k][1] - y) < 40:

                explosion_effects.append([explosive_drums[k][0], explosive_drums[k][1], EXPLOSION_DURATION])

                player_distance = math.hypot(player_pos[0] - explosive_drums[k][0],
                                            player_pos[1] - explosive_drums[k][1])

                if player_distance < 100:
                    player_health -= 20
                    orange_screen_flag = True
                    if player_health <= 0:
                        player_dead = True


                for e in range(len(enemies)-1, -1, -1):
                    enemy_x, enemy_y = enemies[e][:2]
                    enemy_distance = math.hypot(enemy_x - explosive_drums[k][0],
                                              enemy_y - explosive_drums[k][1])
                    if enemy_distance < 300:

                        enemy_type = enemies[e][2] if len(enemies[e]) > 2 else 'red'

                        enemies.pop(e)
                        score += 1

                        new_x = random.randint(-2000, 2000)
                        new_y = random.randint(-2000, 2000)

                        while math.hypot(player_pos[0] - new_x, player_pos[1] - new_y) < 300:
                            new_x = random.randint(-2000, 2000)
                            new_y = random.randint(-2000, 2000)

                        if enemy_type == 'red':
                            enemy_health = 10
                        elif enemy_type == 'purple':
                            enemy_health = 5
                        else:
                            enemy_health = 2

                        enemies.append((new_x, new_y, enemy_type, 1.0, random.randint(0, 359), enemy_health))


                explosive_drums.pop(k)
                exploded = True
                break


        for c_idx in range(len(crates)-1, -1, -1):
            if math.hypot(crates[c_idx][0] - x, crates[c_idx][1] - y) < 60:
                crates.pop(c_idx)
                hit_crate = True
                break


        if life > 0 and not hit_enemy and not hit_boss and not exploded and not hit_crate:
            keep_list.append([x, y, angle, life])
        else:
            if not hit_enemy and not hit_boss and not exploded and not hit_crate:
                missed_bullets += 1

    bullets = keep_list

def is_player_in_room():
    global player_pos, rooms

    for room in rooms:
        room_x, room_y, width, depth = room

        if (room_x <= player_pos[0] <= room_x + width and
            room_y <= player_pos[1] <= room_y + depth):
            return True


    if (room4_x <= player_pos[0] <= room4_x + room4_width and
        room4_y <= player_pos[1] <= room4_y + room4_depth):
        return True

    return False

def is_in_water(x, y):
    tile_size = 50
    tile_x = (x // tile_size) * tile_size
    tile_y = (y // tile_size) * tile_size
    return (tile_x, tile_y) in terrain_map and terrain_map[(tile_x, tile_y)] == 'water'

def spawn_ammo_pack():
    min_distance = 5000

    attempts = 0
    while attempts < 100:
        attempts += 1
        x = random.randint(-GRID_LENGTH * 5, GRID_LENGTH * 5)
        y = random.randint(-GRID_LENGTH * 5, GRID_LENGTH * 5)

        if is_in_water(x, y):
            continue

        if not all(math.hypot(x - ax, y - ay) >= min_distance for ax, ay in ammo_packs):
            continue

        if math.hypot(x, y) < 200:
            continue

        return (x, y)

    return (random.randint(-GRID_LENGTH * 5, GRID_LENGTH * 5),
            random.randint(-GRID_LENGTH * 5, GRID_LENGTH * 5))

def initialize_ammo_packs():
    global ammo_packs
    ammo_packs.clear()
    for _ in range(3):
        ammo_packs.append(spawn_ammo_pack())

def draw_ammo_pack(x, y, z= 70, radius= 15):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0.0, 0.3, 1.0)  # Blue color
    glutSolidSphere(radius, 20, 20)

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    glVertex3f(-radius/2, 0, radius/2)
    glVertex3f(radius/2, 0, radius/2)
    glVertex3f(0, -radius/2, radius/2)
    glVertex3f(0, radius/2, radius/2)
    glEnd()

    glPopMatrix()

def is_colliding_with_objects(x, y):
    if player_pos[1] >= 3400 or player_pos[1] <= -3400 or player_pos[0] <= -3400 or player_pos[0] >= 3400:
        print("collision")
        return True

    for i in crates:
        if abs(x - i[0] + 10) < 50 and abs(y - i[1] + 10) < 50:
            print("collision")
            return True
    for room in rooms:
        room_x, room_y, room_w, room_d = room
        door_width = 200
        door_start_x = room_x + room_w - door_width
        door_end_x = room_x + room_w
        wall_thickness = 20

        if (room_y <= y <= room_y + room_d and
                room_x - wall_thickness <= x <= room_x + wall_thickness):
            print("collision with left wall")
            return True

        if (room_y <= y <= room_y + room_d and
                room_x + room_w - wall_thickness <= x <= room_x + room_w + wall_thickness):
            print("collision with right wall")
            return True

        if (room_x <= x <= room_x + room_w and
                room_y + room_d - wall_thickness <= y <= room_y + room_d + wall_thickness):
            print("collision with back wall")
            return True

        if (room_x <= x <= room_x + room_w and
                room_y - wall_thickness <= y <= room_y + wall_thickness):
            if not (door_start_x <= x <= door_end_x):
                print("collision with front wall")
                return True
            else:
                print("passing through door")

    return False


def spawn_single_enemy():
    enemy_types = [
        {'type': 'red', 'scale': 2.0, 'health': 10},
        {'type': 'purple', 'scale': 0.7, 'health': 2},
        {'type': 'yellow', 'scale': 1.0, 'health': 5},
    ]
    enemy_type = random.choice(enemy_types)

    x = random.randint(-GRID_LENGTH - 500, GRID_LENGTH + 500)
    y = random.randint(-GRID_LENGTH - 500, GRID_LENGTH + 500)
    initial_angle = random.randint(0, 359)

    tile_size = 50
    tile_x = (x // tile_size) * tile_size
    tile_y = (y // tile_size) * tile_size

    if (tile_x, tile_y) in terrain_map and terrain_map[(tile_x, tile_y)] == 'water':
        x = random.randint(-GRID_LENGTH, GRID_LENGTH)
        y = random.randint(-GRID_LENGTH, GRID_LENGTH)

    enemies.append((x, y, enemy_type['type'], enemy_type['scale'], initial_angle, enemy_type['health']))


def check_enemy_respawn():

    global enemy_respawn_timer

    if len(enemies) < MAX_ENEMIES:
        enemy_respawn_timer -= 1

        if enemy_respawn_timer <= 0:
            spawn_single_enemy()
            enemy_respawn_timer = ENEMY_RESPAWN_DELAY


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


def spawn_enemies():
    global enemies
    enemies = []

    enemy_types = [
        {'type': 'red', 'count': 3, 'scale': 2.0, 'health': 10},
        {'type': 'purple', 'count': 5, 'scale': 0.7, 'health': 2},
        {'type': 'yellow', 'count': 3, 'scale': 1.0, 'health': 5},
    ]


    for enemy_type in enemy_types:
        for i in range(enemy_type['count']):

            x = random.randint(-GRID_LENGTH - 500, GRID_LENGTH + 500)
            y = random.randint(-GRID_LENGTH - 500, GRID_LENGTH + 500)
            initial_angle = random.randint(0, 359)


            tile_size = 50
            tile_x = (x // tile_size) * tile_size
            tile_y = (y // tile_size) * tile_size


            if (tile_x, tile_y) in terrain_map and terrain_map[(tile_x, tile_y)] == 'water':
                x = random.randint(-GRID_LENGTH, GRID_LENGTH)
                y = random.randint(-GRID_LENGTH, GRID_LENGTH)


            enemies.append((x, y, enemy_type['type'], enemy_type['scale'], initial_angle, enemy_type['health']))



def move_enemies_towards_player():
    global player_health, player_dead, enemies

    if player_health == 0:
        return

    COLLISION_DIST = 35
    ROTATION_SPEED = 3

    for i in range(len(enemies)):
        ex, ey = enemies[i][0], enemies[i][1]
        enemy_type = enemies[i][2]
        enemy_scale = enemies[i][3]

        enemy_angle = enemies[i][4] if len(enemies[i]) > 4 else 0

        enemy_health = enemies[i][5] if len(enemies[i]) > 5 else 1

        px, py = player_pos
        dx, dy = px - ex, py - ey
        dist = math.hypot(dx, dy)

        target_angle = (math.degrees(math.atan2(dy, dx)) - 90) % 360

        angle_diff = (target_angle - enemy_angle) % 360
        if angle_diff > 180:
            angle_diff -= 360

        if abs(angle_diff) > ROTATION_SPEED:
            if angle_diff > 0:
                enemy_angle = (enemy_angle + ROTATION_SPEED) % 360
            else:
                enemy_angle = (enemy_angle - ROTATION_SPEED) % 360
        else:
            enemy_angle = target_angle


        move_speed = 0
        if abs(angle_diff) < 30:
            move_speed = enemy_speed

        rad = math.radians(enemy_angle + 90)
        move_x = math.cos(rad) * move_speed
        move_y = math.sin(rad) * move_speed

        ex += move_x
        ey += move_y

        if dist < COLLISION_DIST * enemy_scale and not player_dead:
            player_health -= 1
            if player_health <= 0:
                player_dead = True

        if len(enemies[i]) > 5:
            enemies[i] = (ex, ey, enemy_type, enemy_scale, enemy_angle, enemy_health)
        else:
            enemies[i] = (ex, ey, enemy_type, enemy_scale, enemy_angle)


def spawn_player_bullet():
    global player_pos, player_angle

    rad = math.radians(player_angle + 90)
    dir_x = math.cos(rad)
    dir_y = math.sin(rad)


    right_x = math.cos(rad + math.pi / 2)
    right_y = math.sin(rad + math.pi / 2)


    base_x = player_pos[0]
    base_y = player_pos[1]


    arm_offset = 19
    arm_length = 19
    hand_offset = 6
    gun_barrel_y = 20


    gun_x = base_x + right_x * arm_offset
    gun_y = base_y + right_y * arm_offset


    gun_x += -right_x * arm_length
    gun_y += -right_y * arm_length


    gun_x += -right_x * hand_offset
    gun_y += -right_y * hand_offset


    gun_x += dir_x * gun_barrel_y
    gun_y += dir_y * gun_barrel_y


    bullets.append([gun_x, gun_y, player_angle, BULLET_LIFE])


def shrink_expand():
    global enemy_scale_factor, enemy_scale_direction, player_angle
    global cheat_cooldown
    enemy_scale_factor += 0.005 * enemy_scale_direction
    if enemy_scale_factor >= 1.2:
        enemy_scale_factor = 1.2
        enemy_scale_direction = -1
    elif enemy_scale_factor <= 0.8:
        enemy_scale_factor = 0.8
        enemy_scale_direction = 1

def animate():
    global enemy_scale_factor, enemy_scale_direction, fire_cooldown, enemy_respawn_timer
    global handgun_ammo, automatic_ammo, current_weapon, player_in_room, enemies
    global boss_active, boss_fire_cooldown, boss_angle, boss_bullets, boss_pos, bullets, boss_defeated
    global ultimate_active, ultimate_timer, ultimate_cooldown, explosion_effects, orange_screen_flag


    if player_dead or boss_defeated:
        glutPostRedisplay()
        return


    for effect in explosion_effects[:]:
        effect[2] -= 1
        if effect[2] <= 0:
            explosion_effects.remove(effect)


    if ultimate_active:
        ultimate_timer -= 1
        if ultimate_timer <= 0:
            ultimate_active = False
            handgun_ammo = 200
            automatic_ammo = 100


    if ultimate_cooldown > 0:
        ultimate_cooldown -= 1

    if player_in_room and not boss_active and score >= 40:
        spawn_boss()


    if not player_in_room and boss_active:
        boss_active = False
        boss_bullets.clear()


    if boss_active:

        dx = player_pos[0] - boss_pos[0]
        dy = player_pos[1] - boss_pos[1]
        boss_angle = math.degrees(math.atan2(dy, dx))


        boss_fire_cooldown -= 1
        if boss_fire_cooldown <= 0:
            boss_shoot()
            boss_fire_cooldown = boss_fire_rate

    update_boss_bullets()


    if not player_in_room and not player_dead:
        check_enemy_respawn()


    if player_in_room and len(enemies) > 0:
        enemies.clear()

    if left_mouse_pressed and not player_dead and fire_cooldown <= 0:
        if current_weapon == 1 and handgun_ammo > 0:
            spawn_player_bullet()

            if not ultimate_active:
                handgun_ammo -= 1

            fire_rate_multiplier = 0.3 if ultimate_active else 1
            fire_cooldown = handgun_fire_rate * fire_rate_multiplier
        elif current_weapon == 2 and automatic_ammo > 0:
            spawn_player_bullet()

            if not ultimate_active:
                automatic_ammo -= 1

            fire_rate_multiplier = 0.3 if ultimate_active else 1
            fire_cooldown = automatic_fire_rate * fire_rate_multiplier


    if fire_cooldown > 0:
        fire_cooldown -= 1


    if orange_screen_flag:
        orange_screen_flag = False


    shrink_expand()
    process_movement()


    if not player_in_room:
        move_enemies_towards_player()

    update_bullets()
    glutPostRedisplay()

def draw_text(x, y, text, font=GLUT_BITMAP_9_BY_15):
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


def setupCamera():
    global player_pos, player_angle, cam_orbit_angle

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1000 / 800, 0.1, 15000)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    cam_distance = 150
    cam_height = 120


    combined_angle = player_angle + 90 + cam_orbit_angle
    rad = math.radians(combined_angle)

    camera_x = player_pos[0] - math.cos(rad) * cam_distance
    camera_y = player_pos[1] - math.sin(rad) * cam_distance
    camera_z = HEAD_HEIGHT + cam_height

    look_x = player_pos[0]
    look_y = player_pos[1]
    look_z = HEAD_HEIGHT

    # Set up the camera
    gluLookAt(camera_x, camera_y, camera_z,
              look_x, look_y, look_z,
              0, 0, 1)




def draw_sphere(x, y, z, radius, color):
    if color == "green":
        glPushMatrix()
        glTranslatef(x, y, z)

        glColor3f(0.0, 1.0, 0.0)

        gluSphere(gluNewQuadric(), radius, 20, 20)

        glPopMatrix()

    elif color == "gold":
        glPushMatrix()
        glTranslatef(x, y, z)

        glColor3f(1.0, 0.84, 0.0)

        gluSphere(gluNewQuadric(), radius, 20, 20)

        glPopMatrix()


def draw_room(x, y, width, depth, height, door_width=100, door_height=150):

    glColor3f(0.5, 0.5, 0.5)
    room_size = 500

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


    glColor3f(1, 1, 1)


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


    glColor3f(1, 1, 1)


    glBegin(GL_QUADS)

    glVertex3f(x + width - door_width, y, 0)

    glVertex3f(x + width, y, 0)

    glVertex3f(x + width, y, door_height)

    glVertex3f(x + width - door_width, y, door_height)
    glEnd()


def draw_crate(x, y, z=0):
    crate_size = 100


    glColor3f(199 / 255, 157 / 255, 122 / 255)

    glPushMatrix()
    glTranslatef(x, y, z)


    glBegin(GL_QUADS)


    glVertex3f(-crate_size / 2, -crate_size / 2, crate_size / 2)
    glVertex3f(crate_size / 2, -crate_size / 2, crate_size / 2)
    glVertex3f(crate_size / 2, crate_size / 2, crate_size / 2)
    glVertex3f(-crate_size / 2, crate_size / 2, crate_size / 2)


    glVertex3f(-crate_size / 2, -crate_size / 2, -crate_size / 2)
    glVertex3f(crate_size / 2, -crate_size / 2, -crate_size / 2)
    glVertex3f(crate_size / 2, crate_size / 2, -crate_size / 2)
    glVertex3f(-crate_size / 2, crate_size / 2, -crate_size / 2)


    glVertex3f(-crate_size / 2, -crate_size / 2, crate_size / 2)
    glVertex3f(-crate_size / 2, -crate_size / 2, -crate_size / 2)
    glVertex3f(-crate_size / 2, crate_size / 2, -crate_size / 2)
    glVertex3f(-crate_size / 2, crate_size / 2, crate_size / 2)


    glVertex3f(crate_size / 2, -crate_size / 2, crate_size / 2)
    glVertex3f(crate_size / 2, -crate_size / 2, -crate_size / 2)
    glVertex3f(crate_size / 2, crate_size / 2, -crate_size / 2)
    glVertex3f(crate_size / 2, crate_size / 2, crate_size / 2)


    glVertex3f(-crate_size / 2, crate_size / 2, crate_size / 2)
    glVertex3f(crate_size / 2, crate_size / 2, crate_size / 2)
    glVertex3f(crate_size / 2, crate_size / 2, -crate_size / 2)
    glVertex3f(-crate_size / 2, crate_size / 2, -crate_size / 2)


    glVertex3f(-crate_size / 2, -crate_size / 2, crate_size / 2)
    glVertex3f(crate_size / 2, -crate_size / 2, crate_size / 2)
    glVertex3f(crate_size / 2, -crate_size / 2, -crate_size / 2)
    glVertex3f(-crate_size / 2, -crate_size / 2, -crate_size / 2)

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

    draw_room(-1500, -1100, 900, 900, 350, door_width=200, door_height=300)


    draw_room(800, -1100, 900, 900, 350, door_width=200, door_height=300)


    draw_room(-2200, 1800, 1500, 1500, 350, door_width=200, door_height=300)




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
                terrain_type = 'mud'  # Smooth mud road
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


def draw_enemy(enemy_type='red', enemy_scale=1.0, angle=0):

    if enemy_type == 'red':
        body_color = (1.0, 0.0, 0.0)
    elif enemy_type == 'purple':
        body_color = (0.8, 0.0, 0.8)
    elif enemy_type == 'yellow':
        body_color = (1.0, 1.0, 0.0)
    else:
        body_color = (1.0, 0.0, 0.0)

    final_scale = enemy_scale * enemy_scale_factor

    glPushMatrix()
    glRotatef(angle, 0, 0, 1)
    glScalef(final_scale, final_scale, final_scale)


    leg_width = 12
    leg_height = 30
    leg_spacing = 3


    glPushMatrix()
    glColor3f(*body_color)
    glTranslatef(-leg_width / 2 - leg_spacing / 2, 0, 0)
    glScalef(leg_width, 10, leg_height)
    glutSolidCube(1)
    glPopMatrix()

    # Right Leg
    glPushMatrix()
    glColor3f(*body_color)
    glTranslatef(leg_width / 2 + leg_spacing / 2, 0, 0)
    glScalef(leg_width, 10, leg_height)
    glutSolidCube(1)
    glPopMatrix()

    # Hip connector
    glPushMatrix()
    glColor3f(*body_color)
    glTranslatef(0, 0, leg_height)
    glScalef(leg_width * 2 + leg_spacing, 10, 5)
    glutSolidCube(1)
    glPopMatrix()

    # Torso (LEGO minifigure style)
    torso_height = 36
    glPushMatrix()
    glColor3f(*body_color)
    glTranslatef(0, 0, leg_height + torso_height / 2)

    # Main torso block
    glPushMatrix()
    glScalef(27, 15, torso_height)
    glutSolidCube(1)
    glPopMatrix()

    # Evil logo on chest
    glPushMatrix()
    glColor3f(0.0, 0.0, 0.0)  # Black logo
    glTranslatef(0, 7.6, 0)
    glScalef(12, 0.5, 12)
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()


    glPushMatrix()
    glColor3f(1, 0.8, 0.6)  # Skin color
    glTranslatef(0, 0, leg_height + torso_height + 10)


    gluCylinder(gluNewQuadric(), 15, 15, 17, 20, 5)
    glTranslatef(0, 0, 17)
    glutSolidSphere(15, 20, 20)


    glColor3f(0, 0, 0)


    glPushMatrix()
    glTranslatef(-5, 13, -5)  # Left eyebrow
    glRotatef(-30, 0, 0, 1)
    glScalef(7, 1.5, 1.5)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glTranslatef(5, 13, -5)  # Right eyebrow
    glRotatef(30, 0, 0, 1)
    glScalef(7, 1.5, 1.5)
    glutSolidCube(1)
    glPopMatrix()


    glPushMatrix()
    glTranslatef(5, 13, -9)
    glutSolidSphere(2.5, 8, 8)
    glTranslatef(-10, 0, 0)
    glutSolidSphere(2.5, 8, 8)
    glPopMatrix()

    # Frown (angry mouth)
    glPushMatrix()
    glTranslatef(0, 10, -15)
    glRotatef(180, 0, 0, 1)
    glScalef(10, 1.5, 1.5)
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()


    arm_length = 19


    glPushMatrix()
    glColor3f(*body_color)
    glTranslatef(-19, 0, leg_height + torso_height - 6)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 5, arm_length, 8, 8)

    # Left hand
    glColor3f(1, 0.8, 0.6)
    glTranslatef(0, 0, arm_length)
    glutSolidSphere(6, 8, 8)
    glPopMatrix()

    # Right arm
    glPushMatrix()
    glColor3f(*body_color)
    glTranslatef(19, 0, leg_height + torso_height - 6)
    glRotatef(-90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 5, arm_length, 8, 8)

    # Right hand
    glColor3f(1, 0.8, 0.6)
    glTranslatef(0, 0, arm_length)
    glutSolidSphere(6, 8, 8)
    glPopMatrix()

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


    leg_submersion = 20 if player_in_water else 0

    if player_dead:
        glRotatef(-90, 1, 0, 0)

    glTranslatef(0, -25, -leg_submersion)


    # Legs
    leg_width = 12
    leg_height = 30
    leg_spacing = 3


    glPushMatrix()
    glColor3f(0, 0, 0.7)
    glTranslatef(-leg_width / 2 - leg_spacing / 2, 0, 0)
    glScalef(leg_width, 10, leg_height)
    glutSolidCube(1)
    glPopMatrix()


    glPushMatrix()
    glColor3f(0, 0, 0.7)
    glTranslatef(leg_width / 2 + leg_spacing / 2, 0, 0)
    glScalef(leg_width, 10, leg_height)
    glutSolidCube(1)
    glPopMatrix()


    glPushMatrix()
    glColor3f(0, 0, 0.8)
    glTranslatef(0, 0, leg_height)
    glScalef(leg_width * 2 + leg_spacing, 10, 5)
    glutSolidCube(1)
    glPopMatrix()


    torso_height = 36
    glPushMatrix()
    glColor3f(0, 0, 1)  # Blue torso
    glTranslatef(0, 0, leg_height + torso_height / 2)


    glPushMatrix()
    glScalef(27, 15, torso_height)
    glutSolidCube(1)
    glPopMatrix()


    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslatef(0, 7.6, 0)
    glScalef(12, 0.5, 12)
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()


    glPushMatrix()
    glColor3f(1, 0.8, 0.6)
    glTranslatef(0, 0, leg_height + torso_height + 10)


    gluCylinder(gluNewQuadric(), 15, 15, 17, 20, 5)
    glTranslatef(0, 0, 17)
    glutSolidSphere(15, 20, 20)

    # Face features
    glColor3f(0, 0, 0)
    # Eyes
    glPushMatrix()
    glTranslatef(5, 13, -9)
    glutSolidSphere(2.5, 8, 8)
    glTranslatef(-10, 0, 0)
    glutSolidSphere(2.5, 8, 8)
    glPopMatrix()

    # Smile
    glPushMatrix()
    glTranslatef(0, 10, -15)
    glScalef(10, 1.5, 1.5)
    glutSolidCube(1)
    glPopMatrix()

    # Add hair to the head
    glColor3f(0.4, 0.2, 0.0)


    glPushMatrix()
    glTranslatef(0, 0, 5)
    glScalef(1.1, 1.1, 0.5)
    glutSolidSphere(15, 20, 20)
    glPopMatrix()


    glPushMatrix()
    glTranslatef(0, 14, -2)
    glRotatef(30, 1, 0, 0)
    glScalef(20, 4, 8)
    glutSolidCube(1)
    glPopMatrix()


    glPushMatrix()
    glTranslatef(-14, 0, -5)
    glScalef(5, 14, 15)
    glutSolidCube(1)
    glPopMatrix()


    glPushMatrix()
    glTranslatef(14, 0, -5)
    glScalef(5, 14, 15)
    glutSolidCube(1)
    glPopMatrix()

    glPopMatrix()


    arm_length = 19


    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(-19, 0, leg_height + torso_height - 6)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 5, arm_length, 8, 8)


    glColor3f(1, 1, 0)
    glTranslatef(0, 0, arm_length)
    glutSolidSphere(6, 8, 8)
    glPopMatrix()


    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(19, 0, leg_height + torso_height - 6)
    glRotatef(-90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 5, 5, arm_length, 8, 8)


    glColor3f(1, 1, 0)
    glTranslatef(0, 0, arm_length)
    glutSolidSphere(6, 8, 8)


    glPushMatrix()
    glColor3f(0.2, 0.2, 0.2)
    glTranslatef(6, 10, 0)


    glPushMatrix()
    glScalef(4, 12, 4)
    glutSolidCube(1)
    glPopMatrix()


    glPushMatrix()
    glTranslatef(0, 10, 0)
    glScalef(6, 18, 6)
    glutSolidCube(1)
    glPopMatrix()

    # Gun sight
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslatef(0, 20, 0)
    glutSolidSphere(2, 8, 8)
    glPopMatrix()

    glPopMatrix()

    glPopMatrix()

    glPopMatrix()


def if_dead():
    global cheat_cooldown, player_pos, player_angle, player_health, player_dead
    global missed_bullets, score, handgun_ammo, automatic_ammo
    global boss_active, boss_bullets, boss_defeated

    player_dead = False
    player_pos[:] = [0, 0]
    player_health = 7
    player_key = 0
    missed_bullets = 0
    score = 0
    handgun_ammo = 300
    automatic_ammo = 100
    bullets.clear()
    cheat_cooldown = 0
    spawn_enemies()
    initialize_ammo_packs()
    initialize_health_packs()
    boss_active = False
    boss_bullets = []
    boss_defeated = False
    return


def keyboardListener(key, x, y):
    global player_pos, player_angle, player_health, player_dead, orange_screen_flag
    global missed_bullets, score, key_states, cam_orbit_angle
    global current_weapon, boss_defeated, ultimate_active, ultimate_timer
    global handgun_ammo, automatic_ammo, fire_cooldown, ultimate_cooldown

    if boss_defeated:
        return

    if key == b'u' and not ultimate_active and not player_dead and ultimate_cooldown <= 0:
        ultimate_active = True
        ultimate_timer = ULTIMATE_DURATION
        handgun_ammo = 999
        automatic_ammo = 999
        ultimate_cooldown = ULTIMATE_COOLDOWN
    if key == b'1':
        current_weapon = 1
    elif key == b'2':
        current_weapon = 2

    elif key == b'q':
        cam_orbit_angle -= 8
    elif key == b'e':
        cam_orbit_angle += 8

    if player_dead:
        if key in (b'r', b'R'):
            if_dead()
        return

    if key in (b'q', b'Q') and orange_screen_flag:
        orange_screen_flag = False


    if key in key_states:
        key_states[key] = True

    glutPostRedisplay()


def keyboardUpListener(key, x, y):
    global key_states, boss_defeated

    if boss_defeated:
        return

    if key in key_states:
        key_states[key] = False

    glutPostRedisplay()


def process_movement():
    global player_pos, player_angle, orange_screen_flag, previous_location, player_in_water
    global player_in_room, boss_defeated, ultimate_active, normal_move_speed

    if boss_defeated:
        return

    move_speed = normal_move_speed * 2 if ultimate_active else normal_move_speed

    # Handle rotation
    if key_states[b'a'] and not key_states[b'd'] and not key_states[b'w'] and not key_states[b's']:
        player_angle = (player_angle + 8) % 360
    elif key_states[b'd'] and not key_states[b'a'] and not key_states[b'w'] and not key_states[b's']:
        player_angle = (player_angle - 8) % 360

    forward_angle = player_angle + 90
    right_angle = player_angle

    move_angle = None
    if key_states[b'w'] and not key_states[b's']:
        if key_states[b'a'] and not key_states[b'd']:

            move_angle = forward_angle + 45
        elif key_states[b'd'] and not key_states[b'a']:

            move_angle = forward_angle - 45
        else:
            # Forward
            move_angle = forward_angle
    elif key_states[b's'] and not key_states[b'w']:
        if key_states[b'a'] and not key_states[b'd']:
            move_angle = forward_angle + 135
        elif key_states[b'd'] and not key_states[b'a']:
            move_angle = forward_angle - 135
        else:
            # Backward
            move_angle = forward_angle - 180

    if move_angle is not None:
        rad = math.radians(move_angle)
        dx = math.cos(rad) * move_speed
        dy = math.sin(rad) * move_speed

        new_x = player_pos[0] + dx
        new_y = player_pos[1] + dy

        if not is_colliding_with_objects(new_x, new_y):
            player_pos[0] = new_x
            player_pos[1] = new_y


            if len(previous_location) > 100:
                previous_location.pop(0)
            previous_location.append((player_pos[0], player_pos[1]))
            orange_screen_flag = False

    player_in_room = is_player_in_room()
    player_in_water = is_in_water(player_pos[0], player_pos[1])



def mouseListener(button, state, x, y):
    global left_mouse_pressed, handgun_ammo, automatic_ammo, boss_defeated

    if boss_defeated:
        return

    if handgun_ammo>0 and automatic_ammo>0:
        if button == GLUT_LEFT_BUTTON:
            if state == GLUT_DOWN:
                left_mouse_pressed = True
                spawn_player_bullet()
            else:
                left_mouse_pressed = False

    glutPostRedisplay()

def showScreen():
    global player_pos, player_angle, player_health, player_dead, orange_screen_flag
    global score, missed_bullets, key_states, player_key, player_in_room
    global handgun_ammo, automatic_ammo, current_weapon, enemies, boss_defeated
    global ultimate_active, ultimate_timer, ultimate_cooldown

    rotation_angle = 0
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    draw_bullets()

    glPushMatrix()
    glRotatef(rotation_angle, 0.0, 1.0, 0.0)
    glPopMatrix()

    rotation_angle += 0.1
    if rotation_angle > 360:
        rotation_angle = 0

    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], 1)
    glRotatef(player_angle, 0, 0, 1)
    draw_player()
    glPopMatrix()


    for x, y, timer in explosion_effects:
        glColor4f(1.0, 0.5, 0.0, 0.7)
        radius = 100  # Explosion radius

        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(x, y, 2)
        for i in range(37):
            angle = math.radians(i * 10)
            glVertex3f(x + radius * math.cos(angle), y + radius * math.sin(angle), 2)
        glEnd()

    draw_walls()


    if player_in_room and boss_active:

        glPushMatrix()
        glTranslatef(boss_pos[0], boss_pos[1], 100)
        glRotatef(boss_angle, 0, 0, 1)

        draw_boss(0, 0)
        glPopMatrix()


        draw_boss_bullets()


        draw_text(10, 650, f"Boss Health: {boss_health}/{boss_max_health}")

    for x in explosive_drums:
        drum_pos_x = x[0]
        drum_pos_y = x[1]
        drum_pos_z = 0
        draw_explosive_drum(drum_pos_x, drum_pos_y, drum_pos_z)

    for c in crates:
        c_pos_x = c[0]
        c_pos_y = c[1]
        c_pos_z = 50
        draw_crate(c_pos_x, c_pos_y, c_pos_z)


    for h in range(len(health_packs)):
        if health_packs[h] is None:
            continue

        if abs(player_pos[0] - health_packs[h][0]) < 20 and abs(player_pos[1] - health_packs[h][1]) < 20:
            player_health = 100
            health_packs[h] = None
        else:

            draw_health_pack(health_packs[h][0], health_packs[h][1])


    for a in range(len(ammo_packs)):
        if abs(player_pos[0] - ammo_packs[a][0]) < 15 and abs(player_pos[1] - ammo_packs[a][1]) < 15:
            handgun_ammo = 300
            automatic_ammo = 100
            ammo_packs[a] = spawn_ammo_pack()
        else:
            draw_ammo_pack(ammo_packs[a][0], ammo_packs[a][1])


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
    for i in range(10):
        draw_tree(val_x, g_y, 0)
        g_y += 300
    for i in range(10):
        draw_tree(val_x, val_y, 0)
        val_y -= 300
    for i in range(10):
        draw_tree(c_x, c_y, 0)
        c_y -= 300

    # Orange screen effect when hit
    if orange_screen_flag:
        glColor3f(1.0, 0.647, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(-5000, -5000)
        glVertex2f(5000, -5000)
        glVertex2f(5000, 5000)
        glVertex2f(-5000, 5000)
        glEnd()


    for (i, j), terrain_type in terrain_map.items():
        if terrain_type == 'grass':
            glColor3f(0.0, 0.6, 0.0)  # Green
        elif terrain_type == 'mud':
            glColor3f(0.55, 0.27, 0.07)  # Brown
        elif terrain_type == 'water':
            glColor3f(0.0, 0.4, 0.7)  # Blue

        glBegin(GL_QUADS)
        glVertex3f(i, j, 0)
        glVertex3f(i + tile_size, j, 0)
        glVertex3f(i + tile_size, j + tile_size, 0)
        glVertex3f(i, j + tile_size, 0)
        glEnd()


    if not player_in_room:
        for enemy_pos in enemies:
            if player_dead:
                break

            if len(enemy_pos) < 5:
                ex, ey, enemy_type, enemy_scale = enemy_pos
                enemy_angle = 0
            else:
                ex, ey, enemy_type, enemy_scale = enemy_pos[:4]
                enemy_angle = enemy_pos[4] if len(enemy_pos) > 4 else 0

            glPushMatrix()
            glTranslatef(ex, ey, 0)
            draw_enemy(enemy_type, enemy_scale, enemy_angle)
            glPopMatrix()

    # Draw UI
    draw_text(10, 770, f"Player Life Remaining: {player_health}")

    if player_dead:
        draw_text(10, 740, "GAME OVER!!! press R to restart")
        draw_text(10, 710, " ")
    elif boss_defeated:
        draw_text(300, 400, "Yeee! you have defeated the boss, Game is over!!")
    else:
        draw_text(10, 740, f"Game Score: {score}")
        draw_text(10, 710, f"Player Bullet Missed: {missed_bullets}")

        if score >= 40:
            draw_text(10, 600, "You have unlocked the boss, get ready to fight!")

        # Display weapon info
        if current_weapon == 1:
            draw_text(10, 680, f"Weapon: Handgun | Ammo: {handgun_ammo}")
        else:
            draw_text(10, 680, f"Weapon: Automatic | Ammo: {automatic_ammo}")

        # Display ultimate ability status
        if ultimate_active:
            draw_text(10, 620, f"ULTIMATE ACTIVE! {ultimate_timer // 60}s remaining")
        elif ultimate_cooldown > 0:
            draw_text(10, 620, f"Ultimate cooldown: {ultimate_cooldown // 60}s")
        else:
            draw_text(10, 620, "Ultimate ready! Press 'U'")

    glutSwapBuffers()

def main():
    global enemy_respawn_timer
    glutInit()
    generate_terrain()
    initialize_ammo_packs()
    initialize_health_packs()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(300, 100)
    glutCreateWindow(b"Boom!!")
    glEnable(GL_DEPTH_TEST)
    spawn_enemies()

    enemy_respawn_timer = ENEMY_RESPAWN_DELAY
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutKeyboardUpFunc(keyboardUpListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(animate)
    glutMainLoop()


if __name__ == "__main__":
    main()
