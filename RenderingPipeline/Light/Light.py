from enum import Enum


class LightType(Enum):
    point = 1
    area = 2


class Light:
    def __init__(self, coords, intensity, light_type=LightType.point):
        self.coords = coords
        self.intensity = intensity
        self.light_type = light_type
