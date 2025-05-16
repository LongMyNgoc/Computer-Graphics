# main.py
import pygame as pg
from utils import InitGL, DrawGLScene, pickPlanet
from textures import LoadTextures

def main():
    global focus_object, prev_mouse_pos  # Sử dụng biến toàn cục để theo dõi đối tượng được focus và vị trí chuột trước đó

    pg.init()  # Khởi tạo Pygame
    display = (1280, 720)  # Kích thước cửa sổ hiển thị

    # Tạo cửa sổ hiển thị với chế độ DOUBLEBUF (double buffering) và OPENGL (sử dụng OpenGL)
    pg.display.set_mode(display, pg.DOUBLEBUF | pg.OPENGL)
    pg.display.set_caption("Solar System Simulation")  # Tiêu đề cửa sổ

    InitGL(*display)  # Khởi tạo thiết lập OpenGL với kích thước cửa sổ

    # Tải texture hình nền bầu trời sao từ file
    stars_texture = LoadTextures("./TexImg/stars.bmp")

    # Khởi tạo góc xoay ban đầu theo trục X và Y
    x = y = 0
    prev_mouse_pos = None  # Biến lưu vị trí chuột lần trước dùng cho việc xoay camera khi kéo chuột

    # Vòng lặp chính của chương trình, chạy liên tục
    while True:
        pg.time.Clock().tick(60)  # Giới hạn tốc độ vòng lặp ở 60 FPS (khung hình mỗi giây)

        # Xử lý sự kiện trong hàng đợi sự kiện của Pygame
        for event in pg.event.get():
            if event.type == pg.QUIT:
                # Nếu người dùng đóng cửa sổ thì thoát chương trình
                pg.quit()
                quit()

            if event.type == pg.KEYDOWN:
                # Xử lý các phím mũi tên để điều chỉnh góc xoay camera
                if event.key == pg.K_LEFT:
                    y += 2  # Xoay sang trái
                if event.key == pg.K_RIGHT:
                    y -= 2  # Xoay sang phải
                if event.key == pg.K_UP:
                    x += 2  # Xoay lên trên
                if event.key == pg.K_DOWN:
                    x -= 2  # Xoay xuống dưới
                if event.key == pg.K_ESCAPE:
                    # Nhấn ESC để thoát
                    pg.quit()
                    quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                # Khi bấm chuột trái, kiểm tra xem người dùng có chọn hành tinh nào không
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = pg.mouse.get_pos()  # Lấy tọa độ chuột
                    # Gọi hàm pickPlanet để xác định hành tinh được click dựa trên tọa độ chuột
                    focus_object = pickPlanet(mouse_x, mouse_y, stars_texture)
                    prev_mouse_pos = (mouse_x, mouse_y)  # Lưu vị trí chuột để sử dụng khi kéo

            if event.type == pg.MOUSEMOTION and pg.mouse.get_pressed()[0]:
                # Khi kéo chuột trái, tính toán sự thay đổi vị trí chuột để xoay camera
                if prev_mouse_pos:
                    current_mouse_pos = pg.mouse.get_pos()  # Vị trí chuột hiện tại
                    dx = current_mouse_pos[0] - prev_mouse_pos[0]  # Khoảng cách dịch chuyển theo trục X
                    dy = current_mouse_pos[1] - prev_mouse_pos[1]  # Khoảng cách dịch chuyển theo trục Y
                    prev_mouse_pos = current_mouse_pos  # Cập nhật vị trí chuột trước đó

                    # Cập nhật góc xoay dựa trên sự dịch chuyển chuột
                    # Hệ số 0.1 để điều chỉnh độ nhạy xoay
                    y += dx * 0.1
                    x += dy * 0.1

        # Vẽ lại toàn bộ cảnh với góc xoay hiện tại và texture bầu trời sao
        DrawGLScene(x, y, stars_texture)

        # Cập nhật màn hình hiển thị
        pg.display.flip()

        # Tạm dừng 10ms để tránh chạy quá nhanh, giảm tải CPU
        pg.time.wait(10)

# Nếu chạy file này trực tiếp thì gọi hàm main()
if __name__ == "__main__":
    main()
