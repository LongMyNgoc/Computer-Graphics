# skybox.py
from OpenGL.GL import *

def drawSkyBox(size, textureID):
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, textureID)

    # Front Face
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-size/2, -size/2, -size/2)
    glTexCoord2f(1, 0); glVertex3f( size/2, -size/2, -size/2)
    glTexCoord2f(1, 1); glVertex3f( size/2,  size/2, -size/2)
    glTexCoord2f(0, 1); glVertex3f(-size/2,  size/2, -size/2)
    glEnd()

    # Back Face
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-size/2, -size/2, size/2)
    glTexCoord2f(1, 0); glVertex3f( size/2, -size/2, size/2)
    glTexCoord2f(1, 1); glVertex3f( size/2,  size/2, size/2)
    glTexCoord2f(0, 1); glVertex3f(-size/2,  size/2, size/2)
    glEnd()

    # Top Face
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-size/2, size/2, -size/2)
    glTexCoord2f(1, 0); glVertex3f( size/2, size/2, -size/2)
    glTexCoord2f(1, 1); glVertex3f( size/2, size/2, size/2)
    glTexCoord2f(0, 1); glVertex3f(-size/2, size/2, size/2)
    glEnd()

    # Bottom Face
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-size/2, -size/2, -size/2)
    glTexCoord2f(1, 0); glVertex3f( size/2, -size/2, -size/2)
    glTexCoord2f(1, 1); glVertex3f( size/2, -size/2, size/2)
    glTexCoord2f(0, 1); glVertex3f(-size/2, -size/2, size/2)
    glEnd()

    # Right Face
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(size/2, -size/2, -size/2)
    glTexCoord2f(1, 0); glVertex3f(size/2,  size/2, -size/2)
    glTexCoord2f(1, 1); glVertex3f(size/2,  size/2,  size/2)
    glTexCoord2f(0, 1); glVertex3f(size/2, -size/2,  size/2)
    glEnd()

    # Left Face
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-size/2, -size/2, -size/2)
    glTexCoord2f(1, 0); glVertex3f(-size/2,  size/2, -size/2)
    glTexCoord2f(1, 1); glVertex3f(-size/2,  size/2,  size/2)
    glTexCoord2f(0, 1); glVertex3f(-size/2, -size/2,  size/2)
    glEnd()

    glDisable(GL_TEXTURE_2D)
