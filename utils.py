from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from planet import drawSun, drawEarthAndMoon
from skybox import drawSkyBox
from orbit import drawEarthOrbit

# Cấu hình ánh sáng môi trường, ánh sáng khuếch tán, và vị trí nguồn sáng
LightAmb = (0.7, 0.7, 0.7)    # Ánh sáng môi trường màu xám nhạt
LightDif = (1.0, 1.0, 0.0)    # Ánh sáng khuếch tán màu vàng
LightPos = (4.0, 4.0, 6.0, 1.0)  # Vị trí nguồn sáng (x, y, z, w)

# Các biến toàn cục dùng để lưu trạng thái góc xoay các hành tinh và mặt trăng
earth_rot = 0.0       # Góc xoay Trái Đất quanh trục của nó
moon_rot = 0.0        # Góc xoay Mặt Trăng quanh trục của nó
earth_orbit = 0.0     # Góc vị trí Trái Đất trên quỹ đạo quanh Mặt Trời
moon_orbit = 0.0      # Góc vị trí Mặt Trăng trên quỹ đạo quanh Trái Đất
sun_rot = 0.0         # Góc xoay của Mặt Trời

def DrawGLScene(x, y, stars_texture, camera_distance, focus_object):
    global earth_rot, moon_rot, earth_orbit, moon_orbit, sun_rot  # Sử dụng các biến toàn cục lưu trạng thái quay

    # Xóa buffer màu và buffer độ sâu để chuẩn bị vẽ frame mới
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Reset ma trận hiện tại

    # Di chuyển camera lùi về phía sau theo khoảng cách camera
    glTranslatef(0, 0, -camera_distance)

    # Xoay camera theo góc x (xoay quanh trục X) và y (xoay quanh trục Y)
    glRotatef(x, 1, 0, 0)  # Xoay theo trục X
    glRotatef(y, 0, 1, 0)  # Xoay theo trục Y

    # -------- Vẽ Skybox (bầu trời sao) --------
    glPushAttrib(GL_ENABLE_BIT)   # Lưu trạng thái enable hiện tại
    glDisable(GL_LIGHTING)        # Tắt ánh sáng để skybox không bị ảnh hưởng bởi đèn
    glDepthMask(GL_FALSE)         # Tắt ghi vào buffer độ sâu để skybox luôn nằm phía sau
    drawSkyBox(50, stars_texture) # Vẽ skybox với kích thước 50 đơn vị và texture bầu trời sao
    glDepthMask(GL_TRUE)          # Bật lại ghi vào buffer độ sâu
    glPopAttrib()                 # Khôi phục lại trạng thái enable ban đầu

    # -------- Vẽ Mặt Trời --------
    glPushMatrix()                # Lưu ma trận hiện tại (camera transform)
    glLoadName(1)                 # Đặt ID tên cho đối tượng (phục vụ picking)
    glRotatef(sun_rot, 0, 1, 0)  # Quay Mặt Trời quanh trục Y với góc sun_rot
    drawSun()                    # Vẽ Mặt Trời
    glPopMatrix()                 # Khôi phục ma trận ban đầu

    # -------- Vẽ quỹ đạo Trái Đất quanh Mặt Trời --------
    glPushMatrix()
    drawEarthOrbit(5)             # Vẽ vòng quỹ đạo bán kính 5 đơn vị
    glPopMatrix()

    # -------- Vẽ Trái Đất và Mặt Trăng --------
    glPushMatrix()
    glLoadName(2)                 # Đặt ID tên cho nhóm Trái Đất + Mặt Trăng
    glRotatef(earth_orbit, 0, 1, 0)   # Quay toàn bộ hệ Trái Đất + Mặt Trăng quanh Mặt Trời
    glTranslatef(5, 0, 0)         # Dịch chuyển Trái Đất ra vị trí quỹ đạo (cách Mặt Trời 5 đơn vị)
    drawEarthAndMoon(earth_rot, moon_rot)  # Vẽ Trái Đất xoay và Mặt Trăng xoay quanh Trái Đất
    glPopMatrix()

    # -------- Điều chỉnh camera theo đối tượng focus --------
    if focus_object == 1:         # Nếu focus vào Mặt Trời
        camera_distance = max(camera_distance - 0.1, 4)  # Zoom gần lại, min là 4
    elif focus_object == 2:       # Nếu focus vào Trái Đất
        camera_distance = max(camera_distance - 0.1, 6)  # Zoom gần lại, min là 6
    else:                         # Không focus (chế độ tự do)
        camera_distance = min(camera_distance + 0.1, 10) # Zoom ra xa, max là 10

    # -------- Cập nhật các góc quay cho frame tiếp theo --------
    earth_rot = (earth_rot + 1) % 360      # Trái Đất quay quanh trục của nó nhanh (1 độ/frame)
    moon_rot = (moon_rot + 13) % 360       # Mặt Trăng quay quanh trục nhanh hơn (13 độ/frame)
    earth_orbit = (earth_orbit + 0.1) % 360  # Trái Đất quay quanh Mặt Trời chậm hơn (0.1 độ/frame)
    moon_orbit = (moon_orbit + 0.1) % 360     # Mặt Trăng quay quanh Trái Đất (đang không dùng ở đây?)
    sun_rot = (sun_rot + 0.1) % 360         # Mặt Trời tự quay nhẹ (0.1 độ/frame)

def InitGL(Width, Height):                
    """
    Khởi tạo các thông số OpenGL khi bắt đầu chương trình.
    Tham số:
        Width, Height: kích thước cửa sổ hiển thị
    """
    glClearColor(0.0, 0.0, 0.0, 0.0)    # Màu nền là đen
    glClearDepth(1.0)                    # Giá trị độ sâu tối đa
    glClearStencil(0)                    # Giá trị stencil mặc định
    glDepthFunc(GL_LEQUAL)               # Hàm so sánh depth test (<=)
    glEnable(GL_DEPTH_TEST)              # Bật kiểm tra độ sâu
    glShadeModel(GL_SMOOTH)              # Bật chế độ shading mượt mà

    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)  # Tối ưu chất lượng phép chiếu
    glEnable(GL_TEXTURE_2D)             # Bật sử dụng texture 2D

    # Cấu hình ánh sáng
    glLightfv(GL_LIGHT0, GL_AMBIENT, LightAmb)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LightDif)
    glLightfv(GL_LIGHT0, GL_POSITION, LightPos)
    glEnable(GL_LIGHT0)                 # Bật nguồn sáng LIGHT0
    glEnable(GL_LIGHTING)              # Bật hệ thống ánh sáng tổng thể

    # Cấu hình ma trận phép chiếu (projection)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)  # Thiết lập phối cảnh
    glMatrixMode(GL_MODELVIEW)         # Quay lại chế độ modelview

def pickPlanet(x, y, stars_texture, camera_distance, focus_object):
    """
    Hàm xử lý chọn đối tượng bằng kỹ thuật picking OpenGL.
    Tham số:
        x, y: tọa độ con trỏ chuột trong cửa sổ
        stars_texture: texture của skybox (để vẽ lại cảnh picking)
    Trả về:
        ID của đối tượng được chọn (nếu có), hoặc None nếu không chọn được
    """
    glSelectBuffer(512)    # Đặt buffer chứa kết quả picking (512 phần tử)
    glRenderMode(GL_SELECT) # Chuyển sang chế độ chọn (select)

    glInitNames()           # Khởi tạo stack tên object
    glPushName(0)           # Đẩy tên mặc định 0 vào stack

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()          # Lưu lại ma trận phép chiếu hiện tại
    glLoadIdentity()

    # Thiết lập vùng picking quanh điểm x, y chuột kích thước 5x5 pixels
    viewport = glGetIntegerv(GL_VIEWPORT)
    gluPickMatrix(x, viewport[3] - y, 5, 5, viewport)

    # Thiết lập lại phối cảnh giống khi render bình thường
    gluPerspective(45.0, float(viewport[2])/float(viewport[3]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    # Vẽ lại toàn bộ cảnh trong chế độ select
    DrawGLScene(0, 0, stars_texture, camera_distance, focus_object)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()           # Khôi phục ma trận phép chiếu ban đầu
    glMatrixMode(GL_MODELVIEW)

    hits = glRenderMode(GL_RENDER)   # Chuyển về chế độ render bình thường và lấy kết quả chọn

    if hits:
        # hits có dạng list các đối tượng trúng chọn,
        # hits[0][2][0] lấy ID tên của đối tượng đầu tiên được chọn
        return hits[0][2][0]

    return None  # Không chọn được đối tượng nào
