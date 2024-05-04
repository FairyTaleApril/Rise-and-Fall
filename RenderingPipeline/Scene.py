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

    def build_BVH(self):
        self.bvh = BVH(self.objects, 1, SplitMethod.NAIVE)

    def cast_ray(self, ray: Ray, depth):
        if depth > self.max_depth:
            return np.array([0, 0, 0], dtype=np.float32)

        inter = self.bvh.detext_intersect(ray)

        if inter.happened:
            if inter.material.material_type is MaterialType.Diffuse:
                if inter.material.texture:
                    texture_color = inter.material.get_color_at(inter.uv_coords[0], inter.uv_coords[1])
                else:
                    texture_color = np.array([0, 0, 0], dtype=np.float32)

                Ka = inter.material.Ka
                Kd = texture_color / 255.0
                Ks = inter.material.Ks

                amb_light_intensity = np.array([10.0, 10.0, 10.0])
                La = Ka * amb_light_intensity
                result_color = La

                # TODO: Shadow
                for light in self.lights:
                    l = normalize(light.coords - inter.coords)
                    I_r2 = light.intensity / (np.linalg.norm(light.coords - inter.coords) ** 2)
                    Ld = Kd * I_r2 * max(0.0, float(np.dot(inter.N, l)))

                    h = normalize(ray.direction + l)
                    Ls = Ks * I_r2 * max(0.0, float(np.dot(inter.N, h))) ** inter.material.specular_exponent

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
