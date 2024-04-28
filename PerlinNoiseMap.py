import numpy as np
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def logistic(height_map: np.ndarray):
    lowest = np.min(height_map)
    altitude_range = np.max(height_map) - lowest
    return 1 / (1 + np.e ** (4 - 3 * (height_map - lowest) / altitude_range))


def linear(height_map: np.ndarray):
    return height_map


class PerlinNoiseMap:
    def __init__(self, width, height, octaves_list=None, seed=1):
        self.width = width
        self.height = height

        self.noise = []
        if octaves_list is None:
            octaves_list = [3, 6, 12]
            # octaves_list = [3, 6, 12, 24]
        for octaves in octaves_list:
            self.noise.append(PerlinNoise(octaves=octaves, seed=seed))

        self.map = None
        self.terrain_colors = 'terrain'

    def generate_map(self, max_height, frequency=1, gradient_scale=1.0, persistence=0.5, lacunarity=2.0, func=logistic):
        amplitude = 1
        frequency = frequency

        self.map = np.zeros((self.height, self.width))

        gradient_magnitude_list = []
        for noise in self.noise:
            # TODO: Show progress
            noise_map = np.zeros((self.height, self.width))
            for y in range(self.height):
                for x in range(self.width):
                    sample_y = y * frequency / self.height
                    sample_x = x * frequency / self.width

                    perlin_value = amplitude * noise([sample_y, sample_x])
                    noise_map[y, x] += perlin_value

            gradient_x, gradient_y = np.gradient(noise_map)
            gradient_magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
            gradient_magnitude_list.append(gradient_magnitude)

            reduce_map = 1 / (1 + gradient_scale * np.sum(gradient_magnitude_list, axis=0))

            self.map += (noise_map - reduce_map) / len(self.noise)

            amplitude *= persistence
            frequency *= lacunarity

        self.map = max_height * func(self.map)

    def display_map(self):
        plt.imshow(self.map, cmap=self.terrain_colors)
        plt.colorbar()
        plt.show()

    def set_terrain_colors(self, terrain_colors):
        self.terrain_colors = ListedColormap(terrain_colors)

