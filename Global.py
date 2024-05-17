import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

epsilon = 1e-6

# # colors = [Deep, Shallow, Shore, Sand, Grass, Dirt, Rock, Snow]
# cmap_colors = [(0, 0, 0.5), (0, 0, 1), (0, 0.5, 1), (0.94, 0.94, 0.25),
#               (0.13, 0.63, 0), (0.88, 0.88, 0), (0.5, 0.5, 0.5), (1, 1, 1)]
# cmap_values = [0.0, 0.4, 0.5, 0.55, 0.7, 0.8, 0.95, 1.0]
# colors = [Deep, Shallow, Shore, Grass, Hill, Mountain]
cmap_colors = [(0, 0, 0.5), (0, 0, 1), (0, 0.5, 1), (0.94, 0.94, 0.25), (0.13, 0.63, 0), (0.5, 0.5, 0.5), (1, 1, 1)]
cmap_values = [0.0, 0.4, 0.5, 0.55, 0.75, 0.9, 1.0]
my_cmap = LinearSegmentedColormap.from_list('my_colormap', list(zip(cmap_values, cmap_colors)))


def normalize(vector):
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    else:
        return vector / norm


def map_value(_map, area=None, min_value=0, value_range=1):
    if area is None:
        lowest = np.min(_map)
        return (_map - lowest) / (np.max(_map) - lowest) * value_range + min_value
    else:
        lowest = np.min(_map[area])
        return (_map - lowest) / (np.max(_map[area]) - lowest) * value_range + min_value


def deg2rad(deg):
    return deg * np.pi / 180.0


def show_images(images, cmap=None):
    if len(images) == 1:
        plt.imshow(images[0], cmap=cmap)
        plt.colorbar()
    else:
        fig, axes = plt.subplots(len(images), 1)
        for index, image in enumerate(images):
            im = axes[index].imshow(image, cmap=cmap)
            fig.colorbar(im)
    plt.show()


def sphere_position(theta, phi, radius=1):
    return radius * np.array([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)])


def map_color(values, cmap=my_cmap):
    normalized_values = (values - np.min(values)) / (np.max(values) - np.min(values))
    colors = (255.0 * np.array(cmap(normalized_values)[:, :3])).astype(int)
    return colors


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


def save_ply(filename, vertices, faces, vertex_colors=None):
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


def save_obj(filename, vertices, faces):
    with open(filename, 'w') as f:
        for vertex in vertices:
            f.write("v {} {} {}\n".format(vertex[0], vertex[1], vertex[2]))

        for face in faces:
            f.write("f")
            for vertex_index in face:
                f.write(" {}".format(vertex_index))
            f.write("\n")


def to_list(_map):
    height, width = _map.shape[:2]
    _list = []

    for y in range(height):
        for x in range(width):
            _list.append(_map[y, x].tolist())

    return _list
