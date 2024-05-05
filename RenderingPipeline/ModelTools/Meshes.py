import numpy as np
import trimesh

from RenderingPipeline.ModelTools.TriangleMesh import *
from RenderingPipeline.ModelTools.Material import *


class Meshes:
    def __init__(self, material):
        self.obj = None
        self.faces = None
        self.vertices = None

        self.triangle_meshes = None
        self.bounds = None

        self.material = material

    def read_obj(self, filepath):
        self.obj: trimesh.Trimesh = trimesh.load(filepath)
        self.faces = self.obj.faces
        self.vertices = self.obj.vertices

        self.create_meshes()

        print('Model file successfully loaded: ' + filepath)

    def create_meshes(self):
        self.triangle_meshes = []
        self.bounds = []

        for i in range(len(self.faces)):
            mesh = TriangleMesh(self.vertices[self.faces[i][0]], self.vertices[self.faces[i][1]],
                                self.vertices[self.faces[i][2]], self.material)
            self.triangle_meshes.append(mesh)
            self.bounds.append(mesh.bound)

        self.triangle_meshes = np.array(self.triangle_meshes)
        self.bounds = np.array(self.bounds)

    def set_material(self, material):
        self.material = material

    def set_obj_from_map(self, terrain_map: np.ndarray):
        height, width = terrain_map.shape

        with open('Asset/Model/terrain.obj', 'w') as f:
            for row in range(height):
                for col in range(width):
                    altitude = terrain_map[row, col]
                    f.write('v ' + str(col) + ' ' + str(altitude) + ' ' + str(row) + '\n')

            for row in range(height - 1):
                for col in range(width - 1):
                    index = col + row * width + 1
                    f.write('f ' + str(index) + ' ' + str(index + width) + ' ' + str(index + 1) + '\n')
                    f.write('f ' + str(index + 1) + ' ' + str(index + width) + ' ' + str(index + width + 1) + '\n')
        f.close()

        self.read_obj('Asset/Model/terrain.obj')
