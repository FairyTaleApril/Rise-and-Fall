import os
import numpy as np

import PerlinNoiseMap
from PerlinNoiseMap import PerlinNoiseGenerator
from RenderingPipeline.ModelTools.Sphere import Sphere
from RenderingPipeline.Render import *
from RenderingPipeline.Scene import *
from RenderingPipeline.ModelTools.Meshes import *

width = 200
height = 200
max_height = 150
min_height = 100

spp = 1

if __name__ == '__main__':
    sphere = Sphere(100, 500)
    # save_model(os.path.join('Asset', 'Model', 'sphere.obj'), sphere.vertices_list, sphere.faces)
    # sphere_meshes = Meshes(filepath=os.path.join('Asset', 'Model', 'sphere.obj'))
    # sphere_meshes.obj.show()

    perlin_generator = PerlinNoiseGenerator()
    perlin_generator.generate_planet(sphere, max_height, min_height)
    save_model(os.path.join('Asset', 'Model', 'planet.obj'), sphere.vertices_list, sphere.faces)
    sphere_meshes = Meshes(filepath=os.path.join('Asset', 'Model', 'planet.obj'))
    sphere_meshes.obj.show()

    # ocean_vertices, ocean_faces = perlin_generator.generate_planet(105, 100, 0)
    #
    # ocean_faces += len(planet_vertices)
    # planet_faces = np.vstack((planet_faces, ocean_faces))
    # planet_vertices = np.vstack((planet_vertices, ocean_vertices))

    # save_model(os.path.join('Asset', 'Model', 'planet.obj'), planet_vertices, planet_faces)
    #
    # planet = Meshes(filepath=os.path.join('Asset', 'Model', 'planet.obj'))
    # planet.obj.show()

    # terrain_map = perlin_generator.generate_map(width, height, max_height, min_height, func=PerlinNoiseMap.logistic,
    #                                             frequency=2, gradient_scale=-0.5, persistence=0.1, lacunarity=2.0)
    # perlin_generator.display_map(terrain_map)
    #
    # terrain_map_vertices, terrain_map_faces = convert_map_to_3d(terrain_map)
    # save_map(os.path.join('Asset', 'Model', 'terrain.obj'), terrain_map_vertices, terrain_map_faces)
    #
    # terrain = Meshes(None)
    # terrain.read_obj(os.path.join('Asset', 'Model', 'terrain.obj'))
    # terrain.obj.show()

    # universal_material = Material()
    #
    # cow = Meshes(universal_material)
    # cow.read_obj('./Asset/Model/cow.obj')
    # cow.obj.show()

    # light = Light(np.array([0.0, 10.0, 0.0]), np.array([100.0, 100.0, 100.0]))
    #
    # scene = Scene(width, height, 90)
    # scene.add(cow)
    # scene.add(light)
    # scene.build_BVH()
    #
    # render = Render(scene, np.array([0.0, 0.0, -2.0]), spp)
    # render.render()

    # mesh = trimesh.Trimesh(vertices=cow.vertices, faces=cow.faces, face_colors=[100, 100, 100])
    # mesh.show()
