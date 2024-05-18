import os
import random
import threading
import matplotlib.pyplot as plt

from Global import *
from RenderingPipeline.RayTracingTools.Ray import *


def create_rotation_matrix(angle, axis):
    axis = normalize(axis)
    cos_theta = np.cos(np.radians(angle))
    sin_theta = np.sin(np.radians(angle))
    one_minus_cos = 1 - cos_theta
    x, y, z = axis

    rotation_matrix = np.array([
        [cos_theta + x*x*one_minus_cos, x*y*one_minus_cos - z*sin_theta, x*z*one_minus_cos + y*sin_theta],
        [y*x*one_minus_cos + z*sin_theta, cos_theta + y*y*one_minus_cos, y*z*one_minus_cos - x*sin_theta],
        [z*x*one_minus_cos - y*sin_theta, z*y*one_minus_cos + x*sin_theta, cos_theta + z*z*one_minus_cos]
    ])

    return rotation_matrix


class Render:
    def __init__(self, scene, eye_coords, spp):
        self.scene = scene
        self.eye_coords = eye_coords
        self.spp = spp

        self.scale = math.tan(deg2rad(scene.fov * 0.5))
        self.image_aspect_ratio = scene.width / scene.height

        self.frame_buffer = None

        self.progress = 0

    def render(self):
        self.frame_buffer = np.zeros((self.scene.height, self.scene.width, 3), dtype=np.float32)
        self.progress = 0

        num_threads = min(os.cpu_count(), 8)
        rows = self.scene.height // num_threads + 1
        workers = []

        for i in range(num_threads):
            y0 = i * rows
            y1 = min(y0 + rows, self.scene.height)
            worker = threading.Thread(target=self.render_thread, args=(y0, y1))
            workers.append(worker)
            worker.start()

        for worker in workers:
            worker.join()

        plt.figure('Scene')
        plt.imshow(self.frame_buffer)
        plt.show()

    def render_thread(self, y0, y1):
        for y in range(y0, y1):
            for x in range(self.scene.width):
                for k in range(self.spp):
                    # TODO: 视角变换
                    sample_x = (2 * (x + random.random()) / self.scene.width - 1) * self.image_aspect_ratio * self.scale
                    sample_y = (1 - 2 * (y + random.random()) / self.scene.height) * self.scale
                    direction = normalize(np.array([sample_x, sample_y, 1]))
                    # rotated_direction = normalize(self.rotation_matrix @ direction)

                    ray = Ray(self.eye_coords, direction)
                    self.frame_buffer[y, x] += self.scene.cast_ray(ray, 0) / self.spp

            self.update_progress()

    def update_progress(self):
        self.progress += 1
        percentage = 100 * self.progress / self.scene.height
        if percentage == 100:
            print('\rRendering progress: 100.0%', flush=True)
        else:
            print('\rRendering progress: {:.1f}%'.format(percentage), end='', flush=True)
