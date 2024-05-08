import numpy as np


class Sphere:
    def __init__(self, radius, num_segments):
        self.radius = radius
        self.num_segments = num_segments
        self.latitude = num_segments
        self.longitude = num_segments

        self.vertices_map = np.zeros((self.latitude, self.longitude, 3), dtype=float)
        self.vertices_list = []
        self.params = np.zeros((self.latitude, self.longitude, 2), dtype=float)
        self.faces = []

        for latitude in range(self.latitude):
            theta = latitude * np.pi / (self.longitude - 1)

            for longitude in range(self.longitude):
                phi = longitude * 2 * np.pi / self.longitude

                position = radius * np.array([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)])
                self.vertices_map[latitude, longitude] = position
                self.vertices_list.append(position)
                self.params[latitude, longitude] = np.array([theta, phi])

        for latitude in range(self.latitude - 1):
            for longitude in range(self.longitude):
                index = longitude + latitude * self.longitude + 1

                if longitude != self.longitude - 1:
                    self.faces.append([index + 1 + self.longitude, index + 1, index])
                    self.faces.append([index + self.longitude, index + 1 + self.longitude, index])
                else:
                    next_index = 1 + latitude * self.longitude
                    self.faces.append([index + self.longitude, next_index, index])
                    self.faces.append([index + self.longitude, next_index + self.longitude, next_index])
