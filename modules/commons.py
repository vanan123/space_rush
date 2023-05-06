"""Module which contains frequently used functions ans classes"""

import os
import sys

import pygame
import numpy as np
import OpenGL.GL as gl
import OpenGL.GLU as glu

pygame.init()


# Prozor centriran na sredinu ekrana
def center_window():
    """Function for centering window"""
    # Hiển thị cửa sổ game giữa màn hình
    os.environ['SDL_VIDEO_CENTERED'] = '1'


def quit_program():
    """Function for program abort"""
    # Out game
    pygame.quit()
    sys.exit()


def load_texture(path):
    """Function for loading texture"""
    # Hiển thị ảnh nền
    surface = pygame.image.load(path)
    data = pygame.image.tostring(surface, "RGBA", True)

    ix = surface.get_width()
    iy = surface.get_height()

    gl.glEnable(gl.GL_TEXTURE_2D)
    tex_id = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, tex_id)

    gl.glPixelStorei(gl.GL_UNPACK_ALIGNMENT, 1)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, 3, ix, iy, 0,
                    gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, data)

    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
    gl.glTexParameteri(
        gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_R, gl.GL_CLAMP_TO_EDGE)
    gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_MODULATE)

    return tex_id

def ship_movement(player, move_speed, lean_speed, delta_time, x_limit, y_limit):
    # Tính toán và di chuyển máy bay
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        if player.position[0] > -x_limit:
            player.position[0] -= move_speed * delta_time * 1.2
        if player.rot_z < -39:
            player.rot_z = -40
        else:
            player.rot_z -= lean_speed * delta_time
    if keys[pygame.K_d]:
        if player.position[0] < x_limit:
            player.position[0] += move_speed * delta_time * 1.2
        if player.rot_z > 39:
            player.rot_z = 40
        else:
            player.rot_z += lean_speed * delta_time
    if keys[pygame.K_w]:
        if player.position[1] < y_limit:
            player.position[1] += move_speed * delta_time
        if player.rot_x > 24:
            player.rot_x = 25
        else:
            player.rot_x += lean_speed * delta_time
    if keys[pygame.K_s]:
        if player.position[1] > -y_limit:
            player.position[1] -= move_speed * delta_time
        if player.rot_x < -24:
            player.rot_x = -25
        else:
            player.rot_x -= lean_speed * delta_time
    if not keys[pygame.K_a] and not keys[pygame.K_d]:
        if player.rot_z < -1 - lean_speed * delta_time:
            player.rot_z += lean_speed * delta_time
        elif player.rot_z > 1 + lean_speed * delta_time:
            player.rot_z -= lean_speed * delta_time
        else:
            player.rot_z = 0
    if not keys[pygame.K_w] and not keys[pygame.K_s]:
        if player.rot_x < -1 - lean_speed * delta_time:
            player.rot_x += lean_speed * delta_time
        elif player.rot_x > 1 + lean_speed * delta_time:
            player.rot_x -= lean_speed * delta_time
        else:
            player.rot_x = 0

def collision_detection(first, second):
    # Phát hiện tàu và vật thể có va chạm hay không
    distance_array = distance_between_two_objects(first, second)
    distance = distance_array[0]
    r1, r2 = distance_array[1], distance_array[2]

    # Chạm nhau
    if distance < r1 + r2:
        return True
    else:
        return False

def distance_between_two_objects(first, second):
    # Tính toán khoảng cách giữa các đối tượng
    # Khoảng cách được tính từ tâm vật thể này tới tấm của vật thể khác
    # x 
    x1 = first.position[0]
    x2 = second.position[0]

    # y 
    y1 = first.position[1]
    y2 = second.position[1]

    # z 
    z1 = first.position[2]
    z2 = second.position[2]

    if hasattr(first, 'radius'):
        r1 = first.radius
    else:
        r1 = abs(first.size)
    if hasattr(second, 'radius'):
        r2 = second.radius
    else:
        r2 = abs(second.size)

    distance = np.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1))

    x_dist = x1 - x2
    y_dist = y1 - y2
    z_dist = z1 - z2

    return [distance, r1, r2, x_dist, y_dist, z_dist]


def draw_text(position, text_string, size=50, from_center=False, color=(255, 255, 255), back_color=None):
    # Viết chữ trên màn hình
    font = pygame.font.SysFont('timesnewroman', size)
    text_surface = font.render(text_string, True, color, back_color)
    img_data = pygame.image.tostring(text_surface, "RGBA", True)
    ix, iy = text_surface.get_width(), text_surface.get_height()
    x = 20
    if from_center:
        x = position[0] - int(ix / 2)
    else:
        x = position[0]
    gl.glEnable(gl.GL_BLEND)
    gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
    gl.glWindowPos2i(x, position[1])
    gl.glDrawPixels(ix, iy, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, img_data)
    gl.glDisable(gl.GL_BLEND)


class Light(object):
    """Class for adding light into the game"""
    # Thêm ánh sáng cho nền game

    def __init__(self, direction):
        self.intensity = [1.0, 1.0, 1.0, 1.0]
        self.direction = direction
        self.ambient_intensity = [0.2, 0.2, 0.2, 1.0]
        self.specular_intensity = [0.6, 0.6, 0.6, 1.0]
        self.enable_specular = True

    def render(self):
        """Setting a position and type of light"""
        gl.glLightModelfv(gl.GL_LIGHT_MODEL_AMBIENT, self.ambient_intensity)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_POSITION, self.direction)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_DIFFUSE, self.intensity)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_CONSTANT_ATTENUATION, 0.1)
        gl.glLightfv(gl.GL_LIGHT0, gl.GL_LINEAR_ATTENUATION, 0.05)
        # Ovo ispod je za reflektirajuće svjetlo
        if self.enable_specular:
            gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SPECULAR,
                            self.specular_intensity)
            gl.glMaterialfv(gl.GL_FRONT_AND_BACK, gl.GL_SHININESS, 15.0)
            gl.glLightfv(gl.GL_LIGHT0, gl.GL_SPECULAR, self.specular_intensity)

    def enable(self):
        """Enable light"""
        gl.glEnable(gl.GL_LIGHTING)
        gl.glEnable(gl.GL_LIGHT0)

    def disable(self):
        """Disable light"""
        gl.glDisable(gl.GL_LIGHTING)
        gl.glDisable(gl.GL_LIGHT0)


class Sphere(object):
    # Class dùng để tạo các đối tượng vật cản 
    def __init__(self, radius, position, color, visible=True):
        self.radius = radius
        self.position = position
        self.visible = visible
        self.color = color
        self.slices = 25  # meridijani
        self.stacks = 15  # paralele
        self.quadric = glu.gluNewQuadric()

    def render(self):
        # Vẽ các đối tượng vật thể (vật cản)
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        v = self.visible
        gl.glPushMatrix()
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
        self.color = (self.color[0], self.color[1], self.color[2], v)
        gl.glColor4f(*self.color)
        gl.glTranslatef(x, y, z)
        glu.gluSphere(self.quadric, self.radius, self.slices, self.stacks)
        gl.glDisable(gl.GL_BLEND)
        gl.glPopMatrix()

class Skybox(object):
    # Class dùng để khởi tạo ảnh nền
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.skybox = []
        self.sky_position = [0.0, 0.0, 0.0]
        self.sky_planes = [
            [(-10, -10, -10), (-10, -10, +10),
             (-10, +10, +10), (-10, +10, -10)],  
            [(-10, -10, +10), (+10, -10, +10),
             (+10, +10, +10), (-10, +10, +10)],  
            [(+10, -10, +10), (+10, -10, -10),
             (+10, +10, -10), (+10, +10, +10)], 
            [(+10, -10, -10), (-10, -10, -10),
             (-10, +10, -10), (+10, +10, -10)],
            [(-10, +10, -10), (-10, +10, +10),
             (+10, +10, +10), (+10, +10, -10)],
            [(-10, -10, -10), (-10, -10, +10),
             (+10, -10, +10), (+10, -10, -10)]]

        self.sky_tex_coord = [[(0, 0), (1, 0), (1, 1), (0, 1)],
                              [(0, 0), (1, 0), (1, 1), (0, 1)],
                              [(0, 0), (1, 0), (1, 1), (0, 1)],
                              [(0, 0), (1, 0), (1, 1), (0, 1)],
                              [(0, 0), (1, 0), (1, 1), (0, 1)],
                              [(0, 1), (1, 1), (1, 0), (0, 0)]]

    def render(self):
        # Vẽ các hình nền
        gl.glPushMatrix()
        gl.glDisable(gl.GL_CULL_FACE)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_TEXTURE_2D)
        gl.glTranslatef(*self.sky_position)
        for i in range(len(self.sky_planes)):
            gl.glBindTexture(gl.GL_TEXTURE_2D, self.skybox[i])
            gl.glBegin(gl.GL_QUADS)
            for j in range(len(self.sky_planes[i])):
                gl.glTexCoord2f(*self.sky_tex_coord[i][j])
                gl.glVertex3f(*self.sky_planes[i][j])
            gl.glEnd()
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glPopMatrix()

    def init_sky(self):
        # Hiển thị ảnh nền
        self.skybox = [load_texture('materials/sky/Front_MauveSpaceBox.png'),
                       load_texture('materials/sky/Left_MauveSpaceBox.png'),
                       load_texture('materials/sky/Back_MauveSpaceBox.png'),
                       load_texture('materials/sky/Right_MauveSpaceBox.png'),
                       load_texture('materials/sky/Up_MauveSpaceBox.png'),
                       load_texture('materials/sky/Down_MauveSpaceBox.png')]
