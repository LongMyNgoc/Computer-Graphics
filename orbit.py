from math import sin, cos, pi
from OpenGL.GL import *
from OpenGL.GLU import *

def drawEarthOrbit(radius=5.0):
    """
    Hàm này vẽ quỹ đạo hình tròn (đường tròn) đại diện cho chuyển động quay của Trái Đất xung quanh Mặt Trời.
    """

    # Tắt ánh sáng và texture để chỉ vẽ đường viền (không chịu ảnh hưởng ánh sáng và không có hình ảnh phủ lên)
    glDisable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)

    # Đặt màu trắng cho quỹ đạo để dễ quan sát
    glColor3f(1, 1, 1)

    # Bắt đầu vẽ đường tròn bằng các đoạn thẳng nhỏ kết nối với nhau
    glBegin(GL_LINE_LOOP)

    # Duyệt qua các góc từ 0 đến 360 độ, mỗi lần bước 5 độ
    for angle in range(0, 360, 5):
        rad = angle * pi / 180  # Chuyển độ sang radian
        x = radius * cos(rad)   # Tính tọa độ X trên đường tròn
        z = radius * sin(rad)   # Tính tọa độ Z (Y bằng 0 vì nằm trên mặt phẳng XZ)
        glVertex3f(x, 0, z)      # Thêm đỉnh vào đường tròn

    glEnd()  # Kết thúc vẽ đường tròn

    # Bật lại texture và lighting để tiếp tục vẽ các đối tượng khác như Trái Đất, Mặt Trăng, v.v.
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_LIGHTING)
