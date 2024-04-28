import numpy as np


class Bound:
    def __init__(self, triangle):
        self.coords_min = np.array([min(triangle.v0[0], triangle.v1[0], triangle.v2[0]),
                                    min(triangle.v0[1], triangle.v1[1], triangle.v2[1]),
                                    min(triangle.v0[2], triangle.v1[2], triangle.v2[2])])
        self.coords_max = np.array([max(triangle.v0[0], triangle.v1[0], triangle.v2[0]),
                                    max(triangle.v0[1], triangle.v1[1], triangle.v2[1]),
                                    max(triangle.v0[2], triangle.v1[2], triangle.v2[2])])

    def get_centroid(self):
        return 0.5 * (self.coords_min + self.coords_max)

    def detect_intersect(self, ray, inv_dir, dir_is_neg):
        # TODO: delete inv_dir and dir_is_neg
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
