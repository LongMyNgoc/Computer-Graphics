from math import sin, cos, pi
from OpenGL.GL import *
from OpenGL.GLU import *

def drawEarthOrbit(radius=5.0):
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)
    glColor3f(1, 1, 1)  # Màu trắng dễ nhìn
    
    glBegin(GL_LINE_LOOP)
    for angle in range(0, 360, 5):
        rad = angle * 3.14159 / 180
        x = radius * cos(rad)
        z = radius * sin(rad)
        glVertex3f(x, 0, z)
    glEnd()
    
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)

