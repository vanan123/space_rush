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
    os.environ['SDL_VIDEO_CENTERED'] = '1'


def quit_program():
    """Function for program abort"""
    pygame.quit()
    sys.exit()


def load_texture(path):
    """Function for loading texture"""
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


def arrows_movement(obj, speed, d_time):
    """Arrow movement, supports diagonal movement"""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or (keys[pygame.K_LEFT] and keys[pygame.K_UP]) or (keys[pygame.K_LEFT] and keys[pygame.K_DOWN]):
        obj.position[0] -= speed * d_time
    if keys[pygame.K_RIGHT] or (keys[pygame.K_RIGHT] and keys[pygame.K_UP]) or (keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]):
        obj.position[0] += speed * d_time
    if keys[pygame.K_UP] or (keys[pygame.K_LEFT] and keys[pygame.K_UP]) or (keys[pygame.K_RIGHT] and keys[pygame.K_UP]):
        obj.position[2] -= speed * d_time
    if keys[pygame.K_DOWN] or (keys[pygame.K_RIGHT] and keys[pygame.K_DOWN]) or (keys[pygame.K_LEFT] and keys[pygame.K_DOWN]):
        obj.position[2] += speed * d_time

def wasd_xy_movement(obj, speed, d_time):
    """wasd buttons movement along x and y axis (forward-backward, up-down), supports diagonal movement"""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or (keys[pygame.K_a] and keys[pygame.K_w]) or (keys[pygame.K_a] and keys[pygame.K_s]):
        obj.position[0] -= speed * d_time
    if keys[pygame.K_d] or (keys[pygame.K_d] and keys[pygame.K_w]) or (keys[pygame.K_d] and keys[pygame.K_s]):
        obj.position[0] += speed * d_time
    if keys[pygame.K_w] or (keys[pygame.K_a] and keys[pygame.K_w]) or (keys[pygame.K_d] and keys[pygame.K_w]):
        obj.position[1] -= speed * d_time
    if keys[pygame.K_s] or (keys[pygame.K_d] and keys[pygame.K_s]) or (keys[pygame.K_a] and keys[pygame.K_s]):
        obj.position[1] += speed * d_time

def wasd_xz_movement(obj, speed, d_time):
    """wasd buttons movement along x and z axis (forward-backward, left-right)"""
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] or (keys[pygame.K_a] and keys[pygame.K_w]) or (keys[pygame.K_a] and keys[pygame.K_s]):
        obj.position[0] -= speed * d_time
    if keys[pygame.K_d] or (keys[pygame.K_d] and keys[pygame.K_w]) or (keys[pygame.K_d] and keys[pygame.K_s]):
        obj.position[0] += speed * d_time
    if keys[pygame.K_w] or (keys[pygame.K_a] and keys[pygame.K_w]) or (keys[pygame.K_d] and keys[pygame.K_w]):
        obj.position[2] -= speed * d_time
    if keys[pygame.K_s] or (keys[pygame.K_d] and keys[pygame.K_s]) or (keys[pygame.K_a] and keys[pygame.K_s]):
        obj.position[2] += speed * d_time

def ship_movement(player, move_speed, lean_speed, delta_time, x_limit, y_limit):
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

def simple_zoom(fov, button):
    """View zoom, gets called when scrolling, calls mousebuttondown event"""
    if button == 4:
        fov *= 0.9
    elif button == 5:
        fov /= 0.9

    if fov > 100:
        fov = 100
    elif fov < 15:
        fov = 15
    return fov

def collision_detection(first, second):
    """Function to detect collision between two spheres"""
    distance_array = distance_between_two_objects(first, second)
    distance = distance_array[0]
    r1, r2 = distance_array[1], distance_array[2]

    # ako je udaljenost manja od zbroja radijusa imamo sudar
    if distance < r1 + r2:
        return True
    else:
        return False

def basic_AI(first, second, danger_zone, dtime, ai_speed):
    """Simple AI, start to follow a player if it is inside its danger_zone"""
    distance_array = distance_between_two_objects(first, second)
    distance = distance_array[0]
    size_first = distance_array[1]
    size_second = distance_array[2]
    x_dist, y_dist, z_dist = distance_array[3:6]

    if (distance < danger_zone and distance > size_first + size_second):
        second.position[1] += dtime * ai_speed * (y_dist / distance)  # normaliziran vektor
        second.position[0] += dtime * ai_speed * (x_dist / distance)
        second.position[2] += dtime * ai_speed * (z_dist / distance)


def distance_between_two_objects(first, second):
    """Returns distance between objects, used for collision detection"""
    # x pozicija
    x1 = first.position[0]
    x2 = second.position[0]

    # y pozicija
    y1 = first.position[1]
    y2 = second.position[1]

    # z pozicija
    z1 = first.position[2]
    z2 = second.position[2]

    # njihov radijus
    if hasattr(first, 'radius'):
        r1 = first.radius
    else:
        r1 = abs(first.size)
    if hasattr(second, 'radius'):
        r2 = second.radius
    else:
        r2 = abs(second.size)

    # formula za udaljenost između dviju točaka
    distance = np.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 - z1) * (z2 - z1))

    x_dist = x1 - x2
    y_dist = y1 - y2
    z_dist = z1 - z2

    return [distance, r1, r2, x_dist, y_dist, z_dist]


def draw_text(position, text_string, size=50, from_center=False, color=(255, 255, 255), back_color=None):
    """Function for drawing text on screen"""
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


class Cube(object):
    """Class for making a cube"""
    def __init__(self, size, position, color, visible=True):
        self.position = position
        self.size = size
        self.color = color
        self.visible = visible
        self.color.append(self.visible)
        self.vertices = [[+size, -size, -size], [+size, +size, -size],
                         [-size, +size, -size], [-size, -size, -size],
                         [+size, -size, +size], [+size, +size, +size],
                         [-size, -size, +size], [-size, +size, +size]]
        self.cube_sides = [[0, 1, 2, 3], [3, 2, 7, 6], [6, 7, 5, 4],
                           [4, 5, 1, 0], [1, 5, 7, 2], [4, 0, 3, 6]]

    def render(self):
        """Drawing a cube"""
        x = self.position[0]
        y = self.position[1]
        z = self.position[2]
        v = self.visible

        gl.glPushMatrix()
        # these two function below allow object transparency
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_COLOR_MATERIAL)
        gl.glColorMaterial(gl.GL_FRONT_AND_BACK, gl.GL_AMBIENT_AND_DIFFUSE)
        gl.glTranslatef(x, y, z)
        gl.glBegin(gl.GL_QUADS)
        self.color = [self.color[0], self.color[1], self.color[2], v]
        gl.glColor4f(*self.color)
        for side in self.cube_sides:
            for vert in side:
                gl.glVertex3fv(self.vertices[vert])
        gl.glEnd()
        gl.glDisable(gl.GL_BLEND)
        gl.glPopMatrix()


class Sphere(object):
    """Class for making a sphere"""
    def __init__(self, radius, position, color, visible=True):
        self.radius = radius
        self.position = position
        self.visible = visible
        self.color = color
        self.slices = 25  # meridijani
        self.stacks = 15  # paralele
        self.quadric = glu.gluNewQuadric()

    def render(self):
        """Drawing a sphere"""
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


class MouseClass(object):
    """Class for mouse controls"""
    def __init__(self, mouse_speed, move_speed):
        self.move_speed = move_speed
        self.mouse_speed = mouse_speed
        self.up = [0.0, 0.0, 0.0]
        self.right = [0.0, 0.0, 0.0]
        self.direction = [0.0, 0.0, 0.0]
        self.position = [0, 0, 0]
        self.hor_angle = 0.0
        self.vert_angle = 0.0

    def update_view(self):
        """Refreshes direction of view based on right and up vector"""
        self.direction = np.array([
            np.cos(self.vert_angle) * np.sin(self.hor_angle),
            np.sin(self.vert_angle),
            np.cos(self.vert_angle) * np.cos(self.hor_angle)])

        self.right = np.array([
            np.sin(self.hor_angle - np.pi / 2.0),
            0,
            np.cos(self.hor_angle - np.pi / 2.0)])

        # rezultantni vektor dvaju vektora
        self.up = np.cross(self.right, self.direction)

        # spremiti zbroj dvaju vektora, to nam je smjer gledanja u odnosu na trenutnu poziciju
        look_here = np.add(self.position, self.direction)

        look_at = (self.position[0], self.position[1], self.position[2],
                   look_here[0], look_here[1], look_here[2],
                   self.up[0], self.up[1], self.up[2])

        # vraćamo lookAt varijablu koju u glavnom programu proslijedimo u gluLookAt funkciju
        return look_at

    def limit_vert_view(self):
        """Limits vertical view to 90 degress up and down"""
        if self.vert_angle > 0.9:
            self.vert_angle = 0.9
        elif self.vert_angle < -0.9:
            self.vert_angle = -0.9

    def limit_hor_view(self):
        """Limits horizontal view to 90 degress left and right"""
        if self.hor_angle > 0.9:
            self.hor_angle = 0.9
        elif self.hor_angle < -0.9:
            self.hor_angle = -0.9

    def move_player(self, delta_time):
        """Player movement based on direction of view"""
        keys = pygame.key.get_pressed()
        # pomnožiti vektor smjera i desni vektor sa brzinom kretanja i vremenom između dva updatea
        self.direction = np.multiply(
            self.direction, delta_time * self.move_speed)
        self.right = np.multiply(self.right, delta_time * self.move_speed)

        if keys[pygame.K_w]:
            # zbroji trenutnu poziciju i vektor smjera
            self.position = np.add(self.position, self.direction)
        if keys[pygame.K_s]:
            self.position = np.subtract(self.position, self.direction)
        if keys[pygame.K_a]:
            self.position = np.subtract(self.position, self.right)
        if keys[pygame.K_d]:
            self.position = np.add(self.position, self.right)

    def angle(self, width, height, delta_time, mouse_position):
        """Refreshes angle of view, depends on a sensitivity of a mouse (mouse_speed)"""
        self.hor_angle += self.mouse_speed * delta_time * (width / 2 - mouse_position[0])
        self.vert_angle += self.mouse_speed * delta_time * (height / 2 - mouse_position[1])


class Skybox(object):
    """Skybox class (background image)"""
    def __init__(self, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        self.skybox = []
        self.sky_position = [0.0, 0.0, 0.0]
        self.sky_planes = [
            [(-10, -10, -10), (-10, -10, +10),
             (-10, +10, +10), (-10, +10, -10)],  # Naorijed
            [(-10, -10, +10), (+10, -10, +10),
             (+10, +10, +10), (-10, +10, +10)],  # Lijevo
            [(+10, -10, +10), (+10, -10, -10),
             (+10, +10, -10), (+10, +10, +10)],  # Natrag
            [(+10, -10, -10), (-10, -10, -10),
             (-10, +10, -10), (+10, +10, -10)],  # Desno
            [(-10, +10, -10), (-10, +10, +10),
             (+10, +10, +10), (+10, +10, -10)],  # Gore
            [(-10, -10, -10), (-10, -10, +10),
             (+10, -10, +10), (+10, -10, -10)]]  # Dolje

        self.sky_tex_coord = [[(0, 0), (1, 0), (1, 1), (0, 1)],
                              [(0, 0), (1, 0), (1, 1), (0, 1)],
                              [(0, 0), (1, 0), (1, 1), (0, 1)],
                              [(0, 0), (1, 0), (1, 1), (0, 1)],
                              [(0, 0), (1, 0), (1, 1), (0, 1)],
                              [(0, 1), (1, 1), (1, 0), (0, 0)]]

    def render(self):
        """Drawing skybox"""
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
        """Loading skybox with help of load_texture function"""
        self.skybox = [load_texture('materials/sky/Front_MauveSpaceBox.png'),
                       load_texture('materials/sky/Left_MauveSpaceBox.png'),
                       load_texture('materials/sky/Back_MauveSpaceBox.png'),
                       load_texture('materials/sky/Right_MauveSpaceBox.png'),
                       load_texture('materials/sky/Up_MauveSpaceBox.png'),
                       load_texture('materials/sky/Down_MauveSpaceBox.png')]
