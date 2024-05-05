import os
import threading
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

        self.progress = 0

    def generate_map(self, max_height, frequency=1, gradient_scale=1.0, persistence=0.5, lacunarity=2.0, func=linear):
        amplitude = 1
        frequency = frequency

        self.map = np.zeros((self.height, self.width))
        gradient_magnitude_list = []

        self.progress = 0

        for noise in self.noise:
            num_threads = min(os.cpu_count(), 8)
            rows = self.height // num_threads + 1
            workers = []

            noise_map = np.zeros((self.height, self.width))

            for i in range(num_threads):
                y0 = i * rows
                y1 = min(y0 + rows, self.height)
                worker = threading.Thread(target=self.generate_map_thread,
                                          args=(y0, y1, noise, noise_map, frequency, amplitude))
                workers.append(worker)
                worker.start()

            for worker in workers:
                worker.join()

            gradient_x, gradient_y = np.gradient(noise_map)
            gradient_magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
            gradient_magnitude_list.append(gradient_magnitude)

            reduce_map = 1 / (1 + gradient_scale * np.sum(gradient_magnitude_list, axis=0))
            self.map += (noise_map - reduce_map) / len(self.noise)

            amplitude *= persistence
            frequency *= lacunarity

        self.map = max_height * func(self.map)

    def generate_map_thread(self, y0, y1, noise, noise_map, frequency, amplitude):
        for y in range(y0, y1):
            for x in range(self.width):
                sample_y = y * frequency / self.height
                sample_x = x * frequency / self.width

                perlin_value = amplitude * noise([sample_y, sample_x])
                noise_map[y, x] += perlin_value

            self.update_progress()

    def update_progress(self):
        self.progress += 1
        percentage = 100 * self.progress / (len(self.noise) * self.height)
        if percentage == 100:
            print('\rGenerate map progress: 100.0%', flush=True)
        else:
            print('\rGenerate map progress: {:.1f}%'.format(percentage), end='', flush=True)

    def display_map(self):
        plt.imshow(self.map, cmap=self.terrain_colors)
        plt.colorbar()
        plt.show()

    def set_terrain_colors(self, terrain_colors):
        self.terrain_colors = ListedColormap(terrain_colors)
