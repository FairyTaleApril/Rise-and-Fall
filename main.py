import numpy as np
import trimesh

from PerlinNoiseMap import PerlinNoiseMap
from RenderingPipeline.Scene import *
from RenderingPipeline.ModelTools.Object import *


width = 300
height = 200


if __name__ == '__main__':
    perlin_map = PerlinNoiseMap(width, height)
    perlin_map.generate_map()
    perlin_map.display_map()

    scene = Scene(width, height, 90)

    # cow = Object()
    # cow.read_obj('./Asset/Model/cow.obj')
    # cow.obj.show()

    # v = [[0, 0, 0], [10, 0, 0], [0, 10, 0]]
    # f = [[0, 1, 2]]
    # mesh = trimesh.Trimesh(vertices=v, faces=f, face_colors=[0, 0, 0])
    # mesh.show()


