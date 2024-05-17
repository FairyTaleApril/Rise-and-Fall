import numpy as np

from Global import *
from RenderingPipeline.Light.Light import *
from RenderingPipeline.ModelTools.Meshes import *
from RenderingPipeline.ModelTools.Material import *
from RenderingPipeline.RayTracingTools.BVH import *
from RenderingPipeline.RayTracingTools.Ray import *
from RenderingPipeline.RayTracingTools.Intersection import *


def reflect(I, N):
    return I - 2 * np.dot(I, N) * N


def refract(I: np.ndarray, N: np.ndarray, ior):
    cos_i = max(-1.0, min(1.0, float(np.dot(I, N))))
    eta_i, eta_t = 1, ior
    n = N

    if cos_i < 0:
        cos_i = -cos_i
    else:
        eta_i, eta_t = eta_t, eta_i
        n = -N

    eta = eta_t / eta_t
    k = 1 - (1 - cos_i ** 2) * eta ** 2
    return 0 if k < 0 else eta * I + (eta * cos_i - math.sqrt(k)) * n


def fresnel(I, N, ior):
    cos_i = max(-1.0, min(1.0, float(np.dot(I, N))))
    eta_i, eta_t = 1, ior

    if cos_i > 0:
        eta_i, eta_t = eta_t, eta_i

    sin_t = eta_i / eta_t * math.sqrt(max(0.0, 1 - cos_i ** 2))
    if sin_t >= 1:
        return 1
    else:
        cos_t = math.sqrt(max(0.0, 1 - sin_t ** 2))
        cos_i = abs(cos_i)
        Rs = ((eta_t * cos_i) - (eta_i * cos_t)) / ((eta_t * cos_i) + (eta_i * cos_t))
        Rp = ((eta_i * cos_i) - (eta_t * cos_t)) / ((eta_i * cos_i) + (eta_t * cos_t))
        return (Rs ** 2 + Rp ** 2) / 2


class Scene:
    def __init__(self, height, width, fov, background_color=np.array([0.0, 0.0, 0.0])):
        self.height = height
        self.width = width
        self.fov = fov
        self.background_color = background_color

        self.max_depth = 4

        self.meshes_list = []
        self.lights = []
        self.bvh = None

    def add(self, meshes):
        if isinstance(meshes, Meshes):
            self.meshes_list.append(meshes)
        elif isinstance(meshes, Light):
            self.lights.append(meshes)

    def build_BVH(self):
        triangle_meshes = []
        for meshes in self.meshes_list:
            for triangle_mesh in meshes.triangle_meshes:
                triangle_meshes.append(triangle_mesh)
        self.bvh = BVH(triangle_meshes)

        print('BVH successfully built')

    def cast_ray(self, ray: Ray, depth):
        if depth > self.max_depth:
            return self.background_color

        inter: Intersection = self.bvh.detect_intersect(ray)

        if inter.happened:
            if inter.material.material_type is MaterialType.Diffuse:
                hit_point = inter.coords + inter.N * epsilon if np.dot(ray.direction, inter.N) < 0\
                    else inter.coords - inter.N * epsilon

                texture_color = inter.triangle_mesh.get_color_at(inter.uv_coords[0], inter.uv_coords[1])
                Kd = inter.material.Kd
                Ks = inter.material.Ks

                La = inter.material.Ka * texture_color / 255
                result_color = La

                for light in self.lights:
                    l = normalize(light.coords - inter.coords)

                    shadow_inter: Intersection = self.bvh.detect_intersect(Ray(hit_point, l))
                    if shadow_inter.happened:
                        continue

                    I_r2 = light.intensity / (np.linalg.norm(light.coords - inter.coords) ** 2)
                    Ld = Kd * I_r2 * max(0.0, float(np.dot(inter.N, l)))

                    h = normalize(ray.direction + l)
                    Ls = Ks * I_r2 * max(0.0, float(np.dot(inter.N, h))) ** inter.material.specular_exponent
                    # print(Ld + Ls)
                    result_color += Ld + Ls
                return result_color
            elif inter.material.material_type is MaterialType.Reflection_Refraction:
                reflection_dir = normalize(reflect(ray.direction, inter.N))
                reflection_origin = inter.coords - inter.N * epsilon if np.dot(reflection_dir, inter.N) < 0 \
                    else inter.coords + inter.N * epsilon
                reflection_color = self.cast_ray(Ray(reflection_origin, reflection_dir), depth + 1)

                refraction_dir = normalize(refract(ray.direction, inter.N, inter.material.ior))
                refraction_origin = inter.coords - inter.N * epsilon if np.dot(refraction_dir, inter.N) < 0 \
                    else inter.coords + inter.N * epsilon
                refraction_color = self.cast_ray(Ray(refraction_origin, refraction_dir), depth + 1)

                kr = fresnel(ray.direction, inter.N, inter.material.ior)
                return reflection_color * kr + refraction_color * (1 - kr)
        else:
            return self.background_color
