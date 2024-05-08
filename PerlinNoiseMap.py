import os
import threading
import numpy as np
from perlin_noise import PerlinNoise
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from RenderingPipeline.ModelTools.Sphere import Sphere


def logistic(height_map: np.ndarray):
    lowest = np.min(height_map)
    altitude_range = np.max(height_map) - lowest
    return 1 / (1 + np.e ** (4 - 3 * (height_map - lowest) / altitude_range))


def linear(height_map: np.ndarray):
    lowest = np.min(height_map)
    altitude_range = np.max(height_map) - lowest
    return (height_map - lowest) / altitude_range


class PerlinNoiseGenerator:
    def __init__(self, octaves_list=None, seed=1):
        self.noise = []
        if octaves_list is None:
            octaves_list = [3, 6, 12, 24]
        for octaves in octaves_list:
            self.noise.append(PerlinNoise(octaves=octaves, seed=seed))

        self.terrain_colors = 'terrain'

        self.progress = 0

    def generate_map(self, width, height, max_height, min_height, func=logistic,
                     frequency=1, gradient_scale=1.0, persistence=0.1, lacunarity=2.0):
        print('Start generating map ...')

        amplitude = 1
        frequency = frequency

        terrain_map = np.zeros((height, width))
        gradient_magnitude_list = []

        self.progress = 0

        for noise in self.noise:
            num_threads = min(os.cpu_count(), 8)
            rows = height // num_threads + 1
            workers = []

            noise_map = np.zeros((height, width))

            for i in range(num_threads):
                y0 = i * rows
                y1 = min(y0 + rows, height)
                worker = threading.Thread(target=self.generate_map_thread,
                                          args=(y0, y1, width, height, noise, noise_map, frequency, amplitude))
                workers.append(worker)
                worker.start()

            for worker in workers:
                worker.join()

            gradient_x, gradient_y = np.gradient(noise_map)
            gradient_magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
            gradient_magnitude_list.append(gradient_magnitude)

            reduce_map = 1 / (1 + gradient_scale * np.sum(gradient_magnitude_list, axis=0))
            terrain_map += (noise_map - reduce_map) / len(self.noise)

            amplitude *= persistence
            frequency *= lacunarity

        terrain_map = (max_height - min_height) * func(terrain_map) + min_height

        print('Map successfully generated')
        return terrain_map

    def generate_map_thread(self, y0, y1, width, height, noise, noise_map, frequency, amplitude):
        for y in range(y0, y1):
            for x in range(width):
                sample_y = y * frequency / height
                sample_x = x * frequency / width

                perlin_value = amplitude * noise([sample_y, sample_x])
                noise_map[y, x] += perlin_value

            self.update_progress((len(self.noise) * height))

    def generate_planet(self, sphere: Sphere, max_height, min_height, func=logistic,
                        frequency=1, gradient_scale=1.0, persistence=0.1, lacunarity=2.0):
        print('Start generating planet ...')

        amplitude = 1
        frequency = frequency
        gradient_magnitude_list = []
        radius_increments_list = []

        self.progress = 0

        for noise in self.noise:
            num_threads = min(os.cpu_count(), 8)
            latitudes = sphere.latitude // num_threads + 1
            workers = []

            radius_increments = np.zeros(sphere.vertices_map.shape[:2], dtype=float)

            for i in range(num_threads):
                l0 = i * latitudes
                l1 = min(l0 + latitudes, sphere.latitude)
                worker = threading.Thread(target=self.generate_planet_thread,
                                          args=(l0, l1, sphere, radius_increments, noise, frequency, amplitude))
                workers.append(worker)
                worker.start()

            for worker in workers:
                worker.join()

            gradient_x, gradient_y = np.gradient(radius_increments)
            gradient_magnitude = np.sqrt(gradient_x ** 2 + gradient_y ** 2)
            gradient_magnitude_list.append(gradient_magnitude)

            reduce_map = 1 / (1 + gradient_scale * np.sum(gradient_magnitude_list, axis=0))
            radius_increments = (radius_increments - reduce_map) / len(self.noise)
            radius_increments_list.append(radius_increments)

            amplitude *= persistence
            frequency *= lacunarity

        radius_increments = np.sum(np.array(radius_increments_list), axis=0)
        radii = (max_height - min_height) * func(sphere.radius + radius_increments) + min_height
        for latitude in range(sphere.latitude):
            for longitude in range(sphere.longitude):
                position = radii[latitude, longitude] * np.array(
                    [np.sin(sphere.params[latitude, longitude, 0]) * np.cos(sphere.params[latitude, longitude, 1]),
                     np.sin(sphere.params[latitude, longitude, 0]) * np.sin(sphere.params[latitude, longitude, 1]),
                     np.cos(sphere.params[latitude, longitude, 0])])

                sphere.vertices_map[latitude, longitude] = position
                sphere.vertices_list[longitude + latitude * sphere.longitude] = position

        print('Planet successfully generated')

    def generate_planet_thread(self, l0, l1, sphere, radius_increments, noise, frequency, amplitude):
        for latitude in range(l0, l1):
            for longitude in range(sphere.longitude):
                sample_y = sphere.vertices_map[latitude, longitude, 0] * frequency / sphere.radius
                sample_x = sphere.vertices_map[latitude, longitude, 1] * frequency / sphere.radius
                sample_z = sphere.vertices_map[latitude, longitude, 2] * frequency / sphere.radius

                perlin_value = amplitude * noise([sample_y, sample_x, sample_z])
                radius_increments[latitude, longitude] = perlin_value

            self.update_progress(len(self.noise) * sphere.latitude)

    def update_progress(self, num):
        self.progress += 1
        percentage = 100 * self.progress / num
        if percentage == 100:
            print('\rProgress: 100.0%')
        else:
            print('\rProgress: {:.1f}%'.format(percentage), end='')

    def display_map(self, terrain_map):
        plt.imshow(terrain_map, cmap=self.terrain_colors)
        plt.colorbar()
        plt.show()

    def set_terrain_colors(self, terrain_colors):
        self.terrain_colors = ListedColormap(terrain_colors)
