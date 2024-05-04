import numpy as np
import trimesh

from PerlinNoiseMap import PerlinNoiseMap
from RenderingPipeline.Scene import *
from RenderingPipeline.ModelTools.Object import *


width = 500
height = 360


if __name__ == '__main__':
    perlin_map = PerlinNoiseMap(width, height)
    perlin_map.generate_map(max_height=200, frequency=2, gradient_scale=-1.0, persistence=0.1, lacunarity=2)
    perlin_map.display_map()

    # terrain = Object()
    # terrain.set_obj_from_map(perlin_map.map)

    # scene = Scene(width, height, 90)

    # cow = Object()
    # cow.read_obj('./Asset/Model/cow.obj')
    # cow.obj.show()

    # v = [[0, 0, 0], [10, 0, 0], [0, 10, 0]]
    # f = [[0, 1, 2]]
    # mesh = trimesh.Trimesh(vertices=v, faces=f, face_colors=[0, 0, 0])
    # mesh.show()


