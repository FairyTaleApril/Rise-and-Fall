import numpy as np
from enum import Enum
from PIL import Image


class MaterialType(Enum):
    Diffuse = 1


class Material:
    def __init__(self, material_type=MaterialType.Diffuse, emission=np.array([0, 0, 0]), ior=1,
                 Ka=0.005, Ks=0.8, specular_exponent=100):
        self.material_type = material_type
        self.emission = emission
        self.ior = ior
        self.Ka = Ka
        self.Ks = Ks
        self.specular_exponent = specular_exponent
        self.texture = None

    def set_texture(self, filepath):
        self.texture = Image.open(filepath)

    def get_color_at(self, u, v):
        # TODO Bilinear interpolation
        return self.texture[u, v]

