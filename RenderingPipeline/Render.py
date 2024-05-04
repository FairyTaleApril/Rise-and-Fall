import os
import random
import threading
from Global import *
from RayTracingTools.Ray import *


class Render:
    def __init__(self, scene, eye_coords, spp):
        self.scene = scene
        self.eye_coords = eye_coords
        self.spp = spp
        self.scale = math.tan(deg2rad(scene.fov * 0.5))
        self.image_aspect_ratio = scene.width / scene.height
        self.frame_buffer = None

    def render(self):
        self.frame_buffer = np.zeros((self.scene.height, self.scene.width, 3), dtype=np.float32)

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

        return self.frame_buffer

    def render_thread(self, y0, y1):
        for y in range(y0, y1):
            for x in range(self.scene.width):
                index = y * self.scene.width + x
                for k in range(self.spp):
                    sample_x = (2 * (x + random.random()) / self.scene.width - 1) * self.image_aspect_ratio * self.scale
                    sample_y = (1 - 2 * (y + random.random()) / self.scene.height) * self.scale
                    direction = normalize(np.array([sample_x, sample_y, 1]))
                    ray = Ray(self.eye_coords, direction)
                    self.frame_buffer[index] += self.scene.castRay(ray, 0) / self.spp
