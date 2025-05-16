from OpenGL.GL import *
from OpenGL.GLU import *
from textures import LoadTextures
from math import cos, sin

def drawSun():
    """
    Hàm này vẽ Mặt Trời với hiệu ứng ánh sáng và texture phản chiếu (sử dụng Sphere Mapping).
    """

    global Q  # Biến toàn cục cho quadric object (dùng để vẽ hình cầu)
    glColor3f(1, 1, 1)  # Màu trắng (ảnh texture sẽ là chính)

    # Gắn texture Mặt Trời
    glBindTexture(GL_TEXTURE_2D, LoadTextures("./TexImg/sun.tga"))

    # Tạo quadric để vẽ cầu 3D
    Q = gluNewQuadric()
    gluQuadricNormals(Q, GLU_SMOOTH)       # Thiết lập chuẩn pháp tuyến mượt (cho ánh sáng mềm mại)
    gluQuadricTexture(Q, GL_TRUE)          # Cho phép sử dụng texture với quadric

    # Bật chế độ ánh xạ cầu (sphere mapping) cho texture
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    # Vẽ hình cầu (Mặt Trời)
    gluSphere(Q, 1.0, 32, 16)  # bán kính 1.0

    # Vẽ lớp sáng glow bao quanh Mặt Trời
    glColor4f(1, 1, 1, 0.4)          # Màu trắng, độ trong suốt 40%
    glEnable(GL_BLEND)              # Bật chế độ hòa trộn (alpha blending)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    gluSphere(Q, 1.0, 32, 16)       # Vẽ thêm 1 lớp glow trùng với Mặt Trời

    # Tắt blending và các thiết lập ánh xạ cầu
    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)
    glDisable(GL_BLEND)

    # Xóa quadric để giải phóng bộ nhớ
    gluDeleteQuadric(Q)


def drawEarthAndMoon(earth_rot, moon_rot):
    """
    Hàm này vẽ Trái Đất đang tự quay và Mặt Trăng quay quanh Trái Đất theo quỹ đạo tròn.
    Tham số:
        - earth_rot: góc quay của Trái Đất
        - moon_rot: góc quay của Mặt Trăng quanh Trái Đất
    """

    glColor3f(1, 1, 1)

    # Gắn texture cho Trái Đất
    glBindTexture(GL_TEXTURE_2D, LoadTextures("./TexImg/earthmap.bmp"))

    # Tạo quadric để vẽ cầu 3D
    Q = gluNewQuadric()
    gluQuadricNormals(Q, GLU_SMOOTH)
    gluQuadricTexture(Q, GL_TRUE)
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)

    # Vẽ Trái Đất quay quanh trục Y
    glPushMatrix()  # Lưu lại ma trận hiện tại
    glRotatef(earth_rot, 0, 1, 0)  # Xoay Trái Đất quanh trục Y
    gluSphere(Q, 0.4, 32, 16)      # Bán kính Trái Đất: 0.4

    # --- Vẽ quỹ đạo Mặt Trăng quanh Trái Đất ---
    glColor3f(1, 1, 1)  # Màu trắng cho quỹ đạo
    glBegin(GL_LINE_LOOP)
    radius = 1.0  # bán kính quỹ đạo Mặt Trăng
    for angle in range(0, 360, 5):
        rad = angle * 3.14159 / 180
        glVertex3f(radius * cos(rad), 0, radius * sin(rad))  # Trên mặt phẳng XZ
    glEnd()

    # --- Vẽ Mặt Trăng ---
    glBindTexture(GL_TEXTURE_2D, LoadTextures("./TexImg/2k_moon.jpg"))  # Gắn texture cho Mặt Trăng
    glRotatef(moon_rot, 0, 1, 0)  # Quay quanh Trái Đất
    glTranslatef(radius, 0, 0)    # Di chuyển Mặt Trăng ra quỹ đạo
    gluSphere(Q, 0.1, 32, 16)     # Vẽ Mặt Trăng với bán kính nhỏ hơn

    glPopMatrix()  # Khôi phục lại ma trận gốc

    # Xóa quadric
    gluDeleteQuadric(Q)
