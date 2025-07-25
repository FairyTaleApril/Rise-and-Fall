import numpy as np


class Ray:
    def __init__(self, origin: np.ndarray, direction: np.ndarray):
        self.origin = origin
        self.direction = direction

    def point(self, t):
        return self.origin + t * self.direction
