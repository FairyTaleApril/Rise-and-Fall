import numpy as np

from Global import *


class Sphere:
    def __init__(self, latitude, longitude, radius):
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius

        self.vertices_map = np.zeros((self.latitude, self.longitude, 3), dtype=float)
        self.params = np.zeros((self.latitude, self.longitude, 2), dtype=float)
        self.faces = []
        self.radii = self.radius * np.ones((self.latitude, self.longitude), dtype=float)
        self.vertex_colors = np.zeros((self.latitude, self.longitude, 3), dtype=float)

        for latitude in range(self.latitude):
            theta = latitude * np.pi / (self.latitude - 1)

            for longitude in range(self.longitude):
                phi = longitude * 2 * np.pi / self.longitude

                self.vertices_map[latitude, longitude] = sphere_position(theta, phi, radius)
                self.params[latitude, longitude] = np.array([theta, phi])

        for latitude in range(self.latitude - 1):
            for longitude in range(self.longitude):
                index = longitude + latitude * self.longitude

                if longitude != self.longitude - 1:
                    self.faces.append([index + 1 + self.longitude, index + 1, index])
                    self.faces.append([index + self.longitude, index + 1 + self.longitude, index])
                else:
                    next_index = latitude * self.longitude
                    self.faces.append([index + self.longitude, next_index, index])
                    self.faces.append([index + self.longitude, next_index + self.longitude, next_index])

    def compute_vertices_position(self, height_map=None):
        radii = self.radii if height_map is None else height_map

        for latitude in range(self.latitude):
            for longitude in range(self.longitude):
                position = sphere_position(self.params[latitude, longitude, 0], self.params[latitude, longitude, 1],
                                           radii[latitude, longitude])
                self.vertices_map[latitude, longitude] = position

    def compute_vertices_color(self, normalized_map=None):
        if normalized_map is None:
            normalized_map = (self.radii - np.min(self.radii)) / (np.max(self.radii) - np.min(self.radii))

        for latitude in range(self.latitude):
            for longitude in range(self.longitude):
                self.vertex_colors[latitude, longitude] = my_cmap(normalized_map[latitude, longitude])[:3]
        self.vertex_colors = (255 * self.vertex_colors).astype(int)
