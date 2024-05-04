import numpy as np
from enum import Enum
from PIL import Image


class MaterialType(Enum):
    Diffuse = 1
    Reflection_Refraction = 2


class Material:
    def __init__(self, material_type=MaterialType.Diffuse, color=np.array([1, 1, 1]), emission=np.array([0, 0, 0]), ior=1,
                 Ka=0.005, Ks=0.8, specular_exponent=100):
        self.material_type = material_type
        self.color = color
        self.emission = emission
        self.ior = ior
        self.Ka = Ka
        self.Ks = Ks
        self.specular_exponent = specular_exponent
        self.texture = None
        self.width = None
        self.height = None

    def set_texture(self, filepath):
        self.texture = Image.open(filepath)
        self.width, self.height = self.texture.size

    def get_color_at(self, u, v):

        u_img = u * self.width
        v_img = (1 - v) * self.height

        u_min = int(np.floor(u_img))
        u_max = int(np.ceil(u_img))
        v_min = int(np.floor(v_img))
        v_max = int(np.ceil(v_img))

        # Color_11 Color_12
        # Color_21 Color_22
        # in opencv, higher y in image->smaller v in texture
        color_11 = self.texture[v_min, u_min]
        color_12 = self.texture[v_min, u_max]
        color_21 = self.texture[v_max, u_min]
        color_22 = self.texture[v_max, u_max]

        color1 = (u_img - u_min) * color_11 + (u_max - u_img) * color_12
        color2 = (u_img - u_min) * color_21 + (u_max - u_img) * color_22

        color = (v_img - v_min) * color1 + (v_max - v_img) * color2

        self.color = color
        return self.color
        # return self.texture[u, v]



