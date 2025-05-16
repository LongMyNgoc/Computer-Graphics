from OpenGL.GL import *          # Import tất cả các hàm cần thiết của OpenGL
from PIL import Image            # Dùng Pillow để xử lý hình ảnh

# Dictionary lưu các texture đã load để tránh load lại nhiều lần (tối ưu hiệu năng)
textures = {}

def LoadTextures(fname):
    """
    Load một texture từ file ảnh và trả về ID của texture trong OpenGL.
    Nếu ảnh đã từng được load trước đó, trả về lại ID cũ trong cache.
    """
    # Kiểm tra nếu texture đã được load trước đó, trả về luôn ID
    if textures.get(fname) is not None:
        return textures.get(fname)

    # Tạo một texture mới trong OpenGL và lưu ID vào biến 'texture'
    texture = textures[fname] = glGenTextures(1)

    # Dùng PIL để mở file ảnh
    image = Image.open(fname)

    # Lấy kích thước ảnh (width, height)
    ix = image.size[0]
    iy = image.size[1]

    # Chuyển ảnh thành chuỗi byte (định dạng RGBA 4 kênh)
    image = image.tobytes("raw", "RGBX", 0, -1)  # RGBX: thêm 1 byte giả cho độ tương thích RGBA

    # Gán texture đang thao tác
    glBindTexture(GL_TEXTURE_2D, texture)

    # Cấu hình byte alignment trong bộ nhớ cho OpenGL (1 nghĩa là không căn hàng byte)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    # Tải dữ liệu ảnh vào texture trong OpenGL
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)

    # Thiết lập chế độ lặp texture theo chiều S (ngang) và T (dọc)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)

    # Thiết lập chế độ lọc texture khi phóng to hoặc thu nhỏ (NEAREST: lấy pixel gần nhất)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    # Thiết lập chế độ áp dụng texture (DEACAL: chồng hình ảnh lên bề mặt không ảnh hưởng ánh sáng)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

    # Trả về ID texture để gắn vào vật thể khi render
    return texture
