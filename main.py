# main.py
import pygame as pg
from utils import InitGL, DrawGLScene, pickPlanet
from textures import LoadTextures

def main():
    # Khởi tạo pygame và thiết lập cửa sổ hiển thị
    pg.init()
    display = (1280, 720)  # Kích thước cửa sổ
    pg.display.set_mode(display, pg.DOUBLEBUF | pg.OPENGL)  # Tạo cửa sổ với chế độ DOUBLEBUF và hỗ trợ OpenGL
    pg.display.set_caption("Solar System Simulation")       # Đặt tiêu đề cửa sổ

    # Khởi tạo OpenGL với kích thước cửa sổ
    InitGL(*display)

    # Tải texture cho skybox (bầu trời sao)
    stars_texture = LoadTextures("./TexImg/stars.bmp")

    # Khởi tạo các biến để điều khiển góc xoay camera và khoảng cách camera
    x = y = 0                      # Góc xoay camera theo trục x, y
    camera_distance = 10           # Khoảng cách camera ban đầu
    prev_mouse_pos = None          # Vị trí chuột trước đó dùng để tính delta khi kéo chuột
    focus_object = None            # Đối tượng đang được camera theo dõi (None, 1 = Sun, 2 = Earth)

    clock = pg.time.Clock()        # Tạo đối tượng Clock để kiểm soát FPS

    # Vòng lặp chính của chương trình
    while True:
        clock.tick(60)             # Giới hạn tốc độ vòng lặp ở 60 FPS

        # Xử lý các sự kiện (events) từ pygame
        for event in pg.event.get():
            if event.type == pg.QUIT:     # Nếu nhấn nút đóng cửa sổ
                pg.quit()
                quit()

            if event.type == pg.KEYDOWN:  # Xử lý các phím bấm
                if event.key == pg.K_LEFT:
                    y += 2               # Quay camera sang trái
                if event.key == pg.K_RIGHT:
                    y -= 2               # Quay camera sang phải
                if event.key == pg.K_UP:
                    x += 2               # Quay camera lên trên
                if event.key == pg.K_DOWN:
                    x -= 2               # Quay camera xuống dưới
                if event.key == pg.K_ESCAPE:  # Nhấn ESC thoát chương trình
                    pg.quit()
                    quit()

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Click chuột trái để chọn hành tinh
                    mouse_x, mouse_y = pg.mouse.get_pos()  # Lấy tọa độ chuột
                    # Gọi hàm pickPlanet để xác định hành tinh được chọn dựa trên vị trí chuột
                    focus_object = pickPlanet(mouse_x, mouse_y, stars_texture, camera_distance, focus_object)
                    prev_mouse_pos = (mouse_x, mouse_y)   # Lưu vị trí chuột hiện tại
                elif event.button == 4:  # Cuộn chuột lên
                    camera_distance = max(camera_distance - 1, 4)  # Thu nhỏ khoảng cách camera, giới hạn min=4
                elif event.button == 5:  # Cuộn chuột xuống
                    camera_distance = min(camera_distance + 1, 20) # Tăng khoảng cách camera, giới hạn max=20

            if event.type == pg.MOUSEMOTION:
                # Kéo chuột trái để xoay camera
                if pg.mouse.get_pressed()[0]:
                    if prev_mouse_pos:
                        current_mouse_pos = pg.mouse.get_pos()  # Vị trí chuột hiện tại
                        dx = current_mouse_pos[0] - prev_mouse_pos[0]  # Sai khác theo trục x
                        dy = current_mouse_pos[1] - prev_mouse_pos[1]  # Sai khác theo trục y
                        prev_mouse_pos = current_mouse_pos
                        y += dx * 0.1    # Cập nhật góc xoay y theo delta chuột
                        x += dy * 0.1    # Cập nhật góc xoay x theo delta chuột

                # Kéo chuột phải để zoom camera
                elif pg.mouse.get_pressed()[2]:
                    if prev_mouse_pos:
                        current_mouse_pos = pg.mouse.get_pos()
                        dy = current_mouse_pos[1] - prev_mouse_pos[1]
                        prev_mouse_pos = current_mouse_pos
                        camera_distance += dy * 0.05             # Tăng/giảm khoảng cách camera
                        camera_distance = max(4, min(20, camera_distance))  # Giới hạn khoảng cách trong 4 đến 20

        # Vẽ lại toàn cảnh với các tham số điều khiển camera và đối tượng focus
        DrawGLScene(x, y, stars_texture, camera_distance, focus_object)

        # Cập nhật màn hình hiển thị
        pg.display.flip()
        pg.time.wait(10)  # Đợi 10ms để giảm tải CPU

if __name__ == "__main__":
    main()
