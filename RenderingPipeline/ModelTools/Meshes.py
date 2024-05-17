import trimesh
import numpy as np

from RenderingPipeline.ModelTools.Material import Material
from RenderingPipeline.ModelTools.TriangleMesh import TriangleMesh


class Meshes:
    def __init__(self, filepath=None, material=None):
        self.obj = None
        self.faces = None
        self.vertices = None
        self.vertex_colors = None

        self.triangle_meshes = None
        self.bounds = None

        if material is None:
            self.material = Material()
        else:
            self.material = material

        if filepath is not None:
            self.read_obj(filepath)

    def read_obj(self, filepath):
        self.obj: trimesh.Trimesh = trimesh.load(filepath)
        print('Model file successfully loaded: ' + filepath)

        self.faces = self.obj.faces
        self.vertices = self.obj.vertices
        self.vertex_colors = self.obj.visual.vertex_colors

        self.create_meshes()

    def create_meshes(self):
        self.triangle_meshes = []
        self.bounds = []

        num_faces = len(self.faces)
        for i in range(num_faces):
            print('\rCreating TriangleMeshes for the model: {:.1f}%'.format(100 * i / num_faces), end='')

            vertices = self.vertices[self.faces[i]]
            colors = self.vertex_colors[self.faces[i]][:, :3]
            mesh = TriangleMesh(vertices[0], vertices[1], vertices[2], colors[0], colors[1], colors[2], self.material)
            self.triangle_meshes.append(mesh)
            self.bounds.append(mesh.bound)

        print('\rCreating TriangleMeshes for the model: 100.0%')

        self.triangle_meshes = np.array(self.triangle_meshes)
        self.bounds = np.array(self.bounds)
