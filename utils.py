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
focus_object = None   # Đối tượng đang được camera theo dõi (sun, earth, hoặc None)
camera_distance = 10  # Khoảng cách camera so với trung tâm cảnh

def DrawGLScene(x, y, stars_texture):
    """
    Hàm vẽ toàn bộ cảnh 3D mỗi frame.
    Tham số:
        x, y: góc xoay của camera theo trục X và Y
        stars_texture: ID texture dùng để vẽ skybox (bầu trời sao)
    """
    global earth_rot, moon_rot, earth_orbit, moon_orbit, sun_rot, camera_distance, focus_object

    # Xóa buffer màu và độ sâu để chuẩn bị vẽ frame mới
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()  # Đặt lại ma trận modelview

    # Dịch camera lùi lại theo trục Z để quan sát toàn cảnh
    glTranslatef(0, 0, -camera_distance)
    # Xoay cảnh theo góc người dùng điều khiển
    glRotatef(x, 1, 0, 0)  # Xoay quanh trục X
    glRotatef(y, 0, 1, 0)  # Xoay quanh trục Y

    # Vẽ skybox (bầu trời sao) trước hết để nó luôn ở phía sau
    glPushAttrib(GL_ENABLE_BIT)  # Lưu lại trạng thái enable hiện tại
    glDisable(GL_LIGHTING)       # Tắt ánh sáng để skybox không bị ảnh hưởng
    glDepthMask(GL_FALSE)        # Tắt ghi depth buffer để skybox không ghi độ sâu
    drawSkyBox(50, stars_texture) # Vẽ hộp skybox kích thước 50
    glDepthMask(GL_TRUE)         # Bật lại ghi depth buffer
    glPopAttrib()                # Khôi phục trạng thái enable trước đó

    # Vẽ Mặt Trời
    glPushMatrix()               # Lưu trạng thái ma trận hiện tại
    glRotatef(sun_rot, 0, 1, 0) # Xoay Mặt Trời quanh trục Y để tạo hiệu ứng quay
    drawSun()                   # Gọi hàm vẽ Mặt Trời
    glPopMatrix()                # Khôi phục ma trận

    # Vẽ quỹ đạo Trái Đất quanh Mặt Trời (hình vòng tròn trắng)
    glPushMatrix()
    drawEarthOrbit(5)            # Bán kính quỹ đạo là 5 đơn vị
    glPopMatrix()

    # Vẽ Trái Đất và Mặt Trăng
    glPushMatrix()
    glRotatef(earth_orbit, 0, 1, 0)  # Xoay cả nhóm theo quỹ đạo Trái Đất
    glTranslatef(5, 0, 0)             # Dịch Trái Đất ra vị trí trên quỹ đạo
    drawEarthAndMoon(earth_rot, moon_rot)  # Vẽ Trái Đất và Mặt Trăng xoay riêng
    glPopMatrix()

    # Điều chỉnh khoảng cách camera tùy thuộc đối tượng đang theo dõi
    if focus_object == "sun":
        camera_distance = max(camera_distance - 0.1, 4)   # Thu gần camera, tối thiểu 4
    elif focus_object == "earth":
        camera_distance = max(camera_distance - 0.1, 6)   # Thu gần camera, tối thiểu 6
    else:
        camera_distance = min(camera_distance + 0.1, 10)  # Zoom ra tối đa 10

    # Cập nhật góc xoay để tạo chuyển động liên tục mỗi frame
    earth_rot = (earth_rot + 1) % 360        # Trái Đất xoay 1 độ/frame
    moon_rot = (moon_rot + 13) % 360         # Mặt Trăng xoay nhanh hơn
    earth_orbit = (earth_orbit + 0.1) % 360  # Trái Đất quay quanh Mặt Trời chậm hơn
    moon_orbit = (moon_orbit + 0.1) % 360    # Mặt Trăng quay quanh Trái Đất
    sun_rot = (sun_rot + 0.1) % 360           # Mặt Trời tự quay chậm

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

def pickPlanet(x, y, stars_texture):
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
    DrawGLScene(0, 0, stars_texture)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()           # Khôi phục ma trận phép chiếu ban đầu
    glMatrixMode(GL_MODELVIEW)

    hits = glRenderMode(GL_RENDER)   # Chuyển về chế độ render bình thường và lấy kết quả chọn

    if hits:
        # hits có dạng list các đối tượng trúng chọn,
        # hits[0][2][0] lấy ID tên của đối tượng đầu tiên được chọn
        return hits[0][2][0]

    return None  # Không chọn được đối tượng nào
