import numpy as np

from Noise import Noise
from Global import *


class Hill:
    def __init__(self, latitude, longitude, seed=1):
        self.latitude = latitude
        self.longitude = longitude

        self.octaves_list = np.array([4, 8, 16, 32])
        self.frequency_list = np.array([4, 8, 16, 32])
        self.amplitude_list = np.array([1, 0.5, 0.25, 0.125])

        self.noises = []
        for i in range(len(self.octaves_list)):
            self.noises.append(Noise(seed, self.octaves_list[i], self.frequency_list[i], offset_x=0.0, offset_y=0.0))

        self.normalized_map = None

    def generate(self):
        print('Generate Hill map:')

        noise_map = np.zeros((self.latitude, self.longitude), dtype=float)
        for i in range(len(self.noises)):
            noise_map += self.amplitude_list[i] * self.noises[i].sphere_noise(self.latitude, self.longitude)
        noise_map = np.sin(map_value(noise_map) * np.pi / 2)
        self.normalized_map = map_value(noise_map)
