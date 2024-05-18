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

# Sphere
reso_scale = 6
latitude = 100 * reso_scale
longitude = 200 * reso_scale
radius = 100

# Terrain
# types = [Deep, Shallow, Shore, Grass, Hill, Dirt, Mountain]
terrain_types = [0.0, 0.4, 0.5, 0.55, 0.7, 0.8, 0.9, 1.0]
mountain_raise = 2.0
dirt_raise = 1.5
hill_raise = 0.3
land_raise = 0.1

# Render
spp = 8
resolution = 4
scene_height = 100 * resolution
scene_width = 100 * resolution

planet_filepath = os.path.join('Asset', 'Model', 'planet.ply')

if __name__ == '__main__':
    terrain = Terrain(latitude, longitude, terrain_types, seed)
    terrain.generate()
    show_images([-1 * terrain.terrain_map], my_terrain_cmap)

    ocean = Normal(latitude, longitude, seed)
    ocean.generate()

    land = Normal(latitude, longitude, seed)
    land.generate()

    hill = Hill(latitude, longitude, seed)
    hill.generate()

    mountain = Mountain(latitude, longitude, seed)
    mountain.generate()

    boundary = terrain.terrain_map.copy()
    boundary[boundary > -3] = 0
    boundary[boundary <= -3] = 1
    blur = cv2.GaussianBlur(boundary, (15, 15), 2)
    height_map = (land.normalized_map + land_raise) * blur + ocean.normalized_map * (1 - blur)

    boundary = terrain.terrain_map.copy()
    boundary[boundary > -4] = 0
    boundary[boundary <= -4] = 1
    blur = cv2.GaussianBlur(boundary, (15, 15), 2)
    height_map = (hill.normalized_map + hill_raise) * blur + height_map * (1 - blur)

    boundary = terrain.terrain_map.copy()
    boundary[boundary > -5] = 0
    boundary[boundary <= -5] = 1
    blur = cv2.GaussianBlur(boundary, (15, 15), 2)
    height_map = (mountain.normalized_map + dirt_raise) * blur + height_map * (1 - blur)

    boundary = terrain.terrain_map.copy()
    boundary[boundary > -6] = 0
    boundary[boundary <= -6] = 1
    blur = cv2.GaussianBlur(boundary, (15, 15), 2)
    height_map = (mountain.normalized_map + mountain_raise) * blur + height_map * (1 - blur)




    vertex_colors = np.zeros((latitude, longitude, 3), dtype=np.float64)
    for lati in range(latitude):
        for longi in range(longitude):
            vertex_colors[lati, longi] = my_cmap(terrain.normalized_map[lati, longi])[:3]
    vertex_colors = (255 * vertex_colors).astype(int)

    sphere = Sphere(latitude, longitude, radius)
    sphere.radii = height_map * 10 + 100
    sphere.compute_vertices_position()

    save_ply(planet_filepath, to_list(sphere.vertices_map), sphere.faces, to_list(vertex_colors))
    # sphere_meshes = Meshes(planet_filepath)
    # sphere_meshes.obj.show()






    planet = Meshes(planet_filepath)
    planet.obj.show()

    light = Light(np.array([300.0, 300.0, -300.0]), np.array([150000.0, 150000.0, 150000.0]))

    scene = Scene(scene_height, scene_width, 90)
    scene.add(planet)
    scene.add(light)
    scene.build_BVH()

    render = Render(scene, np.array([0.0, 0.0, -170.0]), spp)
    render.render()
