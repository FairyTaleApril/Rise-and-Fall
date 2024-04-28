import numpy as np
import trimesh


class Object:
    def __init__(self):
        self.obj = None
        self.faces = None
        self.vertices = None

        self.bound = None

    def read_obj(self, filepath):
        self.obj = trimesh.load(filepath)

    def set_obj(self, obj):
        self.obj = obj

    def set_obj_from_map(self, terrain_map: np.ndarray):
        height, width = terrain_map.shape
        lowest = np.min(terrain_map)
        highest = np.max(terrain_map)

        with open('Asset/Model/terrain.obj', 'w') as f:
            for row in range(height):
                for col in range(width):
                    # altitude = 20 / (1 + np.e ** (5.5 - 8 * (terrain_map[row, col] - lowest) / (highest - lowest)))
                    altitude = terrain_map[row, col]
                    f.write('v ' + str(col) + ' ' + str(altitude) + ' ' + str(row) + '\n')

            for row in range(height - 1):
                for col in range(width - 1):
                    index = col + row * width + 1
                    f.write('f ' + str(index) + ' ' + str(index + width) + ' ' + str(index + 1) + '\n')
                    f.write('f ' + str(index + 1) + ' ' + str(index + width) + ' ' + str(index + width + 1) + '\n')
        f.close()

        self.obj = trimesh.load('Asset/Model/terrain.obj')
        self.obj.show()


