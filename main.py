import numpy as np
import trimesh

from PerlinNoiseMap import PerlinNoiseMap
from RenderingPipeline.Render import *
from RenderingPipeline.Scene import *
from RenderingPipeline.ModelTools.Meshes import *


width = 500
height = 360

spp = 4


if __name__ == '__main__':
    # perlin_map = PerlinNoiseMap(width, height)
    # perlin_map.generate_map(max_height=200, frequency=2, gradient_scale=-1.0, persistence=0.1, lacunarity=2)
    # perlin_map.display_map()

    # terrain = Object()
    # terrain.set_obj_from_map(perlin_map.map)

    cow = Meshes()
    cow.read_obj('./Asset/Model/cow.obj')
    # cow.obj.show()

    scene = Scene(width, height, 90)
    scene.add(cow)

    render = Render(scene, np.array([0.0, 10.0, 0.0]), spp)
    render.render()

    # mesh = trimesh.Trimesh(vertices=cow.vertices, faces=cow.faces, face_colors=[100, 100, 100])
    # mesh.show()


