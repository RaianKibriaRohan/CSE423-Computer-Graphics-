# # Task1: Building a House in Rainfall

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import random

# Window dimensions
WIDTH = 800
HEIGHT = 600

# Raindrop class
class Raindrop:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = HEIGHT
        self.speed = random.uniform(2, 4)
        self.direction = 0

    def fall(self, direction):
        self.direction = direction
        self.y -= self.speed
        self.x += self.direction
        if self.y < 0:
            self.y = HEIGHT
            self.x = random.randint(0, WIDTH)

    def draw(self):
        glColor3f(0, 0, 1)
        glBegin(GL_LINES)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.direction, self.y - 10)
        glEnd()

# List of raindrops
raindrops = []
for i in range(100):
    new_raindrop = Raindrop()
    raindrops.append(new_raindrop)

# Background color control
background_color = [0.0, 0.0, 0.0]  # Night
target_color = [0.0, 0.0, 0.0]
DAY_COLOR = [0.7, 0.9, 1.0]  # Light blue
NIGHT_COLOR = [0.0, 0.0, 0.0]  # Black

rain_direction = 0

house_color = [0.96, 0.87, 0.70]
roof_color = [0.5, 0.1, 0.1]

def draw_ground():
    glColor3f(0.55, 0.27, 0.07)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(WIDTH, 0)
    glVertex2f(WIDTH, 200)
    glVertex2f(0, 200)
    glEnd()

def draw_trees():
    glColor3f(0, 1, 0)
    tree_positions = [50, 150, 250, 350, 450, 550, 650, 750]
    for x in tree_positions:
        glBegin(GL_TRIANGLES)
        glVertex2f(x - 20, 200)
        glVertex2f(x + 20, 200)
        glVertex2f(x, 300)
        glEnd()

def draw_house():
    glColor3f(*house_color)
    glBegin(GL_QUADS)
    glVertex2f(300, 200)
    glVertex2f(500, 200)
    glVertex2f(500, 350)
    glVertex2f(300, 350)
    glEnd()

    glColor3f(*roof_color)
    glBegin(GL_TRIANGLES)
    glVertex2f(300, 350)
    glVertex2f(500, 350)
    glVertex2f(400, 450)
    glEnd()

    glColor3f(0, 0, 0)
    glBegin(GL_QUADS)
    glVertex2f(400, 200)
    glVertex2f(430, 200)
    glVertex2f(430, 280)
    glVertex2f(400, 280)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(330, 280)
    glVertex2f(360, 280)
    glVertex2f(360, 310)
    glVertex2f(330, 310)
    glEnd()

    glBegin(GL_QUADS)
    glVertex2f(440, 280)
    glVertex2f(470, 280)
    glVertex2f(470, 310)
    glVertex2f(440, 310)
    glEnd()

def display():
    global background_color
    for i in range(3):
        background_color[i] += (target_color[i]-background_color[i])*0.002
    glClearColor(*background_color, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    draw_ground()
    draw_trees()
    draw_house()

    for raindrop in raindrops:
        raindrop.fall(rain_direction)
        raindrop.draw()

    glutSwapBuffers()

def keyboard(key, x, y):
    global target_color
    if key == b'\x1b':  # Escape key
        glutLeaveMainLoop()
    elif key == b'd':
        target_color = DAY_COLOR
    elif key == b'n':
        target_color = NIGHT_COLOR
    glutPostRedisplay()

def special_keys(key, x, y):
    global rain_direction
    if key == GLUT_KEY_LEFT:
        rain_direction = max(rain_direction - 1, -5)
    elif key == GLUT_KEY_RIGHT:
        rain_direction = min(rain_direction + 1, 5)
    glutPostRedisplay()

def idle():
    glutPostRedisplay()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(WIDTH, HEIGHT)
    glutCreateWindow(b"Rainy Day")
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutIdleFunc(idle)
    glViewport(0, 0, WIDTH, HEIGHT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, WIDTH, 0, HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glutMainLoop()
#starting
if __name__ == "__main__":
    main()













