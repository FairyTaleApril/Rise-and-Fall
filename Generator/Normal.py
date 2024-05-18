import numpy as np

from Noise import Noise
from Global import *


class Normal:
    def __init__(self, latitude, longitude, seed=1):
        self.latitude = latitude
        self.longitude = longitude

        self.octaves_list = np.array([4, 8, 16, 32, 64])
        self.frequency_list = np.array([2, 2.5, 3, 3.5, 4])
        self.amplitude_list = np.array([1, 0.75, 0.5, 0.25, 0.1])

        self.noises = []
        for i in range(len(self.octaves_list)):
            self.noises.append(Noise(seed, self.octaves_list[i], self.frequency_list[i], offset_x=0.0, offset_y=0.0))

        self.normalized_map = None

    def generate(self):
        print('Generate Normal map:')

        noise_map = np.zeros((self.latitude, self.longitude), dtype=float)
        for i in range(len(self.noises)):
            noise_map += self.amplitude_list[i] * \
                         np.sin(self.noises[i].sphere_noise(self.latitude, self.longitude) * np.pi / 2)
        self.normalized_map = map_value(noise_map)
