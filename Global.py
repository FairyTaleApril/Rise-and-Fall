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


def convert_map_to_3d(height_map: np.ndarray):
    height, width = height_map.shape
    half_height, half_width = int(height / 2), int(width / 2)

    vertices = []
    for y in range(height):
        for x in range(width):
            vertices.append(np.array([x - half_width, height_map[y, x], y - half_height]))
    vertices = np.array(vertices)

    faces = []
    for y in range(1, height):
        for x in range(1, width):
            index = x + (y - 1) * width
            faces.append(np.array([index, index + width, index + 1]))
            faces.append(np.array([index + 1, index + width, index + width + 1]))
    faces = np.array(faces)
    return vertices, faces


def save_model(filename, vertices, faces):
    with open(filename, 'w') as f:
        for vertex in vertices:
            f.write("v " + " ".join(str(v) for v in vertex) + "\n")

        for face in faces:
            f.write("f " + " ".join(str(f) for f in face) + "\n")


