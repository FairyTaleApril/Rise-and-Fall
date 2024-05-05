import numpy as np

from Global import *
from RenderingPipeline.ModelTools.Meshes import *
from RenderingPipeline.RayTracingTools.Bound import *
from RenderingPipeline.RayTracingTools.BVH import *
from RenderingPipeline.RayTracingTools.Intersection import *


class TriangleMesh:
    def __init__(self, v0, v1, v2, material, N=None):
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.material = material

        self.e1 = v1 - v0
        self.e2 = v2 - v0
        self.N = normalize(np.cross(self.e1, self.e2))

        self.area = 0.5 * np.linalg.norm(np.cross(self.e1, self.e2))

        p_min = np.minimum(np.minimum(v0, v1), v2)
        p_max = np.maximum(np.maximum(v0, v1), v2)
        self.bound = Bound(p_min, p_max)

    def detect_intersect(self, ray):
        inter = Intersection()

        ray_cross_e2 = np.cross(ray.direction, self.e2)
        det = np.dot(self.e1, ray_cross_e2)

        if abs(det) < epsilon:
            return inter

        inv_det = 1.0 / det
        s = ray.origin - self.v0
        u = inv_det * np.dot(s, ray_cross_e2)

        if u < 0 or u > 1:
            return inter

        s_cross_e1 = np.cross(s, self.e1)
        v = inv_det * np.dot(ray.direction, s_cross_e1)

        if v < 0 or u + v > 1:
            return inter

        t = inv_det * np.dot(self.e2, s_cross_e1)

        if t > epsilon:
            inter.happened = True
            inter.t = t
            inter.coords = ray.point(t)
            inter.N = self.N
            inter.triangle_mesh = self
            inter.material = self.material
            inter.uv_coords = [u, v]
        return inter
