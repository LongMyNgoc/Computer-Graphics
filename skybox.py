# skybox.py
from OpenGL.GL import *

def drawSkyBox(size, textureID):
    # Bật chế độ sử dụng texture 2D
    glEnable(GL_TEXTURE_2D)
    # Gắn (bind) texture được cung cấp vào để sử dụng cho toàn bộ skybox
    glBindTexture(GL_TEXTURE_2D, textureID)

    # ===========================
    # Vẽ các mặt của SkyBox Cube
    # ===========================

    # Front Face (mặt trước)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-size/2, -size/2, -size/2)  # Bottom-left
    glTexCoord2f(1, 0); glVertex3f( size/2, -size/2, -size/2)  # Bottom-right
    glTexCoord2f(1, 1); glVertex3f( size/2,  size/2, -size/2)  # Top-right
    glTexCoord2f(0, 1); glVertex3f(-size/2,  size/2, -size/2)  # Top-left
    glEnd()

    # Back Face (mặt sau)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-size/2, -size/2, size/2)   # Bottom-left
    glTexCoord2f(1, 0); glVertex3f( size/2, -size/2, size/2)   # Bottom-right
    glTexCoord2f(1, 1); glVertex3f( size/2,  size/2, size/2)   # Top-right
    glTexCoord2f(0, 1); glVertex3f(-size/2,  size/2, size/2)   # Top-left
    glEnd()

    # Top Face (mặt trên)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-size/2, size/2, -size/2)   # Back-left
    glTexCoord2f(1, 0); glVertex3f( size/2, size/2, -size/2)   # Back-right
    glTexCoord2f(1, 1); glVertex3f( size/2, size/2, size/2)    # Front-right
    glTexCoord2f(0, 1); glVertex3f(-size/2, size/2, size/2)    # Front-left
    glEnd()

    # Bottom Face (mặt dưới)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-size/2, -size/2, -size/2)  # Back-left
    glTexCoord2f(1, 0); glVertex3f( size/2, -size/2, -size/2)  # Back-right
    glTexCoord2f(1, 1); glVertex3f( size/2, -size/2, size/2)   # Front-right
    glTexCoord2f(0, 1); glVertex3f(-size/2, -size/2, size/2)   # Front-left
    glEnd()

    # Right Face (mặt phải)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(size/2, -size/2, -size/2)   # Bottom-back
    glTexCoord2f(1, 0); glVertex3f(size/2,  size/2, -size/2)   # Top-back
    glTexCoord2f(1, 1); glVertex3f(size/2,  size/2,  size/2)   # Top-front
    glTexCoord2f(0, 1); glVertex3f(size/2, -size/2,  size/2)   # Bottom-front
    glEnd()

    # Left Face (mặt trái)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex3f(-size/2, -size/2, -size/2)  # Bottom-back
    glTexCoord2f(1, 0); glVertex3f(-size/2,  size/2, -size/2)  # Top-back
    glTexCoord2f(1, 1); glVertex3f(-size/2,  size/2,  size/2)  # Top-front
    glTexCoord2f(0, 1); glVertex3f(-size/2, -size/2,  size/2)  # Bottom-front
    glEnd()

    # Tắt chế độ texture 2D sau khi vẽ xong skybox
    glDisable(GL_TEXTURE_2D)
