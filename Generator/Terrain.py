import cv2
import numpy as np

from Noise import Noise
from Global import *


class Terrain:
    def __init__(self, latitude, longitude, types, seed=1):
        self.latitude = latitude
        self.longitude = longitude

        self.octaves_list = np.array([4, 8, 16, 32, 64])
        self.frequency_list = np.array([1.5, 3, 6, 12, 24])
        self.amplitude_list = np.array([2, 0.5, 0.125, 0.125, 0.125])

        # types = [Deep, Shallow, Shore, Grass, Hill, Dirt, Mountain]
        self.types = types

        self.noises = []
        for i in range(len(self.octaves_list)):
            self.noises.append(Noise(seed, self.octaves_list[i], self.frequency_list[i], offset_x=0.0, offset_y=0.0))

        self.normalized_map = None
        self.terrain_map = None

    def generate(self):
        print('Generate Terrain map:')

        noise_map = np.zeros((self.latitude, self.longitude), dtype=float)
        for i in range(len(self.noises)):
            noise_map += self.amplitude_list[i] * self.noises[i].sphere_noise(self.latitude, self.longitude)

        normalized_map = map_value(noise_map)
        self.normalized_map = normalized_map.copy()

        for i in range(len(self.types) - 1):
            normalized_map[(normalized_map >= self.types[i]) & (normalized_map <= self.types[i + 1])] = -i
        self.terrain_map = normalized_map








