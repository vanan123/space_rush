"""Module for loading objects from Blender and it's appropriate texture"""

import OpenGL.GL as gl
import numpy as np
from modules.commons import load_texture


def material(filename):
    contents = {}
    mtl = {}
    for line in open(filename, "r"):
        if line.startswith('#'):
            continue
        values = line.split()
        if not values:
            continue
        if values[0] == 'newmtl':
            mtl = contents[values[1]] = {}
        elif mtl is None:
            raise ValueError("mtl does not start with newmtl")
        elif values[0] == 'map_Kd':
            mtl['texture_Kd'] = load_texture(values[1])
        else:
            mtl[values[0]] = list(map(float, values[1:]))
    return contents



class OBJ(object):
    def __init__(self, filename, size):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.size = size
        self.tex = False
        mat = None
        for line in open(filename, "r"):
            if line.startswith('#'):
                continue
            values = line.split()
            if not values:
                continue
            if values[0] == 'v':
                self.vertices.append(values[1:4])
            elif values[0] == 'vt':
                self.texcoords.append(values[1:3])
                self.tex = True
            elif values[0] == 'vn':
                self.normals.append(values[1:4])
            elif values[0] in ('usemtl', 'usemat'):
                mat = values[1]
            elif values[0] == 'mtllib':
                self.mtl = material(values[1])
            elif values[0] == 'f':
                face = []
                tex = []
                norms = []
                for vert in values[1:4]:
                    val = vert.split('/')
                    face.append(int(val[0]))
                    if len(val) >= 2 and len(val[1]) > 0:
                        tex.append(int(val[1]))
                    else:
                        tex.append(0)
                    if len(val) >= 3 and len(val[2]) > 0:
                        norms.append(int(val[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, tex, mat))

        self.list_id = gl.glGenLists(1)
        gl.glNewList(self.list_id, gl.GL_COMPILE)
        self.render_obj()
        gl.glEndList()

   
    def render_obj(self):
        gl.glEnable(gl.GL_TEXTURE_2D)
        for face in self.faces:
            vertices, normals, texture_coords, mat = face
            mtl = self.mtl[mat]
            if 'texture_Kd' in mtl:
                gl.glBindTexture(gl.GL_TEXTURE_2D, mtl['texture_Kd'])
            else:
                gl.glColor3f(*mtl['Kd'])
            gl.glBegin(gl.GL_TRIANGLES)
            for i in range(len(vertices)):
                gl.glNormal3f(float(self.normals[normals[i] - 1][0]),
                              float(self.normals[normals[i] - 1][1]),
                              float(self.normals[normals[i] - 1][2]))
                if self.tex:
                    gl.glTexCoord2f(float(self.texcoords[texture_coords[i] - 1][0]),
                                    float(self.texcoords[texture_coords[i] - 1][1]))
                gl.glVertex3f(float(self.vertices[vertices[i] - 1][0]) * self.size,
                              float(self.vertices[vertices[i] - 1][1]) * self.size,
                              float(self.vertices[vertices[i] - 1][2]) * self.size)
            gl.glEnd()
        gl.glDisable(gl.GL_TEXTURE_2D)

    def max_vert(self):
        #To setect collision, largest coordinate is returned
        max_vert = 0
        for vert in self.vertices:
            if(abs(float(max(vert))) * self.size > max_vert):
                max_vert = abs(float(max(vert))) * self.size
        return max_vert
