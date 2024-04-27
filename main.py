from PerlinNoiseMap import PerlinNoiseMap


width = 100
height = 100


if __name__ == '__main__':
    perlin_map = PerlinNoiseMap(width, height)
    perlin_map.generate_map()
    perlin_map.display_map()


