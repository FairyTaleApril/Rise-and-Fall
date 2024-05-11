import numpy as np
import trimesh

from RenderingPipeline.ModelTools.Material import *
from RenderingPipeline.ModelTools.TriangleMesh import TriangleMesh


class Meshes:
    def __init__(self, filepath=None, material=None):
        self.obj = None
        self.faces = None
        self.vertices = None
        self.vertex_colors = None  # 添加顶点颜色属性

        self.triangle_meshes = None
        self.bounds = None

        self.material = material

        if filepath is not None:
            self.read_obj(filepath)

    def read_obj(self, filepath):
        print('Start loading model ...')
        self.obj: trimesh.Trimesh = trimesh.load(filepath)
        print('Model file successfully loaded: ' + filepath)

        self.faces = self.obj.faces
        self.vertices = self.obj.vertices
        # get color
        self.vertex_colors = self.obj.visual.vertex_colors

        self.create_meshes()

    def create_meshes(self):
        print('Start creating TriangleMeshes for the model ...')

        self.triangle_meshes = []
        self.bounds = []

        num_faces = len(self.faces)
        for i in range(num_faces):
            print('\rProcess: {:.1f}%'.format(100 * i / num_faces), end='')
            if self.vertex_colors is not None:
                colors = self.vertex_colors[self.faces[i]]  # 获取三个顶点的颜色
            mesh = TriangleMesh(self.vertices[self.faces[i][0]], self.vertices[self.faces[i][1]],
                                self.vertices[self.faces[i][2]], colors[0], colors[1], colors[2], self.material)
            self.triangle_meshes.append(mesh)
            self.bounds.append(mesh.bound)
        print('\rProcess: 100.0%')

        self.triangle_meshes = np.array(self.triangle_meshes)
        self.bounds = np.array(self.bounds)

        print('TriangleMeshes successfully created')

    def set_material(self, material):
        self.material = material
