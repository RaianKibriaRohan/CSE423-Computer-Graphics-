# Task2: Building the Amazing Box

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

class Point:
    def __init__(self, x, y):
        self.size = 10
        self.r = random.random()
        self.g = random.random()
        self.b = random.random()
        self.x = x
        self.y = y
        self.direction_x = random.choice([1, -1])
        self.direction_y = random.choice([1, -1])

class PointScene:
    def __init__(self):
        self.width = self.height = 500
        self.background = 0
        self.speed = 0.001
        self.point_list = []
        self.freeze = False

    def makePoints(self, x, y):
        # Create 1 point per click
        self.point_list.append(Point(x, self.height - y))
        print(f"Created 1 point at ({x}, {self.height - y})")

    def drawPoints(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.iterate()
        glClearColor(self.background, self.background, self.background, 1.0)
        
        for point in self.point_list:
            glPointSize(point.size)
            glBegin(GL_POINTS)
            glColor3f(point.r, point.g, point.b)  # Set point color
            glVertex2f(point.x, point.y)  # Draw point
            glEnd()
        glutSwapBuffers()

    def iterate(self):
        glViewport(0, 0, self.width, self.height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, self.width, 0.0, self.height, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def showScreen(self):
        self.drawPoints()

    def animate(self):
        if not self.freeze:
            for point in self.point_list:
                point.x += point.direction_x * self.speed
                point.y += point.direction_y * self.speed
                # Bounce off window edges
                if point.x < 0 or point.x > self.width:
                    point.direction_x *= -1
                if point.y < 0 or point.y > self.height:
                    point.direction_y *= -1
        glutPostRedisplay()

    def mouseListener(self, button, state, x, y):
        if not self.freeze:
            if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
                self.makePoints(x, y)  # Create 1 point per click
        glutPostRedisplay()

    def specialKeyListener(self, key, x, y):
        if not self.freeze:
            if key == GLUT_KEY_UP:
                self.speed += 0.001
                print(f"Speed increased to: {self.speed}")
            if key == GLUT_KEY_DOWN:
                self.speed -= 0.001
                print(f"Speed decreased to: {self.speed}")
        glutPostRedisplay()

    def run(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA)
        glutInitWindowSize(self.width, self.height)
        glutInitWindowPosition(0, 0)
        glutCreateWindow(b"OpenGL Point Spawn")
        glutDisplayFunc(self.showScreen)
        glutIdleFunc(self.animate)
        glutMouseFunc(self.mouseListener)
        glutSpecialFunc(self.specialKeyListener)
        print("Starting GLUT main loop...")
        glutMainLoop()

if __name__ == "__main__":
    PointScene().run()
