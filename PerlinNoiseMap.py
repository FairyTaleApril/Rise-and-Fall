import numpy as np
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


class PerlinNoiseMap:
    def __init__(self, width, height, octaves_list=None, seed=1):
        self.__width = width
        self.__height = height

        self.__noise = []
        if octaves_list is None:
            octaves_list = [3, 6, 12, 24]
        for octaves in octaves_list:
            self.__noise.append(PerlinNoise(octaves=octaves, seed=seed))

        self.__map = None
        self.__terrain_colors = 'terrain'

    def generate_map(self, persistence=0.5, lacunarity=2.0):
        amplitude = 1
        frequency = 1

        self.__map = np.zeros((self.__height, self.__width))
        for noise in self.__noise:
            for y in range(self.__height):
                for x in range(self.__width):
                    sample_y = y * frequency / self.__height
                    sample_x = x * frequency / self.__width

                    self.__map[y, x] += amplitude * noise([sample_y, sample_x])

            amplitude *= persistence
            frequency *= lacunarity

    def get_map(self):
        return self.__map

    def display_map(self):
        plt.imshow(self.__map, cmap=self.__terrain_colors)
        plt.show()

    def set_terrain_colors(self, terrain_colors):
        self.__terrain_colors = ListedColormap(terrain_colors)

