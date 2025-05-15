from OpenGL.GL import *
from OpenGL.GLU import *
from textures import LoadTextures
from math import cos, sin

def drawSun():
    global Q
    glColor3f(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, LoadTextures("./TexImg/sun.tga"))

    Q = gluNewQuadric()
    gluQuadricNormals(Q, GLU_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    gluSphere(Q, 1.0, 32, 16)

    glColor4f(1, 1, 1, 0.4)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    gluSphere(Q, 1.0, 32, 16)

    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)
    glDisable(GL_BLEND)
    gluDeleteQuadric(Q)

def drawEarthAndMoon(earth_rot, moon_rot):
    glColor3f(1, 1, 1)
    glBindTexture(GL_TEXTURE_2D, LoadTextures("./TexImg/earthmap.bmp"))

    Q = gluNewQuadric()
    gluQuadricNormals(Q, GLU_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    # Vẽ Trái Đất
    glPushMatrix()
    glRotatef(earth_rot, 0, 1, 0)
    gluSphere(Q, 0.4, 32, 16)

    # Vẽ quỹ đạo Mặt Trăng
    glColor3f(1, 1, 1)  # màu trắng cho quỹ đạo
    glBegin(GL_LINE_LOOP)
    radius = 1.0
    for angle in range(0, 360, 5):
        rad = angle * 3.14159 / 180
        glVertex3f(radius * cos(rad), 0, radius * sin(rad))
    glEnd()

    # Vẽ Mặt Trăng
    glBindTexture(GL_TEXTURE_2D, LoadTextures("./TexImg/2k_moon.jpg"))
    glRotatef(moon_rot, 0, 1, 0)
    glTranslatef(radius, 0, 0)
    gluSphere(Q, 0.1, 32, 16)

    glPopMatrix()
    gluDeleteQuadric(Q)
