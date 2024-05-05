import numpy as np
from enum import Enum
from PIL import Image


class MaterialType(Enum):
    Diffuse = 1
    Reflection_Refraction = 2


class Material:
    def __init__(self, material_type=MaterialType.Diffuse, color=np.array([100.0, 100.0, 100.0]),
                 ior=0.8, Ka=0.005, Kd=0.6, Ks=0.8, specular_exponent=100):
        self.material_type = material_type
        self.color = color

        self.ior = ior
        self.Ka = Ka
        self.Kd = Kd
        self.Ks = Ks
        self.specular_exponent = specular_exponent

        self.texture = None
        self.width = None
        self.height = None

    def set_texture(self, filepath):
        self.texture = Image.open(filepath)
        self.width, self.height = self.texture.size

    def get_color_at(self, u, v):
        if self.texture:
            # TODO: 双线性插值
            u_img = u * self.width
            v_img = (1 - v) * self.height

            u1, v1 = int(u_img), int(v_img)

            return self.texture[u1, v1]
        else:
            return self.color



