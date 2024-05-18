import numpy as np
from enum import Enum
from noise import pnoise3, snoise3

from Global import *


class NoiseType(Enum):
    perlin = 0
    simple = 1


class Noise:
    def __init__(self, seed, octaves, frequency=70, offset_x=0.0, offset_y=0.0, noise_type=NoiseType.perlin):
        self.seed = seed
        self.octaves = octaves
        self.frequency = frequency
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.noise_type = noise_type

    def sphere_noise(self, latitude=100, longitude=100, sample_radius=1):
        sample_radius = sample_radius * self.frequency
        noise_map = np.zeros((latitude, longitude), dtype=float)

        for y in range(latitude):
            print('\rGenerating map: {:.1f}%'.format(100 * y / latitude), end='')
            theta = y * np.pi / latitude
            for x in range(longitude):
                phi = x * 2 * np.pi / longitude
                position = sphere_position(theta, phi, sample_radius)

                if self.noise_type is NoiseType.perlin:
                    perlin_value = pnoise3(position[0], position[1], position[2], octaves=self.octaves, base=self.seed)
                else:
                    perlin_value = snoise3(position[0], position[1], position[2], octaves=self.octaves)
                noise_map[y, x] = perlin_value

        print('\rGenerating map: 100.0%')
        return noise_map
