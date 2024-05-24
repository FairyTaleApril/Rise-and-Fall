# Playing God: Planetary Terrain Generation Using Perlin Noise
## Overview
This project is a Python-based application that procedurally generates a planet's terrain and renders it using a ray tracing pipeline.
The terrain generation uses a combination of noise functions to create various geological features such as oceans, hills, and mountains.
The rendering pipeline simulates light interaction with the terrain to produce realistic images of the planet.

## Configuration
The script includes several configurable parameters:

* Sphere Parameters:
    * reso_scale: Resolution scale factor.
    * latitude and longitude: Define the resolution of the spherical mesh.
    * radius: Radius of the planet.
* Terrain Parameters:
    * terrain_types: Specifies the thresholds for different terrain types.
    * mountain_raise, dirt_raise, hill_raise, land_raise: Elevation factors for different terrains.
* Render Parameters:
    * spp: Samples per pixel for rendering.
    * resolution: Resolution scale for the rendered image.
    * scene_height and scene_width: Dimensions of the rendered scene.

## Usage
To generate and render a planet, run the main.py script.
At runtime, some result images may pop up.
Closing the popped-up windows will allow the program to continue running until the planet is fully rendered using the ray tracing pipeline.

Please check if you have successfully install visual studio C++ build tools before running it, which can be downlaoded at https://visualstudio.microsoft.com/zh-hans/downloads/.
If the render result does not pop up, please add the followings in main.py:
'import matplotlib'
'matplotlib.use('TkAgg')'
