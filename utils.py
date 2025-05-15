from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from planet import drawSun, drawEarthAndMoon
from skybox import drawSkyBox
from orbit import drawEarthOrbit

LightAmb = (0.7, 0.7, 0.7)  
LightDif = (1.0, 1.0, 0.0)  
LightPos = (4.0, 4.0, 6.0, 1.0)
earth_rot = 0.0
moon_rot = 0.0
earth_orbit = 0.0
moon_orbit = 0.0
sun_rot = 0.0
focus_object = None
camera_distance = 10

def DrawGLScene(x, y, stars_texture):
    global earth_rot, moon_rot, earth_orbit, moon_orbit, sun_rot, camera_distance, focus_object
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(0, 0, -camera_distance)
    glRotatef(x, 1, 0, 0)
    glRotatef(y, 0, 1, 0)
    
    # Vẽ skybox đầu tiên:
    glPushAttrib(GL_ENABLE_BIT)
    glDisable(GL_LIGHTING)
    glDepthMask(GL_FALSE)
    drawSkyBox(50, stars_texture)
    glDepthMask(GL_TRUE)
    glPopAttrib()

    # Vẽ Mặt Trời
    glPushMatrix()
    glRotatef(sun_rot, 0, 1, 0)
    drawSun()
    glPopMatrix()

    # Vẽ quỹ đạo Trái Đất quanh Mặt Trời (vòng tròn trắng)
    glPushMatrix()
    drawEarthOrbit(5)  # bán kính quỹ đạo Trái Đất
    glPopMatrix()

    # Vẽ Trái Đất + Mặt Trăng (đã dịch chuyển theo quỹ đạo)
    glPushMatrix()
    glRotatef(earth_orbit, 0, 1, 0)
    glTranslatef(5, 0, 0)
    drawEarthAndMoon(earth_rot, moon_rot)
    glPopMatrix()

    # Điều chỉnh khoảng cách camera
    if focus_object == "sun":
        camera_distance = max(camera_distance - 0.1, 4)
    elif focus_object == "earth":
        camera_distance = max(camera_distance - 0.1, 6)
    else:
        camera_distance = min(camera_distance + 0.1, 10)

    # Cập nhật các góc xoay
    earth_rot = (earth_rot + 1) % 360
    moon_rot = (moon_rot + 13) % 360
    earth_orbit = (earth_orbit + 0.1) % 360
    moon_orbit = (moon_orbit + 0.1) % 360
    sun_rot = (sun_rot + 0.1) % 360

def InitGL(Width, Height):                
    glClearColor(0.0, 0.0, 0.0, 0.0)    
    glClearDepth(1.0)                    
    glClearStencil(0)
    glDepthFunc(GL_LEQUAL)               
    glEnable(GL_DEPTH_TEST)                
    glShadeModel(GL_SMOOTH)                

    glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
    glEnable(GL_TEXTURE_2D)

    glLightfv(GL_LIGHT0, GL_AMBIENT, LightAmb)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, LightDif)
    glLightfv(GL_LIGHT0, GL_POSITION, LightPos)
    glEnable(GL_LIGHT0)           
    glEnable(GL_LIGHTING)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def pickPlanet(x, y, stars_texture):
    glSelectBuffer(512)
    glRenderMode(GL_SELECT)
    glInitNames()
    glPushName(0)

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    viewport = glGetIntegerv(GL_VIEWPORT)
    gluPickMatrix(x, viewport[3] - y, 5, 5, viewport)
    gluPerspective(45.0, float(viewport[2])/float(viewport[3]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    DrawGLScene(0, 0, stars_texture)

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    hits = glRenderMode(GL_RENDER)

    if hits:
        return hits[0][2][0]
    return None