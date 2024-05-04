import numpy as np
import trimesh

from RenderingPipeline.RayTracingTools.Bound import *
from RenderingPipeline.ModelTools.TriangleMesh import *
from RenderingPipeline.ModelTools.Material import *


class Meshes:
    def __init__(self):
        self.obj = None
        self.faces = None
        self.vertices = None

        self.meshes = None
        self.bounds = None

        self.material = None

    def read_obj(self, filepath):
        self.obj = trimesh.load(filepath)
        self.faces = self.obj.faces
        self.vertices = self.obj.vertices
        self.create_meshes()

    def set_meshes(self, obj, faces, vertices):
        self.obj = obj
        self.faces = faces
        self.vertices = vertices
        self.create_meshes()

    def create_meshes(self):
        self.meshes = []
        self.bounds = []

        for face in self.faces:
            mesh = TriangleMesh(self.vertices[face[0]], self.vertices[face[1]], self.vertices[face[2]], self.material)
            self.meshes.append(mesh)
            self.bounds.append(mesh.bound)

        self.meshes = np.array(self.meshes)
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
