import numpy as np


def union_bound(bound1, bound2):
    if bound1 is None:
        return bound2
    elif bound2 is None:
        return bound1
    else:
        p_min = np.minimum(bound1.p_min, bound2.p_min)
        p_max = np.maximum(bound1.p_max, bound2.p_max)
        return Bound(p_min, p_max)


def union_bound_point(bound, point):
    if bound is None:
        return Bound(point, point)
    else:
        p_min = np.minimum(bound.p_min, point)
        p_max = np.maximum(bound.p_max, point)
        return Bound(p_min, p_max)


class Bound:
    def __init__(self, p_min=None, p_max=None):
        self.p_min = p_min
        self.p_max = p_max
    
    def get_centroid(self):
        return 0.5 * (self.p_min + self.p_max)

    def detect_intersect(self, ray):
        inv_dir = np.array([1.0 / ray.direction[0], 1.0 / ray.direction[1], 1.0 / ray.direction[2]])
        dir_is_neg = [int(ray.direction[i] > 0) for i in range(3)]

        t_enter = -np.inf
        t_exit = np.inf

        for i in range(3):
            min_value = (self.p_min[i] - ray.origin[i]) * inv_dir[i]
            max_value = (self.p_max[i] - ray.origin[i]) * inv_dir[i]

            if not dir_is_neg[i]:
                min_value, max_value = max_value, min_value

            t_enter = max(min_value, t_enter)
            t_exit = min(max_value, t_exit)

        return t_enter <= t_exit and t_exit >= 0

    def max_extent(self):
        d = self.p_max - self.p_min
        if d[0] > d[1] and d[0] > d[2]:
            return 0
        else:
            return 1 if d[1] > d[2] else 2
