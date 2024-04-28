import numpy as np

from Global import *
from RenderingPipeline.Light.Light import *
from RenderingPipeline.ModelTools.Object import *
from RenderingPipeline.ModelTools.Material import *
from RenderingPipeline.RayTracingTools.Intersection import *


class Scene:
    def __init__(self, width, height, fov):
        self.width = width
        self.height = height
        self.fov = fov
        self.max_depth = 5
        self.objects = []
        self.lights = []
        self.bvh = None

    def add(self, obj):
        if isinstance(obj, Object):
            self.objects.append(obj)
        elif isinstance(obj, Light):
            self.lights.append(obj)

    def cast_ray(self, ray, depth):
        if depth > self.max_depth:
            return np.array([0, 0, 0], dtype=np.float32)

        inter = self.bvh.detext_intersect(ray)

        if inter.happened:
            material = inter.obj.material
            if material.material_type is MaterialType.Diffuse:
                if material:
                    texture_color = material.get_color_at(inter.uv_coords[0], inter.uv_coords[1])
                else:
                    texture_color = np.array([0, 0, 0], dtype=np.float32)

                Ka = material.Ka
                Kd = texture_color / 255.0
                Ks = material.Ks

                amb_light_intensity = np.array([10.0, 10.0, 10.0])
                La = Ka * amb_light_intensity
                result_color = La

                for light in self.lights:
                    l = normalize(light.coords - inter.coords)
                    I_r2 = light.intensity / (np.linalg.norm(light.coords - inter.coords) ** 2)
                    Ld = Kd * I_r2 * max(0.0, np.dot(inter.N, l))

                    h = normalize(ray.direction + l)
                    Ls = Ks * I_r2 * max(0.0, np.dot(inter.N, h)) **material.specular_exponent

                    result_color += Ld + Ls
                return result_color

