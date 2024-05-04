import numpy as np

from RenderingPipeline.RayTracingTools.Intersection import *


class Bound:
    def __init__(self, triangle):
        self.coords_min = np.array([min(triangle.v0[0], triangle.v1[0], triangle.v2[0]),
                                    min(triangle.v0[1], triangle.v1[1], triangle.v2[1]),
                                    min(triangle.v0[2], triangle.v1[2], triangle.v2[2])])
        self.coords_max = np.array([max(triangle.v0[0], triangle.v1[0], triangle.v2[0]),
                                    max(triangle.v0[1], triangle.v1[1], triangle.v2[1]),
                                    max(triangle.v0[2], triangle.v1[2], triangle.v2[2])])
        self.pMin = None
        self.pMax = None

    
    def bound3(self, p1, p2):
        self.pMin = np.array([min(p1[0], p2[0]), min(p1[1], p2[1]), min(p1[2], p2[2])])
        self.pMax = np.array([max(p1[0], p2[0]), max(p1[1], p2[1]), max(p1[2], p2[2])])

    
    def get_centroid(self):
        return 0.5 * (self.coords_min + self.coords_max)

    
    def detect_intersect(self, ray):
        inter = Intersection()

        # Calculate inv_dir and dir_is_neg from ray direction
        inv_dir = np.array([1.0 / ray.direction[0], 1.0 / ray.direction[1], 1.0 / ray.direction[2]])
        dir_is_neg = [int(ray.direction[i] > 0) for i in range(3)]

        t_enter = -np.inf
        t_exit = np.inf

        for i in range(3):
            min_value = (self.coords_min[i] - ray.origin[i]) * inv_dir[i]
            max_value = (self.coords_max[i] - ray.origin[i]) * inv_dir[i]
            if not dir_is_neg[i]:
                min_value, max_value = max_value, min_value
            t_enter = max(min_value, t_enter)
            t_exit = min(max_value, t_exit)

        return t_enter <= t_exit and t_exit >= 0

    
    def diagonal(self):
        return self.pMax - self.pMin


    def max_extent(self):
        d = self.diagonal()
        if d[0] > d[1] and d[0] > d[2]:
            return 0
        elif d[1] > d[2]:
            return 1
        else:
            return 2

    
    def intersect(self, other):
        p_min = np.maximum(self.coords_min, other.coords_min)
        p_max = np.minimum(self.coords_max, other.coords_max)
        return Bound(p_min, p_max)

    
    def offset(self, point):
        o = point - self.coords_min
        if np.any(self.coords_max > self.coords_min):
            o /= self.coords_max - self.coords_min
        return o

    
    def overlaps(self, other):
        x = (self.coords_max[0] >= other.coords_min[0]) and (self.coords_min[0] <= other.coords_max[0])
        y = (self.coords_max[1] >= other.coords_min[1]) and (self.coords_min[1] <= other.coords_max[1])
        z = (self.coords_max[2] >= other.coords_min[2]) and (self.coords_min[2] <= other.coords_max[2])
        return x and y and z

    
    def inside(self, point):
        return np.all(point >= self.coords_min) and np.all(point <= self.coords_max)

    
    def union(b1, b2):
        p_min = np.minimum(b1.pMin, b2.pMin)
        p_max = np.maximum(b1.pMax, b2.pMax)
        return Bound(p_min, p_max)

    
    def union_with_point(b, p):
        p_min = np.minimum(b.pMin, p)
        p_max = np.maximum(b.pMax, p)
        return Bound(p_min, p_max)
