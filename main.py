import os
import cv2
import random
import numpy as np

from Generator.Hill import Hill
from Generator.Mountain import Mountain
from Generator.Normal import Normal
from Generator.Terrain import Terrain
from Global import *
from Noise import Noise
from RenderingPipeline.Light.Light import Light
from RenderingPipeline.ModelTools.Sphere import Sphere
from RenderingPipeline.ModelTools.Meshes import Meshes
from RenderingPipeline.Render import Render
from RenderingPipeline.Scene import Scene

seed = 1

reso_scale = 1
latitude = 100 * reso_scale
longitude = 200 * reso_scale
radius = 100

# types = [Deep, Shallow, Shore, Grass, Hill, Mountain]
height_range = [100, 102, 103, 103.5, 106, 108, 110]

spp = 1
scene_height = 100
scene_width = 100

planet_filepath = os.path.join('Asset', 'Model', 'planet.ply')

if __name__ == '__main__':
    height_map = np.zeros((latitude, longitude), dtype=np.float64)
    color_map = np.zeros((latitude, longitude), dtype=np.float64)

    terrain = Terrain(latitude, longitude, seed)
    terrain.generate()
    # show_images([terrain.terrain_map], 'grey')

    # generators = []
    # for i in range(4):
    #     generators.append(Normal(latitude, longitude, seed, reso_scale))
    # generators.append(Hill(latitude, longitude, seed, reso_scale))
    # generators.append(Mountain(latitude, longitude, seed, reso_scale))
    #
    # for i in range(len(generators)):
    #     generators[i].generate()
    #     area = terrain.terrain_map == -i
    #     normalized_map = generators[i].normalized_map
    #
    #     height_map[area] = map_value(normalized_map, area, height_range[i], height_range[i + 1] - height_range[i])[area]
    #     color_map[area] = normalized_map[area] * (cmap_values[i + 1] - cmap_values[i]) + cmap_values[i]

    vertex_colors = np.zeros((latitude, longitude, 3), dtype=np.float64)
    for lati in range(latitude):
        for longi in range(longitude):
            vertex_colors[lati, longi] = my_cmap(terrain.normalized_map[lati, longi])[:3]
    vertex_colors = (255 * vertex_colors).astype(int)

    blur = cv2.GaussianBlur(terrain.terrain_map, (19, 19), 2)
    show_images([terrain.terrain_map, blur], my_cmap)




    # sphere = Sphere(latitude, longitude, radius)
    # sphere.radii = terrain.normalized_map * 10 + 100
    # # sphere.radii[normalized_map < 0.5] = normalized_map[normalized_map < 0.5] * terrain_height_range / 2 +\
    # #     terrain_min_height + terrain_height_range / 4
    # sphere.compute_vertices_position()
    # # sphere.compute_vertices_color(normalized_map * 0.1 + 0.99)
    #
    # save_ply(planet_filepath, to_list(sphere.vertices_map), sphere.faces, to_list(vertex_colors))
    # sphere_meshes = Meshes(planet_filepath)
    # sphere_meshes.obj.show()
    #
    # sphere.radii = normalized_map2 * terrain_height_range + terrain_min_height
    # # sphere.radii[normalized_map < 0.5] = normalized_map[normalized_map < 0.5] * terrain_height_range / 2 +\
    # #     terrain_min_height + terrain_height_range / 4
    # sphere.compute_vertices_position()
    # sphere.compute_vertices_color(normalized_map2 * 0.1 + 0.99)
    #
    # save_ply(planet_filepath, to_list(sphere.vertices_map), sphere.faces, to_list(sphere.vertex_colors))
    # sphere_meshes = Meshes(planet_filepath)
    # sphere_meshes.obj.show()

    # pl.radii = cv2.GaussianBlur(pl.radii, (51, 51), 10)

    # planet = Meshes(planet_filepath)
    #
    # light = Light(np.array([150.0, 150.0, -150.0]), np.array([30000.0, 30000.0, 30000.0]))
    #
    # scene = Scene(scene_height, scene_width, 90)
    # scene.add(planet)
    # scene.add(light)
    # scene.build_BVH()
    #
    # render = Render(scene, np.array([0.0, 0.0, -150.0]), spp)
    # render.render()
