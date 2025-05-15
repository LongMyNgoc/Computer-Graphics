# main.py
import pygame as pg
from utils import InitGL, DrawGLScene, pickPlanet
from textures import LoadTextures

def main():
    global focus_object, prev_mouse_pos
    pg.init()
    display = (1280, 720)
    pg.display.set_mode(display, pg.DOUBLEBUF | pg.OPENGL)
    pg.display.set_caption("Solar System Simulation")
    InitGL(*display)
    stars_texture = LoadTextures("./TexImg/stars.bmp")
    x = y = 0
    prev_mouse_pos = None
    while True:
        pg.time.Clock().tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    y += 2
                if event.key == pg.K_RIGHT:
                    y -= 2
                if event.key == pg.K_UP:
                    x += 2 
                if event.key == pg.K_DOWN:
                    x -= 2
                if event.key == pg.K_ESCAPE:
                    pg.quit()
                    quit()
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = pg.mouse.get_pos()
                    focus_object = pickPlanet(mouse_x, mouse_y, stars_texture)
                    prev_mouse_pos = (mouse_x, mouse_y)
            if event.type == pg.MOUSEMOTION and pg.mouse.get_pressed()[0]:
                if prev_mouse_pos:
                    current_mouse_pos = pg.mouse.get_pos()
                    dx = current_mouse_pos[0] - prev_mouse_pos[0]
                    dy = current_mouse_pos[1] - prev_mouse_pos[1]
                    prev_mouse_pos = current_mouse_pos
                    y += dx * 0.1  # Adjust the multiplier for sensitivity
                    x += dy * 0.1  # Adjust the multiplier for sensitivity

        DrawGLScene(x, y, stars_texture)
        pg.display.flip()
        pg.time.wait(10)

if __name__ == "__main__":
    main()
