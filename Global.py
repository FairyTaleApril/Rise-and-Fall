import math
import numpy as np


epsilon = 1e-6


def normalize(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    else:
        return vector / norm


def deg2rad(deg):
    return deg * np.pi / 180.0


def lerp(v0, v1, t):
    return (1 - t) * v0 + t * v1


