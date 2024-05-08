import math
import numpy as np
import matplotlib.cm as cm

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


def save_model(filename, vertices, faces, vertex_colors=None):
    num_vertices = len(vertices)
    num_faces = len(faces)

    with open(filename, 'w') as f:
        f.write("ply\n")
        f.write("format ascii 1.0\n")
        f.write("element vertex {}\n".format(num_vertices))
        f.write("property float x\n")
        f.write("property float y\n")
        f.write("property float z\n")
        if vertex_colors is not None:
            f.write("property uchar red\n")
            f.write("property uchar green\n")
            f.write("property uchar blue\n")
        f.write("element face {}\n".format(num_faces))
        f.write("property list uchar int vertex_index\n")
        f.write("end_header\n")

        if vertex_colors is not None:
            for i in range(num_vertices):
                x, y, z = vertices[i]
                r, g, b = vertex_colors[i]
                f.write("{} {} {} {} {} {}\n".format(x, y, z, int(r), int(g), int(b)))
        else:
            for vertex in vertices:
                x, y, z = vertex
                f.write("{} {} {}\n".format(x, y, z))

        for face in faces:
            num_vertices_in_face = len(face)
            f.write("{} ".format(num_vertices_in_face))
            for vertex_index in face:
                f.write("{} ".format(vertex_index))
            f.write("\n")


def map_2_list(_map):
    height, width = _map.shape[:2]
    _list = []

    for y in range(height):
        for x in range(width):
            _list.append(_map[y, x].tolist())

    return _list


def value_2_color(values):
    cmap_terrain = cm.get_cmap('terrain')
    normalized_values = (values - np.min(values)) / (np.max(values) - np.min(values))
    colors = (255 * np.array(cmap_terrain(normalized_values)[:, :3])).astype(int)
    return colors
